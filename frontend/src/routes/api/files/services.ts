import { WEBUI_API_BASE_URL } from '$lib/constants';
import type { FileInfo, FileUploadResponse, FileListResponse, FileDeleteResponse } from './types';

/**
 * Upload a file
 */
export async function uploadFile(
  token: string,
  file: File,
  collectionName?: string
): Promise<FileUploadResponse> {
  const formData = new FormData();
  formData.append('file', file);
  
  if (collectionName) {
    formData.append('collection_name', collectionName);
  }

  const response = await fetch(`${WEBUI_API_BASE_URL}/files/upload`, {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      authorization: `Bearer ${token}`
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
 * List files
 */
export async function listFiles(
  token: string,
  collectionName?: string
): Promise<FileListResponse> {
  const searchParams = new URLSearchParams();
  
  if (collectionName) {
    searchParams.append('collection_name', collectionName);
  }

  const response = await fetch(`${WEBUI_API_BASE_URL}/files/list?${searchParams.toString()}`, {
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
 * Delete a file
 */
export async function deleteFile(token: string, fileId: string): Promise<FileDeleteResponse> {
  const response = await fetch(`${WEBUI_API_BASE_URL}/files/${fileId}`, {
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

  return response.json();
}

/**
 * Get file by ID
 */
export async function getFileById(token: string, fileId: string): Promise<FileInfo> {
  const response = await fetch(`${WEBUI_API_BASE_URL}/files/${fileId}`, {
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
