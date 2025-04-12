import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import * as modelService from '../services';

// GET /api/models/config - Get model configuration
export const GET: RequestHandler = async ({ request, locals }) => {
  try {
    const token = request.headers.get('authorization')?.split(' ')[1] || '';
    
    const config = await modelService.getModelConfig(token);
    return json({ models: config });
  } catch (error) {
    console.error('Error fetching model config:', error);
    return json({ error: 'Failed to fetch model config' }, { status: 500 });
  }
};

// POST /api/models/config - Update model configuration
export const POST: RequestHandler = async ({ request, locals }) => {
  try {
    const token = request.headers.get('authorization')?.split(' ')[1] || '';
    const data = await request.json();
    
    const result = await modelService.updateModelConfig(token, data.models);
    return json(result);
  } catch (error) {
    console.error('Error updating model config:', error);
    return json({ error: 'Failed to update model config' }, { status: 500 });
  }
};
