import { ChatSocket } from "./websocket";

const socket = new ChatSocket();
const conversationId = Date.now() + Math.floor(Math.random() * 1000);

export function connectChat(
  onMessage: (data: any) => void,
  onClose?: () => void // <-- FIX: Add onClose as an optional parameter here
) {
  socket.connect(
    onMessage,
    onClose
  );
}

export function sendMessage(message: string, requestId?: string) {
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
