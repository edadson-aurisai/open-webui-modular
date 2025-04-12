import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import * as authService from '../services';

// POST /api/auth/register - Register user
export const POST: RequestHandler = async ({ request, locals }) => {
  try {
    const data = await request.json();
    
    const result = await authService.register(data);
    return json(result);
  } catch (error) {
    console.error('Error registering user:', error);
    return json({ error: 'Failed to register user' }, { status: 500 });
  }
};
