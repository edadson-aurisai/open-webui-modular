import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import * as modelService from './services';

// GET /api/models - Get all models
export const GET: RequestHandler = async ({ request, url, locals }) => {
  try {
    const token = request.headers.get('authorization')?.split(' ')[1] || '';
    const base = url.searchParams.has('base');
    
    // Note: In a real implementation, you would get connections from the user's session
    // For now, we'll pass null
    const models = await modelService.getModels(token, null, base);
    return json({ data: models });
  } catch (error) {
    console.error('Error fetching models:', error);
    return json({ error: 'Failed to fetch models' }, { status: 500 });
  }
};
