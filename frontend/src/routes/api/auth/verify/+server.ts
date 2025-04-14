import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import * as authService from '../services';

// GET /api/auth/verify - Verify session
export const GET: RequestHandler = async ({ request, locals }) => {
  try {
    const token = request.headers.get('authorization')?.split(' ')[1] || '';
    
    const result = await authService.verifySession(token);
    return json(result);
  } catch (error) {
    console.error('Error verifying session:', error);
    return json({ error: 'Invalid or expired session' }, { status: 401 });
  }
};
