import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import * as fileService from '../services';

// GET /api/files/list - List files
export const GET: RequestHandler = async ({ request, url, locals }) => {
  try {
    const token = request.headers.get('authorization')?.split(' ')[1] || '';
    const collectionName = url.searchParams.get('collection_name') || undefined;
    
    const files = await fileService.listFiles(token, collectionName);
    return json(files);
  } catch (error) {
    console.error('Error listing files:', error);
    return json({ error: 'Failed to list files' }, { status: 500 });
  }
};
