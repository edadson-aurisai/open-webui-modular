import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import * as chatService from '../services';

// GET /api/chats/[id] - Get a chat by ID
export const GET: RequestHandler = async ({ params, request, locals }) => {
  try {
    const token = request.headers.get('authorization')?.split(' ')[1] || '';
    const id = params.id;
    
    const chat = await chatService.getChatById(token, id);
    return json(chat);
  } catch (error) {
    console.error(`Error fetching chat ${params.id}:`, error);
    return json({ error: 'Failed to fetch chat' }, { status: 500 });
  }
};

// POST /api/chats/[id] - Update a chat
export const POST: RequestHandler = async ({ params, request, locals }) => {
  try {
    const token = request.headers.get('authorization')?.split(' ')[1] || '';
    const id = params.id;
    const data = await request.json();
    
    const result = await chatService.updateChatById(token, id, data.chat);
    return json(result);
  } catch (error) {
    console.error(`Error updating chat ${params.id}:`, error);
    return json({ error: 'Failed to update chat' }, { status: 500 });
  }
};

// DELETE /api/chats/[id] - Delete a chat
export const DELETE: RequestHandler = async ({ params, request, locals }) => {
  try {
    const token = request.headers.get('authorization')?.split(' ')[1] || '';
    const id = params.id;
    
    const result = await chatService.deleteChatById(token, id);
    return json(result);
  } catch (error) {
    console.error(`Error deleting chat ${params.id}:`, error);
    return json({ error: 'Failed to delete chat' }, { status: 500 });
  }
};
