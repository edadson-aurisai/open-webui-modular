import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import * as authService from '../services';

// POST /api/auth/login - Login user
export const POST: RequestHandler = async ({ request, locals }) => {
  try {
    // For form data
    const contentType = request.headers.get('content-type') || '';
    let credentials;
    
    if (contentType.includes('application/x-www-form-urlencoded')) {
      const formData = await request.formData();
      credentials = {
        username: formData.get('username') as string,
        password: formData.get('password') as string
      };
    } else {
      // For JSON
      credentials = await request.json();
    }
    
    const result = await authService.login(credentials);
    return json(result);
  } catch (error) {
    console.error('Error logging in:', error);
    return json({ error: 'Failed to login' }, { status: 401 });
  }
};
