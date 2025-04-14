import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import * as toolService from './services';

// GET /api/tools - Get all tools
export const GET: RequestHandler = async ({ request, locals }) => {
  try {
    const token = request.headers.get('authorization')?.split(' ')[1] || '';
    
    const tools = await toolService.getTools(token);
    return json(tools);
  } catch (error) {
    console.error('Error fetching tools:', error);
    return json({ error: 'Failed to fetch tools' }, { status: 500 });
  }
};
