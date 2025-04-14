import { WEBUI_BASE_URL } from '$lib/constants';
import type { CodeExecuteRequest, CodeExecuteResponse, CodeInterpreterRequest, CodeInterpreterResponse } from './types';

/**
 * Execute code on the backend server
 */
export async function executeCode(
  token: string,
  code: string,
  language: string = "python"
): Promise<CodeExecuteResponse> {
  const response = await fetch(`${WEBUI_BASE_URL}/api/agent/code/execute`, {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      ...(token && { authorization: `Bearer ${token}` })
    },
    body: JSON.stringify({
      code,
      language
    })
  });

  if (!response.ok) {
    const error = await response.json();
    throw error.detail || error;
  }

  return response.json();
}

/**
 * Run code interpreter on the backend server
 */
export async function runCodeInterpreter(
  token: string,
  query: string,
  context?: string
): Promise<CodeInterpreterResponse> {
  const response = await fetch(`${WEBUI_BASE_URL}/api/agent/code/interpreter`, {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      ...(token && { authorization: `Bearer ${token}` })
    },
    body: JSON.stringify({
      query,
      ...(context && { context })
    })
  });

  if (!response.ok) {
    const error = await response.json();
    throw error.detail || error;
  }

  return response.json();
}
