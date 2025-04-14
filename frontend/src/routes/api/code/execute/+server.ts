import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import * as codeService from '../services';

// POST /api/code/execute - Execute code
export const POST: RequestHandler = async ({ request, locals }) => {
  try {
    const token = request.headers.get('authorization')?.split(' ')[1] || '';
    const data = await request.json();
    
    const result = await codeService.executeCode(token, data.code, data.language || 'python');
    return json(result);
  } catch (error) {
    console.error('Error executing code:', error);
    return json({ error: 'Failed to execute code' }, { status: 500 });
  }
};
