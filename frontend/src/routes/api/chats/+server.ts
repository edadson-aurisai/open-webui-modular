import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import * as chatService from './services';

// GET /api/chats - Get all chats
export const GET: RequestHandler = async ({ request, url, locals }) => {
  try {
    const token = request.headers.get('authorization')?.split(' ')[1] || '';
    const page = url.searchParams.get('page') ? parseInt(url.searchParams.get('page') as string) : null;
    
    const chats = await chatService.getChats(token, page);
    return json(chats);
  } catch (error) {
    console.error('Error fetching chats:', error);
    return json({ error: 'Failed to fetch chats' }, { status: 500 });
  }
};

// POST /api/chats - Create a new chat
export const POST: RequestHandler = async ({ request, locals }) => {
  try {
    const token = request.headers.get('authorization')?.split(' ')[1] || '';
    const data = await request.json();
    
    const result = await chatService.createChat(token, data);
    return json(result);
  } catch (error) {
    console.error('Error creating chat:', error);
    return json({ error: 'Failed to create chat' }, { status: 500 });
  }
};

// DELETE /api/chats - Delete all chats
export const DELETE: RequestHandler = async ({ request, locals }) => {
  try {
    const token = request.headers.get('authorization')?.split(' ')[1] || '';
    
    // This would need to be implemented in the service layer
    // For now, we'll return a not implemented response
    return json({ error: 'Delete all chats not implemented' }, { status: 501 });
  } catch (error) {
    console.error('Error deleting all chats:', error);
    return json({ error: 'Failed to delete all chats' }, { status: 500 });
  }
};
