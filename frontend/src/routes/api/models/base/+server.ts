import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import * as modelService from '../services';

// GET /api/models/base - Get base models
export const GET: RequestHandler = async ({ request, locals }) => {
  try {
    const token = request.headers.get('authorization')?.split(' ')[1] || '';
    
    // Note: In a real implementation, you would get connections from the user's session
    // For now, we'll pass null and set base to true
    const models = await modelService.getModels(token, null, true);
    return json({ data: models });
  } catch (error) {
    console.error('Error fetching base models:', error);
    return json({ error: 'Failed to fetch base models' }, { status: 500 });
  }
};
