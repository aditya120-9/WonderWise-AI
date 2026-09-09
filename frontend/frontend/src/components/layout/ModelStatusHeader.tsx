import { Circle } from "lucide-react";

export default function ModelStatusHeader() {
  return (
    <header className="h-16 bg-white border-b border-[#e5e7eb] flex items-center justify-end px-6">
      <div className="text-xs text-slate-500">
        <span className="inline-flex items-center gap-2">
          <Circle size={8} className="text-emerald-500" fill="currentColor" />
          <span className="whitespace-nowrap">Local AI • Ollama • Online</span>
        </span>
      </div>
    </header>
  );
}

