export interface WebSocketResponse {
  type: "chunk" | "end" | "error";
  content?: string;
  message?: string;
  request_id?: string | null;
}

export class ChatSocket {
  private socket: WebSocket | null = null;
  private queue: string[] = [];
  private connectionToken = 0;

  connect(
    onMessage: (data: WebSocketResponse) => void,
    onClose?: () => void
  ) {
    // Prevent overlapping sockets during React StrictMode mount/unmount cycles.
    this.connectionToken += 1;
    const token = this.connectionToken;

    // Close any existing socket before creating a new one.
    try {
      this.socket?.close();
    } catch {
      // ignore
    }

    this.socket = new WebSocket("ws://127.0.0.1:8000/ws/chat");

    this.socket.onopen = () => {
      // Only the latest active connection should flush the queue.
      if (token !== this.connectionToken) return;

      while (this.queue.length > 0) {
        const queuedMessage = this.queue.shift();
        if (queuedMessage && this.socket?.readyState === WebSocket.OPEN) {
          this.socket.send(queuedMessage);
        }
      }
    };

    this.socket.onmessage = (event) => {
      // Ignore messages from stale connections.
      if (token !== this.connectionToken) return;

      const data = JSON.parse(event.data);
      onMessage(data);
    };

    this.socket.onclose = () => {
      if (token !== this.connectionToken) return;
      onClose?.();
    };

    this.socket.onerror = () => {
      if (token !== this.connectionToken) return;
      console.error("WebSocket connection error");
    };
  }


  send(message: string) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(message);
      return;
    }

    if (this.socket) {
      this.queue.push(message);
    } else {
      console.warn("WebSocket is not connected yet. Message queued.");
      this.queue.push(message);
    }
  }

  disconnect() {
    // Invalidate current connection so any in-flight messages are ignored.
    this.connectionToken += 1;

    this.queue = [];
    if (this.socket) {
      this.socket.onopen = null;
      this.socket.onmessage = null;
      this.socket.onclose = null;
      this.socket.onerror = null;
    }
    this.socket?.close();
    this.socket = null;
  }
}

