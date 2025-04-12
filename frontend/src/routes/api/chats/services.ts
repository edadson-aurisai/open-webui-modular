import { WEBUI_API_BASE_URL } from '$lib/constants';
import type { Chat, ChatCreateRequest, ChatCreateResponse, TagsResponse } from './types';
import { getTimeRange } from '$lib/utils';

/**
 * Create a new chat
 */
export async function createChat(token: string, chat: ChatCreateRequest): Promise<ChatCreateResponse> {
  const response = await fetch(`${WEBUI_API_BASE_URL}/chats/new`, {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      authorization: `Bearer ${token}`
    },
    body: JSON.stringify({
      chat: chat
    })
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }

  return response.json();
}

/**
 * Get a list of chats
 */
export async function getChats(token: string, page: number | null = null): Promise<Chat[]> {
  const searchParams = new URLSearchParams();
  
  if (page !== null) {
    searchParams.append('page', `${page}`);
  }

  const response = await fetch(`${WEBUI_API_BASE_URL}/chats/?${searchParams.toString()}`, {
    method: 'GET',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      ...(token && { authorization: `Bearer ${token}` })
    }
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }

  const chats = await response.json();
  return chats.map((chat: Chat) => ({
    ...chat,
    time_range: getTimeRange(chat.updated_at)
  }));
}

/**
 * Get a chat by ID
 */
export async function getChatById(token: string, id: string): Promise<Chat> {
  const response = await fetch(`${WEBUI_API_BASE_URL}/chats/${id}`, {
    method: 'GET',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      ...(token && { authorization: `Bearer ${token}` })
    }
  });

  if (!response.ok) {
    const error = await response.json();
    throw error.detail || error;
  }

  return response.json();
}

/**
 * Update a chat by ID
 */
export async function updateChatById(token: string, id: string, chat: object): Promise<any> {
  const response = await fetch(`${WEBUI_API_BASE_URL}/chats/${id}`, {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      ...(token && { authorization: `Bearer ${token}` })
    },
    body: JSON.stringify({
      chat: chat
    })
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }

  return response.json();
}

/**
 * Delete a chat by ID
 */
export async function deleteChatById(token: string, id: string): Promise<any> {
  const response = await fetch(`${WEBUI_API_BASE_URL}/chats/${id}`, {
    method: 'DELETE',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      ...(token && { authorization: `Bearer ${token}` })
    }
  });

  if (!response.ok) {
    const error = await response.json();
    throw error.detail || error;
  }

  return response.json();
}

/**
 * Get all tags
 */
export async function getAllTags(token: string): Promise<TagsResponse> {
  const response = await fetch(`${WEBUI_API_BASE_URL}/chats/all/tags`, {
    method: 'GET',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      ...(token && { authorization: `Bearer ${token}` })
    }
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }

  return response.json();
}

/**
 * Get pinned chats
 */
export async function getPinnedChats(token: string): Promise<Chat[]> {
  const response = await fetch(`${WEBUI_API_BASE_URL}/chats/pinned`, {
    method: 'GET',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      ...(token && { authorization: `Bearer ${token}` })
    }
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }

  const chats = await response.json();
  return chats.map((chat: Chat) => ({
    ...chat,
    time_range: getTimeRange(chat.updated_at)
  }));
}

/**
 * Toggle chat pinned status
 */
export async function toggleChatPinned(token: string, id: string): Promise<any> {
  const response = await fetch(`${WEBUI_API_BASE_URL}/chats/${id}/pin`, {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      ...(token && { authorization: `Bearer ${token}` })
    }
  });

  if (!response.ok) {
    const error = await response.json();
    throw error.detail || error;
  }

  return response.json();
}

/**
 * Share a chat
 */
export async function shareChat(token: string, id: string): Promise<any> {
  const response = await fetch(`${WEBUI_API_BASE_URL}/chats/${id}/share`, {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      ...(token && { authorization: `Bearer ${token}` })
    }
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }

  return response.json();
}

/**
 * Get chat by share ID
 */
export async function getChatByShareId(token: string, shareId: string): Promise<Chat> {
  const response = await fetch(`${WEBUI_API_BASE_URL}/chats/share/${shareId}`, {
    method: 'GET',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      ...(token && { authorization: `Bearer ${token}` })
    }
  });

  if (!response.ok) {
    const error = await response.json();
    throw error;
  }

  return response.json();
}
