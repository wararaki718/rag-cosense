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
  let response: Response;
  try {
    response = await fetch(url, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
    });
  } catch (e: unknown) {
    console.error(`Fetch failed for ${url}:`, e);
    throw new ServiceError(
      `Network Error: Failed to fetch from ${url}. Please ensure the server is running and reachable.`,
      "NETWORK_ERROR"
    );
  }

  const contentType = response.headers.get("content-type") || "";
  if (!contentType.toLowerCase().includes("application/json")) {
    const text = await response.text();
    console.error(`Non-JSON response from ${url}:`, response.status, contentType, text.substring(0, 500));
    
    if (response.status === 502 || response.status === 504) {
      throw new ServiceError("Cannot reach the server. Please ensure the backend is running.", "SERVER_UNREACHABLE");
    }
    
    throw new ServiceError(
      `Server Error (${response.status}): The server returned an invalid response format (not JSON). Content-Type: ${contentType}`,
      "INVALID_RESPONSE_FORMAT"
    );
  }

  const body = await response.json();

  if (!response.ok || body.status === "error") {
    throw new ServiceError(
      body.message || "Unknown error",
      body.code || "UNKNOWN_ERROR",
    );
  }

  return body;
}
