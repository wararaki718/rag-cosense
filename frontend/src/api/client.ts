const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';

export async function request<T>(
  path: string,
  options?: RequestInit
): Promise<T> {
  const url = `${API_BASE_URL}${path}`;
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });

  const body = await response.json();

  if (!response.ok || body.status === 'error') {
    const error = new Error(body.message || 'Unknown error');
    (error as any).code = body.code || 'UNKNOWN_ERROR';
    throw error;
  }

  return body;
}
