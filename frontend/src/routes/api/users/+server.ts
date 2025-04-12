import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import * as userService from './services';

// GET /api/users - Get all users
export const GET: RequestHandler = async ({ request, url, locals }) => {
  try {
    const token = request.headers.get('authorization')?.split(' ')[1] || '';
    const page = url.searchParams.get('page') ? parseInt(url.searchParams.get('page') as string) : 1;
    const limit = url.searchParams.get('limit') ? parseInt(url.searchParams.get('limit') as string) : 20;
    
    const users = await userService.getUsers(token, page, limit);
    return json(users);
  } catch (error) {
    console.error('Error fetching users:', error);
    return json({ error: 'Failed to fetch users' }, { status: 500 });
  }
};

// POST /api/users - Create a new user
export const POST: RequestHandler = async ({ request, locals }) => {
  try {
    const token = request.headers.get('authorization')?.split(' ')[1] || '';
    const data = await request.json();
    
    const result = await userService.createUser(token, data);
    return json(result);
  } catch (error) {
    console.error('Error creating user:', error);
    return json({ error: 'Failed to create user' }, { status: 500 });
  }
};
