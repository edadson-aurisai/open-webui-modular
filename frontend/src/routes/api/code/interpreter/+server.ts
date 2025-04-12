import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import * as codeService from '../services';

// POST /api/code/interpreter - Run code interpreter
export const POST: RequestHandler = async ({ request, locals }) => {
  try {
    const token = request.headers.get('authorization')?.split(' ')[1] || '';
    const data = await request.json();
    
    const result = await codeService.runCodeInterpreter(token, data.query, data.context);
    return json(result);
  } catch (error) {
    console.error('Error running code interpreter:', error);
    return json({ error: 'Failed to run code interpreter' }, { status: 500 });
  }
};
