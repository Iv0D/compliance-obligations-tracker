import type { ApiError } from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export class ApiResponseError extends Error {
  constructor(
    public readonly code: string,
    message: string,
    public readonly status: number
  ) {
    super(message);
    this.name = "ApiResponseError";
  }
}

async function throwIfError(response: Response): Promise<Response> {
  if (response.ok) return response;
  let code = "unknown_error";
  let message = response.statusText;
  try {
    const body = (await response.json()) as { error: ApiError };
    code = body.error.code;
    message = body.error.message;
  } catch {
    /* use statusText */
  }
  throw new ApiResponseError(code, message, response.status);
}

export async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...init?.headers },
  });
  await throwIfError(response);
  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}
