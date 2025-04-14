import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import * as configService from '../config/services';

// GET /api/community_sharing - Get community sharing enabled status
export const GET: RequestHandler = async ({ request, locals }) => {
  try {
    const token = request.headers.get('authorization')?.split(' ')[1] || '';
    
    const config = await configService.getCommunitySharingEnabledStatus(token);
    return json(config);
  } catch (error) {
    console.error('Error fetching community sharing status:', error);
    return json({ error: 'Failed to fetch community sharing status' }, { status: 500 });
  }
};
