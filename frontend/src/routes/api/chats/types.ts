// Chat API Types

export interface Chat {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
  user_id: string;
  pinned: boolean;
  folder_id?: string;
  tags?: string[];
  share_id?: string;
  archived?: boolean;
}

export interface ChatCreateRequest {
  chat: {
    title?: string;
    messages?: any[];
    models?: any[];
    system?: string;
    tags?: string[];
  };
}

export interface ChatCreateResponse {
  id: string;
}

export interface ChatUpdateRequest {
  chat: Partial<Chat>;
}

export interface ChatListResponse {
  chats: Chat[];
}

export interface TagResponse {
  name: string;
  count: number;
}

export interface TagsResponse {
  tags: TagResponse[];
}
