import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import * as authService from '../services';

// POST /api/auth/logout - Logout user
export const POST: RequestHandler = async ({ request, locals }) => {
  try {
    const token = request.headers.get('authorization')?.split(' ')[1] || '';
    
    await authService.logout(token);
    return json({ success: true });
  } catch (error) {
    console.error('Error logging out:', error);
    return json({ error: 'Failed to logout' }, { status: 500 });
  }
};
