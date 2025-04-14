import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import * as fileService from '../services';

// GET /api/files/[id] - Get a file by ID
export const GET: RequestHandler = async ({ params, request, locals }) => {
  try {
    const token = request.headers.get('authorization')?.split(' ')[1] || '';
    const id = params.id;
    
    const file = await fileService.getFileById(token, id);
    return json(file);
  } catch (error) {
    console.error(`Error fetching file ${params.id}:`, error);
    return json({ error: 'Failed to fetch file' }, { status: 500 });
  }
};

// DELETE /api/files/[id] - Delete a file
export const DELETE: RequestHandler = async ({ params, request, locals }) => {
  try {
    const token = request.headers.get('authorization')?.split(' ')[1] || '';
    const id = params.id;
    
    const result = await fileService.deleteFile(token, id);
    return json(result);
  } catch (error) {
    console.error(`Error deleting file ${params.id}:`, error);
    return json({ error: 'Failed to delete file' }, { status: 500 });
  }
};
