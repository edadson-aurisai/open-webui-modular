// Files API Types

export interface FileInfo {
  id: string;
  filename: string;
  collection_name: string;
  created_at: string;
  size?: number;
  mime_type?: string;
  user_id?: string;
}

export interface FileUploadResponse {
  id: string;
  filename: string;
  document_ids: string[];
}

export interface FileListResponse {
  files: FileInfo[];
}

export interface FileDeleteResponse {
  success: boolean;
}
