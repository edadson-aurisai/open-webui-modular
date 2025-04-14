import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import * as userService from '../services';

// GET /api/users/me - Get current user
export const GET: RequestHandler = async ({ request, locals }) => {
  try {
    const token = request.headers.get('authorization')?.split(' ')[1] || '';
    
    const user = await userService.getCurrentUser(token);
    return json(user);
  } catch (error) {
    console.error('Error fetching current user:', error);
    return json({ error: 'Failed to fetch current user' }, { status: 500 });
  }
};
