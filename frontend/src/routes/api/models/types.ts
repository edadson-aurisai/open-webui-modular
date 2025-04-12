// Models API Types

export interface Model {
  id: string;
  name: string;
  owned_by: string;
  direct?: boolean;
  openai?: {
    id: string;
  };
  urlIdx?: string;
  tags?: string[];
}

export interface ModelResponse {
  data: Model[];
}

export interface ModelConfig {
  id: string;
  name: string;
  meta: ModelMeta;
  base_model_id?: string;
  params: ModelParams;
}

export interface ModelMeta {
  description?: string;
  capabilities?: object;
  profile_image_url?: string;
}

export interface ModelParams {}

export type GlobalModelConfig = ModelConfig[];
