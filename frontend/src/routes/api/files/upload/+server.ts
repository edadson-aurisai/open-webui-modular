import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import * as fileService from '../services';

// POST /api/files/upload - Upload a file
export const POST: RequestHandler = async ({ request, locals }) => {
  try {
    const token = request.headers.get('authorization')?.split(' ')[1] || '';
    
    // Handle multipart form data
    const formData = await request.formData();
    const file = formData.get('file') as File;
    const collectionName = formData.get('collection_name') as string || undefined;
    
    if (!file) {
      return json({ error: 'No file provided' }, { status: 400 });
    }
    
    const result = await fileService.uploadFile(token, file, collectionName);
    return json(result);
  } catch (error) {
    console.error('Error uploading file:', error);
    return json({ error: 'Failed to upload file' }, { status: 500 });
  }
};
