import { WEBUI_BASE_URL } from '$lib/constants';
import type { 
  BackendConfig, 
  ModelFilterConfig, 
  GlobalModelConfig,
  WebhookConfig,
  CommunitySharingConfig
} from './types';

/**
 * Get backend configuration
 */
export async function getBackendConfig(): Promise<BackendConfig> {
  const response = await fetch(`${WEBUI_BASE_URL}/api/config`, {
    method: 'GET',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json'
    }
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }

  return response.json();
}

/**
 * Get model filter configuration
 */
export async function getModelFilterConfig(token: string): Promise<ModelFilterConfig> {
  const response = await fetch(`${WEBUI_BASE_URL}/api/config/model/filter`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    }
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }

  return response.json();
}

/**
 * Update model filter configuration
 */
export async function updateModelFilterConfig(
  token: string,
  enabled: boolean,
  models: string[]
): Promise<ModelFilterConfig> {
  const response = await fetch(`${WEBUI_BASE_URL}/api/config/model/filter`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({
      enabled: enabled,
      models: models
    })
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }

  return response.json();
}

/**
 * Get model configuration
 */
export async function getModelConfig(token: string): Promise<GlobalModelConfig> {
  const response = await fetch(`${WEBUI_BASE_URL}/api/config/models`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    }
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }

  const res = await response.json();
  return res.models;
}

/**
 * Update model configuration
 */
export async function updateModelConfig(
  token: string,
  config: GlobalModelConfig
): Promise<any> {
  const response = await fetch(`${WEBUI_BASE_URL}/api/config/models`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({
      models: config
    })
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }

  return response.json();
}

/**
 * Get webhook URL
 */
export async function getWebhookUrl(token: string): Promise<WebhookConfig> {
  const response = await fetch(`${WEBUI_BASE_URL}/api/webhook`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    }
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }

  return response.json();
}

/**
 * Update webhook URL
 */
export async function updateWebhookUrl(token: string, url: string): Promise<WebhookConfig> {
  const response = await fetch(`${WEBUI_BASE_URL}/api/webhook`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({
      url: url
    })
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }

  return response.json();
}

/**
 * Get community sharing enabled status
 */
export async function getCommunitySharingEnabledStatus(token: string): Promise<CommunitySharingConfig> {
  const response = await fetch(`${WEBUI_BASE_URL}/api/community_sharing`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    }
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }

  return response.json();
}

/**
 * Toggle community sharing enabled status
 */
export async function toggleCommunitySharingEnabledStatus(token: string): Promise<CommunitySharingConfig> {
  const response = await fetch(`${WEBUI_BASE_URL}/api/community_sharing/toggle`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    }
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }

  return response.json();
}

/**
 * Get changelog
 */
export async function getChangelog(): Promise<any> {
  const response = await fetch(`${WEBUI_BASE_URL}/api/changelog`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }

  return response.json();
}

/**
 * Get version updates
 */
export async function getVersionUpdates(token: string): Promise<any> {
  const response = await fetch(`${WEBUI_BASE_URL}/api/version/updates`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    }
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }

  return response.json();
}
