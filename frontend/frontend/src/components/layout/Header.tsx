import { Bot, Circle } from "lucide-react";

export default function Header() {
    return (
        <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-6 shadow-sm">
            <div>
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-2xl bg-blue-600 flex items-center justify-center text-white shadow-md">
                        <Bot size={18} />
                    </div>
                    <div>
                        <h2 className="text-lg font-bold text-slate-900">WonderWise AI</h2>
                        <p className="text-xs text-slate-500 mt-1">Your Intelligent Travel Companion</p>
                    </div>
                </div>
            </div>

            <div className="flex items-center gap-3">
                <span className="text-xs text-slate-500">Local AI • Ollama • Online</span>
                <div className="inline-flex items-center gap-2 rounded-full bg-slate-100 px-3 py-1 text-xs text-slate-700">
                    <Circle size={8} className="text-emerald-500" fill="currentColor" />
                    <span>Online</span>
                </div>
            </div>
        </header>
    );
}