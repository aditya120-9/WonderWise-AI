import { useEffect, useRef, useState } from "react";
import {
  connectChat,
  disconnectChat,
  stopChat,
  sendMessage as send,
} from "../services/chatService";
import type { Message } from "../types/chat";

function sanitizeChunk(chunk: string) {
  // Ollama chunks can split in the middle of a word, so preserve boundaries.
  return chunk.replace(/\r\n/g, "\n");
}

export function useChat(conversationId: number | null) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  const activeRequestIdRef = useRef<string | null>(null);

  const lastChunkByRequestRef = useRef<Map<string, string>>(new Map());
  const requestTextAccumulatorRef = useRef<Map<string, string>>(new Map());

  useEffect(() => {
    if (conversationId === null) return;

    connectChat((data) => {
      if (data.type === "end") {
        if (!data.request_id || data.request_id === activeRequestIdRef.current) {
          setLoading(false);
        }
        return;
      }

      if (data.type === "chunk") {
        const requestId = data.request_id ?? "";
        const content = sanitizeChunk(data.content ?? "");

        // If backend doesn't send request_id yet, append as before.
        if (!requestId) {
          setMessages((prev) => {
            const last = prev[prev.length - 1];
            if (last && last.role === "assistant") {
              const previousText = last.content;
              const nextText = previousText + content;
              if (previousText === nextText) {
                return prev;
              }
              return [
                ...prev.slice(0, -1),
                { ...last, content: nextText },
              ];
            }
            return prev;
          });
          return;
        }

        // Ignore chunks that don't belong to the currently active request
        if (activeRequestIdRef.current && requestId !== activeRequestIdRef.current) {
          return;
        }

        if (lastChunkByRequestRef.current.get(requestId) === content) {
          return;
        }
        lastChunkByRequestRef.current.set(requestId, content);

        const currentAccumulated = requestTextAccumulatorRef.current.get(requestId) ?? "";
        const nextFull = currentAccumulated + content;
        requestTextAccumulatorRef.current.set(requestId, nextFull);

        setMessages((prev) => {
          const last = prev[prev.length - 1];

          if (last && last.role === "assistant") {
            return [
              ...prev.slice(0, -1),
              { ...last, content: nextFull },
            ];
          }

          return prev;
        });

        return;
      }


      if (data.type === "error") {
        setLoading(false);
        console.error("Chat Error:", data.message);
      }
    });

    return () => {
      disconnectChat();
    };
  }, [conversationId]);

  function sendMessage(text: string) {
    if (!text.trim()) return;

    const requestId = `${Date.now()}-${Math.random().toString(16).slice(2)}`;
    activeRequestIdRef.current = requestId;
    lastChunkByRequestRef.current.clear();
    requestTextAccumulatorRef.current.clear();

    setMessages((prev) => [
      ...prev,
      {
        id: Date.now(),
        role: "user",
        content: text,
      },
      {
        id: Date.now() + 1,
        role: "assistant",
        content: "",
      },
    ]);

    setLoading(true);
    if (conversationId !== null) send(text, conversationId, requestId);
  }

  function resetChat() {
    setMessages([]);
    setLoading(false);
    activeRequestIdRef.current = null;
    lastChunkByRequestRef.current.clear();
    requestTextAccumulatorRef.current.clear();
  }

  function stopGeneration() {
    stopChat();
    setLoading(false);
  }

  return {
    messages,
    loading,
    sendMessage,
    stopGeneration,
    resetChat,
  };
}

