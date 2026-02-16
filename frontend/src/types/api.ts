export interface Source {
  title: string;
  url: string;
  score: number;
}

export interface ChatRequest {
  query: string;
  context_history?: Array<{
    role: 'user' | 'assistant';
    content: string;
  }>;
}

export interface ChatSuccessResponse {
  status: 'success';
  data: {
    answer: string;
    sources: Source[];
  };
}

export interface ChatErrorResponse {
  status: 'error';
  message: string;
  code: string;
}

export type ChatResponse = ChatSuccessResponse | ChatErrorResponse;
