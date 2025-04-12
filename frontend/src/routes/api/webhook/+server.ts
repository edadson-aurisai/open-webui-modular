import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import * as configService from '../config/services';

// GET /api/webhook - Get webhook URL
export const GET: RequestHandler = async ({ request, locals }) => {
  try {
    const token = request.headers.get('authorization')?.split(' ')[1] || '';
    
    const config = await configService.getWebhookUrl(token);
    return json(config);
  } catch (error) {
    console.error('Error fetching webhook URL:', error);
    return json({ error: 'Failed to fetch webhook URL' }, { status: 500 });
  }
};

// POST /api/webhook - Update webhook URL
export const POST: RequestHandler = async ({ request, locals }) => {
  try {
    const token = request.headers.get('authorization')?.split(' ')[1] || '';
    const data = await request.json();
    
    const result = await configService.updateWebhookUrl(token, data.url);
    return json(result);
  } catch (error) {
    console.error('Error updating webhook URL:', error);
    return json({ error: 'Failed to update webhook URL' }, { status: 500 });
  }
};
