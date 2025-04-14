import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import * as toolService from '../services';

// POST /api/tools/server - Execute a tool server
export const POST: RequestHandler = async ({ request, locals }) => {
  try {
    const token = request.headers.get('authorization')?.split(' ')[1] || '';
    const data = await request.json();
    
    const { url, name, params, serverData } = data;
    
    const result = await toolService.executeToolServer(token, url, name, params, serverData);
    return json(result);
  } catch (error) {
    console.error('Error executing tool server:', error);
    return json({ error: 'Failed to execute tool server' }, { status: 500 });
  }
};
