import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import * as authService from '../services';

// POST /api/auth/reset-password - Reset password
export const POST: RequestHandler = async ({ request, locals }) => {
  try {
    const data = await request.json();
    
    const result = await authService.resetPassword(data);
    return json(result);
  } catch (error) {
    console.error('Error resetting password:', error);
    return json({ error: 'Failed to reset password' }, { status: 500 });
  }
};
