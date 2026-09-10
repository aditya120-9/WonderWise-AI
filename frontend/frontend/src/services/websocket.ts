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
  private connectionUrl = "";
  private messageHandler: ((data: WebSocketResponse) => void) | null = null;
  private closeHandler: (() => void) | undefined;

  connect(
    url: string,
    onMessage: (data: WebSocketResponse) => void,
    onClose?: () => void
  ) {
    this.connectionUrl = url;
    this.messageHandler = onMessage;
    this.closeHandler = onClose;
    // Prevent overlapping sockets during React StrictMode mount/unmount cycles.
    this.connectionToken += 1;
    const token = this.connectionToken;

    // Close any existing socket before creating a new one.
    try {
      this.socket?.close();
    } catch {
      // ignore
    }

    this.socket = new WebSocket(url);

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
    const socketUnavailable = !this.socket ||
      this.socket.readyState === WebSocket.CLOSING ||
      this.socket.readyState === WebSocket.CLOSED;
    if (socketUnavailable && this.connectionUrl && this.messageHandler) {
      this.socket = null;
      this.queue.push(message);
      this.connect(this.connectionUrl, this.messageHandler, this.closeHandler);
      return;
    }

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
    this.connectionUrl = "";
    this.messageHandler = null;
    this.closeHandler = undefined;
  }

  cancel() {
    this.connectionToken += 1;
    this.socket?.close();
    this.socket = null;
  }
}

