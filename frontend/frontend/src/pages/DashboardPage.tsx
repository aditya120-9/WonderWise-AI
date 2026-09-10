import { Settings2 } from "lucide-react";
import Header from "../components/layout/Header";
import SuggestedPrompts from "../components/chat/SuggestedPrompts";
import WelcomeScreen from "../components/chat/WelcomeScreen";

interface Props {
  onStartChat: (prompt?: string) => void;
}

const planningPrompts = [
  ["Plan a trip", "Help me plan a trip with flights, hotels, and activities."],
  ["Travel itinerary", "Create a travel itinerary for a 5-day visit."],
  ["Book hotels", "Find the best hotel options in a popular destination."],
  ["Bali getaway", "Tell me about Bali travel options."],
  ["Weekend trip ideas", "Give me ideas for a weekend trip."],
  ["Budget planner", "Help me plan a budget travel experience."],
] as const;

export default function DashboardPage({ onStartChat }: Props) {
  return (
    <div className="min-h-screen bg-slate-100 text-slate-900">
      <main className="mx-auto grid min-h-screen max-w-[1700px] gap-6 px-4 py-5 xl:grid-cols-[320px_1fr]">
        <aside className="space-y-5">
          <div className="rounded-[32px] border border-slate-200 bg-white p-5 shadow-sm">
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="text-xs uppercase tracking-[0.35em] text-slate-500">WonderWise AI</p>
                <h1 className="mt-3 text-2xl font-semibold text-slate-900">Travel Assistant</h1>
              </div>
              <button
                type="button"
                onClick={() => onStartChat()}
                className="rounded-2xl bg-slate-100 px-3 py-2 text-xs font-semibold uppercase tracking-[0.28em] text-slate-700 transition hover:bg-slate-200"
              >
                New Chat
              </button>
            </div>

            <div className="mt-7 space-y-3">
              {planningPrompts.slice(0, 3).map(([label, prompt]) => (
                <button key={label} type="button" onClick={() => onStartChat(prompt)} className="w-full rounded-3xl border border-slate-200 bg-slate-50 px-4 py-4 text-left text-sm font-semibold text-slate-900 transition hover:border-blue-500">
                  {label}
                </button>
              ))}
            </div>
          </div>

          <div className="rounded-[32px] border border-slate-200 bg-white p-5 shadow-sm">
            <div className="flex items-center justify-between gap-4">
              <div>
                <p className="text-xs uppercase tracking-[0.35em] text-slate-500">Recent chats</p>
                <p className="mt-2 text-sm text-slate-500">Access your latest conversations quickly.</p>
              </div>
              <Settings2 className="text-slate-400" size={18} />
            </div>

            <div className="mt-5 space-y-3">
              {planningPrompts.slice(3).map(([label, prompt]) => (
                <button key={label} type="button" onClick={() => onStartChat(prompt)} className="w-full rounded-3xl border border-slate-200 bg-slate-50 px-4 py-4 text-left text-sm text-slate-700 transition hover:border-slate-300">
                  {label}
                </button>
              ))}
            </div>
          </div>

          <div className="rounded-[32px] border border-slate-200 bg-white p-5 shadow-sm">
            <p className="text-xs uppercase tracking-[0.35em] text-slate-500">Tips</p>
            <p className="mt-3 text-sm leading-6 text-slate-600">
              Use the chatbot to discover destinations, compare travel options, and get personalized itineraries.
            </p>
          </div>
        </aside>

        <section className="space-y-6">
          <Header />

          <div className="grid gap-5 xl:grid-cols-[1.5fr_1fr]">
            <WelcomeScreen />

            <div className="rounded-[32px] border border-slate-200 bg-white p-5 shadow-sm">
              <div>
                <p className="text-xs uppercase tracking-[0.35em] text-slate-500">Popular actions</p>
                <h2 className="mt-3 text-2xl font-semibold text-slate-900">Start planning in seconds</h2>
                <p className="mt-2 text-sm text-slate-500">Tap one of the travel prompts or start a new chat to begin.</p>
              </div>
              <div className="mt-5">
                <SuggestedPrompts onSelect={(prompt) => onStartChat(prompt)} />
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
