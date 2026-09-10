import { Cpu, History, LogOut, Plus } from "lucide-react";
import { motion } from "framer-motion";
import { useEffect, useState } from "react";
import { listConversations, type Conversation } from "../../services/conversations";


interface Props {
  onNewChat: () => void;
  onSelectConversation: (conversationId: number) => void;
  onLogout: () => void;
  userEmail: string;
}

export default function Sidebar({ onNewChat, onSelectConversation, onLogout, userEmail }: Props) {
  const [recentChats, setRecentChats] = useState<Conversation[]>([]);

  useEffect(() => {
    listConversations().then(setRecentChats).catch(() => setRecentChats([]));
  }, []);

  return (
    <motion.aside
      initial={{ x: -30, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      transition={{ duration: 0.4 }}
      className="fixed left-0 top-0 z-20 h-screen w-[280px] bg-white border-r border-[#e5e7eb] flex flex-col"
    >
      <div className="p-5">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-2xl bg-blue-600 flex items-center justify-center text-white text-xl">
            🌍
          </div>
          <div>
            <h1 className="font-bold text-xl">WonderWise</h1>
            <p className="text-gray-500 text-sm">AI Travel Assistant</p>
          </div>
        </div>

        <button
          onClick={onNewChat}
          className="mt-4 w-full rounded-xl bg-blue-600 py-2 text-white flex items-center justify-center gap-2 transition hover:bg-blue-700 text-sm"
        >
          <Plus size={16} />
          New Chat
        </button>
      </div>

      <div className="px-6 pt-1">
        <p className="flex items-center gap-2 font-semibold mb-4 text-xs uppercase tracking-[0.35em] text-slate-500">
          <History size={16} />
          Recent Chats
        </p>

        <div className="space-y-1">
          {recentChats.map((chat) => (
            <button
              key={chat.id}
              type="button"
              onClick={() => onSelectConversation(chat.id)}
              className="w-full rounded-lg px-2 py-2 text-sm text-slate-700 hover:bg-slate-100 transition text-left"
            >
              <span className="inline-flex items-center gap-2">
                <span aria-hidden="true">💬</span>
                {chat.title}
              </span>
            </button>
          ))}
          {recentChats.length === 0 && <p className="px-2 text-sm text-slate-400">No saved conversations yet.</p>}
        </div>
      </div>

      <div className="mt-auto p-4">
        <div className="mt-4 flex items-center justify-between gap-3 rounded-lg border border-slate-200 p-3">
          <span className="min-w-0 truncate text-xs text-slate-600">{userEmail}</span>
          <button type="button" onClick={onLogout} className="text-slate-500 hover:text-red-600" aria-label="Sign out">
            <LogOut size={16} />
          </button>
        </div>

        <div className="mt-4 rounded-lg bg-slate-100 p-3">
          <div className="flex items-center gap-2">
            <Cpu size={18} />
            <span className="text-sm font-medium text-slate-800">Qwen2.5 3B</span>
          </div>
          <p className="text-sm text-gray-500 mt-2">Running Locally</p>
        </div>
      </div>
    </motion.aside>
  );
}

