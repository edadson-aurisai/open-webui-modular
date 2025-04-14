// Users API Types

export interface User {
  id: string;
  username: string;
  email: string;
  display_name?: string;
  avatar_url?: string;
  role: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
}

export interface UserCreateRequest {
  username: string;
  email: string;
  password: string;
  display_name?: string;
  role?: string;
}

export interface UserUpdateRequest {
  email?: string;
  display_name?: string;
  avatar_url?: string;
  password?: string;
  role?: string;
  is_active?: boolean;
}

export interface UserResponse {
  user: User;
}

export interface UsersListResponse {
  users: User[];
  total: number;
  page: number;
  limit: number;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  display_name?: string;
}

export interface RegisterResponse {
  access_token: string;
  token_type: string;
  user: User;
}
