import api from "./api";

export interface Conversation {
  id: number;
  title: string;
  created_at: string;
}

export async function createConversation(title = "New Conversation") {
  const { data } = await api.post<Conversation>("/conversations", { title });
  return data;
}

export async function listConversations() {
  const { data } = await api.get<Conversation[]>("/conversations");
  return data;
}