import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import * as configService from '../../services';

// GET /api/config/model/filter - Get model filter configuration
export const GET: RequestHandler = async ({ request, locals }) => {
  try {
    const token = request.headers.get('authorization')?.split(' ')[1] || '';
    
    const config = await configService.getModelFilterConfig(token);
    return json(config);
  } catch (error) {
    console.error('Error fetching model filter config:', error);
    return json({ error: 'Failed to fetch model filter config' }, { status: 500 });
  }
};

// POST /api/config/model/filter - Update model filter configuration
export const POST: RequestHandler = async ({ request, locals }) => {
  try {
    const token = request.headers.get('authorization')?.split(' ')[1] || '';
    const data = await request.json();
    
    const result = await configService.updateModelFilterConfig(token, data.enabled, data.models);
    return json(result);
  } catch (error) {
    console.error('Error updating model filter config:', error);
    return json({ error: 'Failed to update model filter config' }, { status: 500 });
  }
};
