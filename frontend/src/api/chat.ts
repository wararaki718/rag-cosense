import { request } from './client';
import type { ChatRequest, ChatSuccessResponse } from '../types/api';

export async function sendChatMessage(payload: ChatRequest): Promise<ChatSuccessResponse> {
  return request<ChatSuccessResponse>('/chat', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}
