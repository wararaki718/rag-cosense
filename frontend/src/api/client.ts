const API_BASE_URL = import.meta.env.VITE_API_URL || "/api/v1";

export class ServiceError extends Error {
  code?: string;
  constructor(message: string, code?: string) {
    super(message);
    this.name = "ServiceError";
    this.code = code;
  }
}

export async function request<T>(
  path: string,
  options?: RequestInit,
): Promise<T> {
  const url = `${API_BASE_URL}${path}`;
  const response = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });

  const body = await response.json();

  if (!response.ok || body.status === "error") {
    throw new ServiceError(
      body.message || "Unknown error",
      body.code || "UNKNOWN_ERROR",
    );
  }

  return body;
}
