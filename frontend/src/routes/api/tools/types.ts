// Tools API Types

export interface ToolSpec {
  name: string;
  description: string;
  parameters: {
    type: string;
    properties: Record<string, any>;
    required: string[];
  };
}

export interface Tool {
  name: string;
  description: string;
  spec: ToolSpec;
  server?: {
    name: string;
    url: string;
  };
}

export interface ToolListResponse {
  tools: Tool[];
}

export interface ToolExecuteRequest {
  name: string;
  params: Record<string, any>;
}

export interface ToolExecuteResponse {
  result: any;
  error?: string;
}
