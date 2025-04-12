import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import * as chatService from '../services';

// GET /api/chats/pinned - Get pinned chats
export const GET: RequestHandler = async ({ request, locals }) => {
  try {
    const token = request.headers.get('authorization')?.split(' ')[1] || '';
    
    const chats = await chatService.getPinnedChats(token);
    return json(chats);
  } catch (error) {
    console.error('Error fetching pinned chats:', error);
    return json({ error: 'Failed to fetch pinned chats' }, { status: 500 });
  }
};
