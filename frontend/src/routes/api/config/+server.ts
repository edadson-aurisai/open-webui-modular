import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import * as configService from './services';

// GET /api/config - Get backend configuration
export const GET: RequestHandler = async ({ request, locals }) => {
  try {
    const config = await configService.getBackendConfig();
    return json(config);
  } catch (error) {
    console.error('Error fetching backend config:', error);
    return json({ error: 'Failed to fetch backend config' }, { status: 500 });
  }
};
