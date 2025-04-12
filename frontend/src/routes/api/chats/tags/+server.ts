import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import * as chatService from '../services';

// GET /api/chats/tags - Get all tags
export const GET: RequestHandler = async ({ request, locals }) => {
  try {
    const token = request.headers.get('authorization')?.split(' ')[1] || '';
    
    const tags = await chatService.getAllTags(token);
    return json(tags);
  } catch (error) {
    console.error('Error fetching tags:', error);
    return json({ error: 'Failed to fetch tags' }, { status: 500 });
  }
};
