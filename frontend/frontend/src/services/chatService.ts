import { ChatSocket } from "./websocket";
import type { WebSocketResponse } from "./websocket";

const socket = new ChatSocket();

export function connectChat(
  onMessage: (data: WebSocketResponse) => void,
  onClose?: () => void
) {
  socket.connect(
    `${(import.meta.env.VITE_WS_URL ?? "ws://127.0.0.1:8000/ws/chat")}?token=${encodeURIComponent(localStorage.getItem("wonderwise_token") ?? "")}`,
    onMessage,
    onClose
  );
}

export function sendMessage(message: string, conversationId: number, requestId?: string) {
  const payload = JSON.stringify({
    message,
    conversation_id: conversationId,
    request_id: requestId,
  });

  socket.send(payload);
}

export function disconnectChat() {
  socket.disconnect();
}

export function stopChat() {
  socket.cancel();
}
