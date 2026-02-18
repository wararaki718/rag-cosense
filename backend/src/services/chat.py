from typing import List, Tuple, Optional, Any
import httpx
import logging
import urllib.parse
import re
from elasticsearch import AsyncElasticsearch
from src.core.config import settings
from src.schemas.chat import Message, Source

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self) -> None:
        self.es = AsyncElasticsearch(settings.ELASTICSEARCH_URL)
        self.encoder_url = settings.ENCODER_SERVICE_URL
        self.ollama_url = f"{settings.OLLAMA_BASE_URL}/api/generate"

    def _clean_text(self, text: str) -> str:
        """Removes HTML tags and other noise from the text."""
        # Remove HTML tags
        text = re.sub(r'<[^>]*>', '', text)
        # Normalize whitespace (but keep some newlines for clarity in chat)
        text = re.sub(r'[ \t]+', ' ', text).strip()
        return text

    async def get_sparse_embeddings(self, query: str) -> dict[str, float]:
        """Generates a sparse embedding for the given query using the encoder service."""
        try:
            url = f"{self.encoder_url}/encode"
            payload = {"text": query}
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, timeout=60.0)
                response.raise_for_status()
                data = response.json()
                return data["sparse_values"]
        except Exception as e:
            logger.error(f"Encoder service failed: {e}")
            return {}

    async def retrieve_contexts(self, sparse_vector: dict[str, float], top_k: int = 5) -> Tuple[List[Source], List[Any]]:
        """Retrieves relevant contexts from Elasticsearch using the sparse vector."""
        if not sparse_vector:
            return [], []
            
        index_name = "cosense_pages"
        
        # Build elasticsearch query using rank_feature
        # We search with each token in the sparse_vector
        search_query = {
            "query": {
                "bool": {
                    "should": [
                        {"rank_feature": {"field": f"sparse_vector.{token}", "boost": weight}}
                        for token, weight in sparse_vector.items()
                        if token # Ensure token is not empty
                    ]
                }
            },
            "_source": ["text", "metadata.title"],
            "size": top_k
        }

        try:
            response = await self.es.search(index=index_name, body=search_query)
        except Exception as e:
            logger.error(f"Elasticsearch search failed: {e}")
            return [], []

        sources = []
        hits = response["hits"]["hits"]
        for hit in hits:
            text = hit["_source"].get("text", "")
            title = hit["_source"].get("metadata", {}).get("title", "Untitled")
            score = hit.get("_score", 0.0)
            project = settings.COSENSE_PROJECT_NAME
            
            # URL encode the title but handle spaces specifically for Scrapbox
            safe_title = urllib.parse.quote(title.replace(' ', '_'), safe="")
            url = f"https://scrapbox.io/{project}/{safe_title}"
            
            sources.append(Source(
                title=title,
                url=url,
                score=float(score)
            ))
            hit["text"] = text
            
        return sources, hits

    async def process_query(self, query: str, context_history: Optional[List[Message]] = None) -> Tuple[str, List[Source]]:
        # 0. Clean input query
        cleaned_query = self._clean_text(query)
        
        # 1. Get sparse embedding for the query
        sparse_vector = await self.get_sparse_embeddings(cleaned_query)
        
        # 2. Retrieve contexts from Elasticsearch
        sources, hits = await self.retrieve_contexts(sparse_vector)
        
        # 3. Construct Context from hits
        context_parts = []
        for hit in hits:
            title = hit["_source"].get("metadata", {}).get("title", "Untitled")
            text = hit.get("text", "")
            context_parts.append(f"Source: {title}\nContent: {text}")
        context_text = "\n\n".join(context_parts)
        
        # 4. Construct Prompt
        chat_history_str = ""
        if context_history:
            chat_history_str = "\n".join([f"{msg.role}: {msg.content}" for msg in context_history])
            
        system_prompt = f"""あなたはCosense (Scrapbox) のナレッジベースをもとに回答するAIアシスタントです。
以下のコンテキストと会話履歴をもとに、ユーザーの質問に日本語で回答してください。
分からない場合は「分かりません」と答えてください。

【コンテキスト】
{context_text}

【会話履歴】
{chat_history_str}

【質問】
{query}

【回答】"""

        # 5. Call Ollama
        payload = {
            "model": settings.EMBEDDING_MODEL,
            "prompt": system_prompt,
            "stream": False
        }
        
        answer = "エラーが発生しました。しばらくしてからもう一度お試しください。"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.ollama_url, json=payload, timeout=120.0)
                
                # Check for non-JSON response which might happen on server errors (HTML)
                content_type = response.headers.get("content-type", "")
                if "application/json" not in content_type:
                    logger.error(f"Ollama returned non-JSON response: {response.status_code} {content_type}")
                    answer = "生成サービスが現在利用できません (Server Response is not JSON)。"
                else:
                    response.raise_for_status()
                    data = response.json()
                    answer = data.get("response", "回答を生成できませんでした。")
        except Exception as e:
            logger.error(f"Ollama inference failed: {e}")
            # If it's a known error message, might want to be more specific, 
            # but usually telling the user an error occurred is enough.
            answer = f"エラーが発生しました: {str(e)}"
            
        return answer, sources
