import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import * as userService from '../services';

// GET /api/users/[id] - Get a user by ID
export const GET: RequestHandler = async ({ params, request, locals }) => {
  try {
    const token = request.headers.get('authorization')?.split(' ')[1] || '';
    const id = params.id;
    
    const user = await userService.getUserById(token, id);
    return json(user);
  } catch (error) {
    console.error(`Error fetching user ${params.id}:`, error);
    return json({ error: 'Failed to fetch user' }, { status: 500 });
  }
};

// PUT /api/users/[id] - Update a user
export const PUT: RequestHandler = async ({ params, request, locals }) => {
  try {
    const token = request.headers.get('authorization')?.split(' ')[1] || '';
    const id = params.id;
    const data = await request.json();
    
    const result = await userService.updateUser(token, id, data);
    return json(result);
  } catch (error) {
    console.error(`Error updating user ${params.id}:`, error);
    return json({ error: 'Failed to update user' }, { status: 500 });
  }
};

// DELETE /api/users/[id] - Delete a user
export const DELETE: RequestHandler = async ({ params, request, locals }) => {
  try {
    const token = request.headers.get('authorization')?.split(' ')[1] || '';
    const id = params.id;
    
    await userService.deleteUser(token, id);
    return json({ success: true });
  } catch (error) {
    console.error(`Error deleting user ${params.id}:`, error);
    return json({ error: 'Failed to delete user' }, { status: 500 });
  }
};
