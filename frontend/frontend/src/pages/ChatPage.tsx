import { useEffect, useState } from "react";
import { ArrowLeft, Car, Compass, Hotel, Plane, Train, Wallet } from "lucide-react";
import Header from "../components/layout/Header";
import ChatWindow from "../components/chat/ChatWindow";
import ChatInput from "../components/chat/chatInput";


import { useChat } from "../hooks/useChat";
import { createConversation } from "../services/conversations";

const travelActions = [
  ["Find Flights", "Best prices today", "Help me find the cheapest flights for my next trip", Plane],
  ["Hotels", "Curated stays", "Show me hotel options with great reviews and value", Hotel],
  ["Train Booking", "Fastest routes", "Find the best train routes and schedules for my journey", Train],
  ["Cab Booking", "Airport & city rides", "Recommend the best cab options for airport and city travel", Car],
  ["Explore Places", "Hidden gems", "Suggest interesting travel destinations I should explore", Compass],
  ["Budget Planner", "Smart itineraries", "Create a budget travel plan for my next vacation", Wallet],
] as const;

interface Props {
  initialPrompt?: string;
  onBack: () => void;
  existingConversationId?: number | null;
}

export default function ChatPage({ initialPrompt = "", onBack, existingConversationId = null }: Props) {
  const [conversationId, setConversationId] = useState<number | null>(existingConversationId);
  const { messages, loading, sendMessage, stopGeneration } = useChat(conversationId);
  const [inputValue, setInputValue] = useState("");

  useEffect(() => {
    if (initialPrompt) {
      setInputValue(initialPrompt);
    }
  }, [initialPrompt]);

  useEffect(() => {
    if (existingConversationId !== null) return;
    let active = true;
    createConversation()
      .then((conversation) => {
        if (active) setConversationId(conversation.id);
      })
      .catch(() => onBack());
    return () => {
      active = false;
    };
  }, [existingConversationId, onBack]);

  function handleSend() {
    if (!inputValue.trim()) return;
    sendMessage(inputValue.trim());
    setInputValue("");
  }

  const isActiveChat = messages.length > 0 || loading;

  return (
    <div className="min-h-screen bg-slate-100 text-slate-900">
      <main className="mx-auto flex min-h-screen max-w-[1400px] flex-col gap-6 px-4 py-5">
        <div
          className={`flex items-center justify-between gap-4 rounded-[32px] border border-slate-200 bg-white p-5 shadow-sm transition-opacity ${
            isActiveChat ? "opacity-0 pointer-events-none" : "opacity-100"
          }`}
        >
          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={onBack}
              className="inline-flex h-11 w-11 items-center justify-center rounded-2xl border border-slate-200 bg-slate-50 text-slate-700 transition hover:bg-slate-100"
            >
              <ArrowLeft size={20} />
            </button>
            <div>
              <p className="text-xs uppercase tracking-[0.35em] text-slate-500">WonderWise AI</p>
              <h1 className="mt-2 text-2xl font-semibold text-slate-900">New conversation</h1>
            </div>
          </div>
          <Header />
        </div>

        <section className="grid gap-6 xl:grid-cols-1">
          <div className="flex flex-col gap-6 rounded-[32px] border border-slate-200 bg-white p-5 shadow-sm">
            {isActiveChat ? (
              <div className="min-h-[520px] overflow-hidden rounded-[28px] border border-slate-200 bg-slate-50 p-5">
                <ChatWindow messages={messages} />
              </div>
            ) : (
              <div className="relative min-h-[680px] overflow-hidden rounded-[28px] border border-slate-200 bg-white">
                <div className="absolute inset-0">
                  <div className="flex h-full w-full flex-col items-center justify-center px-6">
                    <div className="text-center">
                      <div className="text-sm uppercase tracking-[0.35em] text-slate-500">Good evening,</div>
                      <h2 className="mt-2 text-4xl font-semibold text-slate-900">
                        <span className="text-blue-600">Aditya</span>
                      </h2>
                      <p className="mt-3 text-[16px] text-slate-700">Where would you like to go?</p>
                    </div>

                    <div className="mt-10 w-full max-w-4xl">
                      <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
                        {travelActions.map(([title, subtitle, prompt, Icon]) => (
                          <button
                            key={title}
                            type="button"
                            onClick={() => setInputValue(prompt)}
                            className="rounded-2xl border border-gray-200 bg-white p-4 text-left shadow-sm transition-all hover:shadow-md hover:scale-[1.01]"
                          >
                            <div className="flex items-center gap-4">
                              <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-blue-100 text-blue-600">
                                <Icon size={21} aria-hidden="true" />
                              </div>
                              <div>
                                <div className="text-[15px] font-semibold text-slate-900">{title}</div>
                                <div className="mt-1 text-sm text-slate-500">{subtitle}</div>
                              </div>
                            </div>
                          </button>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Floating input for New Chat */}
                <div className="pointer-events-auto absolute bottom-6 left-1/2 w-[min(1100px,calc(100vw-2rem))] -translate-x-1/2">
                  <div className="rounded-full border border-slate-200 bg-white shadow-md">
                    <div className="flex items-center gap-3 px-4 py-3">
                      <div className="flex flex-1 items-center gap-3">
                        <input
                          className="w-full bg-transparent px-2 py-2 text-slate-900 outline-none"
                          placeholder="Ask anything about your journey..."
                          value={inputValue}
                          onChange={(e) => setInputValue(e.target.value)}
                          onKeyDown={(e) => {
                            if (e.key === "Enter" && !loading) handleSend();
                          }}
                          disabled={loading}
                        />
                      </div>

                      <div className="flex items-center gap-2">
                        <button
                          type="button"
                          onClick={handleSend}
                          disabled={loading}
                          className="inline-flex h-11 w-11 items-center justify-center rounded-full bg-blue-600 text-white shadow-sm hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-slate-400"
                          aria-label="Send"
                        >
                          ⤴
                        </button>
                      </div>
                    </div>
                  </div>
                  <div className="mt-2 text-center text-xs text-slate-400">
                    WonderWise will use your message to generate a response.
                  </div>
                </div>
              </div>
            )}
          </div>
        </section>

        {/* Floating fixed input for active chat */}
        <div
          className={`fixed left-1/2 bottom-6 z-30 w-[min(1400px,calc(100vw-2rem))] -translate-x-1/2 ${
            isActiveChat ? "opacity-100" : "opacity-0 pointer-events-none"
          } transition-opacity`}
        >
          <ChatInput value={inputValue} onChange={setInputValue} onSend={handleSend} onStop={stopGeneration} loading={loading} />
        </div>
      </main>
    </div>
  );
}
