import { WEBUI_BASE_URL } from '$lib/constants';
import type { Model, GlobalModelConfig } from './types';
import { getOpenAIModelsDirect } from '$lib/apis/openai';

/**
 * Get all models
 */
export async function getModels(
  token: string = '',
  connections: object | null = null,
  base: boolean = false
): Promise<Model[]> {
  const response = await fetch(`${WEBUI_BASE_URL}/api/models${base ? '/base' : ''}`, {
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
  let models = res?.data ?? [];

  if (connections && !base) {
    let localModels = [];

    if (connections) {
      const OPENAI_API_BASE_URLS = connections.OPENAI_API_BASE_URLS;
      const OPENAI_API_KEYS = connections.OPENAI_API_KEYS;
      const OPENAI_API_CONFIGS = connections.OPENAI_API_CONFIGS;

      const requests = [];
      for (const idx in OPENAI_API_BASE_URLS) {
        const url = OPENAI_API_BASE_URLS[idx];

        if (idx.toString() in OPENAI_API_CONFIGS) {
          const apiConfig = OPENAI_API_CONFIGS[idx.toString()] ?? {};

          const enable = apiConfig?.enable ?? true;
          const modelIds = apiConfig?.model_ids ?? [];

          if (enable) {
            if (modelIds.length > 0) {
              const modelList = {
                object: 'list',
                data: modelIds.map((modelId) => ({
                  id: modelId,
                  name: modelId,
                  owned_by: 'openai',
                  openai: { id: modelId },
                  urlIdx: idx
                }))
              };

              requests.push(
                (async () => {
                  return modelList;
                })()
              );
            } else {
              requests.push(
                (async () => {
                  return await getOpenAIModelsDirect(url, OPENAI_API_KEYS[idx])
                    .then((res) => {
                      return res;
                    })
                    .catch((err) => {
                      return {
                        object: 'list',
                        data: [],
                        urlIdx: idx
                      };
                    });
                })()
              );
            }
          } else {
            requests.push(
              (async () => {
                return {
                  object: 'list',
                  data: [],
                  urlIdx: idx
                };
              })()
            );
          }
        }
      }

      const responses = await Promise.all(requests);

      for (const idx in responses) {
        const response = responses[idx];
        const apiConfig = OPENAI_API_CONFIGS[idx.toString()] ?? {};

        let models = Array.isArray(response) ? response : (response?.data ?? []);
        models = models.map((model) => ({ ...model, openai: { id: model.id }, urlIdx: idx }));

        const prefixId = apiConfig.prefix_id;
        if (prefixId) {
          for (const model of models) {
            model.id = `${prefixId}.${model.id}`;
          }
        }

        const tags = apiConfig.tags;
        if (tags) {
          for (const model of models) {
            model.tags = tags;
          }
        }

        localModels = localModels.concat(models);
      }
    }

    models = models.concat(
      localModels.map((model) => ({
        ...model,
        name: model?.name ?? model?.id,
        direct: true
      }))
    );

    // Remove duplicates
    const modelsMap = {};
    for (const model of models) {
      modelsMap[model.id] = model;
    }

    models = Object.values(modelsMap);
  }

  return models;
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
export async function updateModelConfig(token: string, config: GlobalModelConfig): Promise<any> {
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
