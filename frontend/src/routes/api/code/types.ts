// Code API Types

export interface CodeExecuteRequest {
  code: string;
  language: string;
}

export interface CodeExecuteResponse {
  result: string;
  stdout?: string;
  stderr?: string;
  execution_time?: number;
}

export interface CodeInterpreterRequest {
  query: string;
  context?: string;
}

export interface CodeInterpreterResponse {
  result: string;
  stdout?: string;
  stderr?: string;
  execution_time?: number;
}
