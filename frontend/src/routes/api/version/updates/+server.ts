import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import * as configService from '../../../config/services';

// GET /api/version/updates - Get version updates
export const GET: RequestHandler = async ({ request, locals }) => {
  try {
    const token = request.headers.get('authorization')?.split(' ')[1] || '';
    
    const updates = await configService.getVersionUpdates(token);
    return json(updates);
  } catch (error) {
    console.error('Error fetching version updates:', error);
    return json({ error: 'Failed to fetch version updates' }, { status: 500 });
  }
};
