// Config API Types

export interface BackendConfig {
  version: string;
  auth: {
    enabled: boolean;
    providers: string[];
    registration_enabled: boolean;
  };
  features: {
    chat: boolean;
    tts: boolean;
    images: boolean;
    vision: boolean;
    tools: boolean;
    retrieval: boolean;
    code_execution: boolean;
  };
  ui: {
    theme: string;
    default_language: string;
    available_languages: string[];
  };
  [key: string]: any;
}

export interface ModelFilterConfig {
  enabled: boolean;
  models: string[];
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

export interface WebhookConfig {
  url: string;
}

export interface CommunitySharingConfig {
  enabled: boolean;
}
