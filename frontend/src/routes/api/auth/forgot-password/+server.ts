import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import * as authService from '../services';

// POST /api/auth/forgot-password - Forgot password
export const POST: RequestHandler = async ({ request, locals }) => {
  try {
    const data = await request.json();
    
    const result = await authService.forgotPassword(data);
    return json(result);
  } catch (error) {
    console.error('Error processing forgot password request:', error);
    return json({ error: 'Failed to process forgot password request' }, { status: 500 });
  }
};
