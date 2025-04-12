import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import * as configService from '../config/services';

// GET /api/changelog - Get changelog
export const GET: RequestHandler = async ({ request, locals }) => {
  try {
    const changelog = await configService.getChangelog();
    return json(changelog);
  } catch (error) {
    console.error('Error fetching changelog:', error);
    return json({ error: 'Failed to fetch changelog' }, { status: 500 });
  }
};
