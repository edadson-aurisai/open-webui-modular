import { WEBUI_BASE_URL } from '$lib/constants';
import type { Tool, ToolListResponse, ToolExecuteRequest, ToolExecuteResponse } from './types';
import { convertOpenApiToToolPayload } from '$lib/utils';

/**
 * Get all tools
 */
export async function getTools(token: string): Promise<ToolListResponse> {
  const response = await fetch(`${WEBUI_BASE_URL}/api/v1/agent/tools`, {
    method: 'GET',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      authorization: `Bearer ${token}`
    }
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }

  return response.json();
}

/**
 * Execute a tool
 */
export async function executeTool(
  token: string,
  toolRequest: ToolExecuteRequest
): Promise<ToolExecuteResponse> {
  const response = await fetch(`${WEBUI_BASE_URL}/api/v1/agent/tools/execute`, {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      authorization: `Bearer ${token}`
    },
    body: JSON.stringify(toolRequest)
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }

  return response.json();
}

/**
 * Get tool server data
 */
export async function getToolServerData(token: string, url: string): Promise<any> {
  const response = await fetch(`${url}`, {
    method: 'GET',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      ...(token && { authorization: `Bearer ${token}` })
    }
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }

  const res = await response.json();
  
  const data = {
    openapi: res,
    info: res.info,
    specs: convertOpenApiToToolPayload(res)
  };

  return data;
}

/**
 * Execute a tool server
 */
export async function executeToolServer(
  token: string,
  url: string,
  name: string,
  params: Record<string, any>,
  serverData: { openapi: any; info: any; specs: any }
): Promise<any> {
  try {
    // Find the matching operationId in the OpenAPI spec
    const matchingRoute = Object.entries(serverData.openapi.paths).find(([_, methods]) =>
      Object.entries(methods as any).some(([__, operation]: any) => operation.operationId === name)
    );

    if (!matchingRoute) {
      throw new Error(`No matching route found for operationId: ${name}`);
    }

    const [routePath, methods] = matchingRoute;

    const methodEntry = Object.entries(methods as any).find(
      ([_, operation]: any) => operation.operationId === name
    );

    if (!methodEntry) {
      throw new Error(`No matching method found for operationId: ${name}`);
    }

    const [httpMethod, operation]: [string, any] = methodEntry;

    // Split parameters by type
    const pathParams: Record<string, any> = {};
    const queryParams: Record<string, any> = {};
    let bodyParams: any = {};

    if (operation.parameters) {
      operation.parameters.forEach((param: any) => {
        const paramName = param.name;
        const paramIn = param.in;
        if (params.hasOwnProperty(paramName)) {
          if (paramIn === 'path') {
            pathParams[paramName] = params[paramName];
          } else if (paramIn === 'query') {
            queryParams[paramName] = params[paramName];
          }
        }
      });
    }

    let finalUrl = `${url}${routePath}`;

    // Replace path parameters (`{param}`)
    Object.entries(pathParams).forEach(([key, value]) => {
      finalUrl = finalUrl.replace(new RegExp(`{${key}}`, 'g'), encodeURIComponent(value));
    });

    // Append query parameters to URL if any
    if (Object.keys(queryParams).length > 0) {
      const queryString = new URLSearchParams(
        Object.entries(queryParams).map(([k, v]) => [k, String(v)])
      ).toString();
      finalUrl += `?${queryString}`;
    }

    // Handle requestBody composite
    if (operation.requestBody && operation.requestBody.content) {
      if (params !== undefined) {
        bodyParams = params;
      } else {
        // Optional: Fallback or explicit error if body is expected but not provided
        throw new Error(`Request body expected for operation '${name}' but none found.`);
      }
    }

    // Prepare headers and request options
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(token && { authorization: `Bearer ${token}` })
    };

    let requestOptions: RequestInit = {
      method: httpMethod.toUpperCase(),
      headers
    };

    if (['post', 'put', 'patch'].includes(httpMethod.toLowerCase()) && operation.requestBody) {
      requestOptions.body = JSON.stringify(bodyParams);
    }

    const res = await fetch(finalUrl, requestOptions);
    if (!res.ok) {
      const resText = await res.text();
      throw new Error(`HTTP error! Status: ${res.status}. Message: ${resText}`);
    }

    return await res.json();
  } catch (err: any) {
    console.error('API Request Error:', err.message);
    return { error: err.message };
  }
}
