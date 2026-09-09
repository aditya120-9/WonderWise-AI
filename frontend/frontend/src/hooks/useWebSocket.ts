import { useEffect, useRef } from "react";

import type { SocketMessage } from "../types/socket";

interface Props {
  onMessage: (message: SocketMessage) => void;
}

export function useWebSocket({ onMessage }: Props) {
  const socket = useRef<WebSocket | null>(null);

  useEffect(() => {
    socket.current = new WebSocket("ws://127.0.0.1:8000/ws/chat");

    socket.current.onmessage = (event) => {
      const message: SocketMessage = JSON.parse(event.data);
      onMessage(message);
    };

    return () => {
      socket.current?.close();
    };
  }, []);

  function send(data: object) {
    socket.current?.send(JSON.stringify(data));
  }

  return { send };
}
