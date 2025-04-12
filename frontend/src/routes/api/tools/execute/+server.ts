import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import * as toolService from '../services';

// POST /api/tools/execute - Execute a tool
export const POST: RequestHandler = async ({ request, locals }) => {
  try {
    const token = request.headers.get('authorization')?.split(' ')[1] || '';
    const data = await request.json();
    
    const result = await toolService.executeTool(token, data);
    return json(result);
  } catch (error) {
    console.error('Error executing tool:', error);
    return json({ error: 'Failed to execute tool' }, { status: 500 });
  }
};
