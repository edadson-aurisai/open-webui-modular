import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import * as configService from '../../config/services';

// GET /api/community_sharing/toggle - Toggle community sharing enabled status
export const GET: RequestHandler = async ({ request, locals }) => {
  try {
    const token = request.headers.get('authorization')?.split(' ')[1] || '';
    
    const result = await configService.toggleCommunitySharingEnabledStatus(token);
    return json(result);
  } catch (error) {
    console.error('Error toggling community sharing status:', error);
    return json({ error: 'Failed to toggle community sharing status' }, { status: 500 });
  }
};
