import { WEBUI_API_BASE_URL } from '$lib/constants';
import type { 
  User, 
  UserCreateRequest, 
  UserUpdateRequest, 
  UserResponse, 
  UsersListResponse,
  LoginRequest,
  LoginResponse,
  RegisterRequest,
  RegisterResponse
} from './types';

/**
 * Get all users
 */
export async function getUsers(
  token: string,
  page: number = 1,
  limit: number = 20
): Promise<UsersListResponse> {
  const searchParams = new URLSearchParams();
  searchParams.append('page', page.toString());
  searchParams.append('limit', limit.toString());

  const response = await fetch(`${WEBUI_API_BASE_URL}/users?${searchParams.toString()}`, {
    method: 'GET',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      authorization: `Bearer ${token}`
    }
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }

  return response.json();
}

/**
 * Get user by ID
 */
export async function getUserById(token: string, id: string): Promise<UserResponse> {
  const response = await fetch(`${WEBUI_API_BASE_URL}/users/${id}`, {
    method: 'GET',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      authorization: `Bearer ${token}`
    }
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }

  return response.json();
}

/**
 * Create a new user
 */
export async function createUser(token: string, user: UserCreateRequest): Promise<UserResponse> {
  const response = await fetch(`${WEBUI_API_BASE_URL}/users`, {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      authorization: `Bearer ${token}`
    },
    body: JSON.stringify(user)
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }

  return response.json();
}

/**
 * Update a user
 */
export async function updateUser(
  token: string,
  id: string,
  user: UserUpdateRequest
): Promise<UserResponse> {
  const response = await fetch(`${WEBUI_API_BASE_URL}/users/${id}`, {
    method: 'PUT',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      authorization: `Bearer ${token}`
    },
    body: JSON.stringify(user)
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }

  return response.json();
}

/**
 * Delete a user
 */
export async function deleteUser(token: string, id: string): Promise<void> {
  const response = await fetch(`${WEBUI_API_BASE_URL}/users/${id}`, {
    method: 'DELETE',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      authorization: `Bearer ${token}`
    }
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }
}

/**
 * Get current user
 */
export async function getCurrentUser(token: string): Promise<UserResponse> {
  const response = await fetch(`${WEBUI_API_BASE_URL}/users/me`, {
    method: 'GET',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      authorization: `Bearer ${token}`
    }
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }

  return response.json();
}

/**
 * Login user
 */
export async function login(credentials: LoginRequest): Promise<LoginResponse> {
  const formData = new URLSearchParams();
  formData.append('username', credentials.username);
  formData.append('password', credentials.password);

  const response = await fetch(`${WEBUI_API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: formData
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }

  return response.json();
}

/**
 * Register user
 */
export async function register(user: RegisterRequest): Promise<RegisterResponse> {
  const response = await fetch(`${WEBUI_API_BASE_URL}/auth/register`, {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(user)
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }

  return response.json();
}
