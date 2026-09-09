interface Props {
  value: string;
  onChange: (value: string) => void;
  onSend: () => void;
  loading: boolean;
}

export default function ChatInput({ value, onChange, onSend, loading }: Props) {
  return (
    <div className="bg-white border-t border-slate-200 px-4 py-4 shadow-sm">
      <div className="max-w-[1500px] mx-auto flex flex-col gap-3 sm:flex-row items-center">
        <input
          className="flex-1 min-w-0 rounded-3xl border border-slate-200 bg-slate-50 px-5 py-4 text-slate-900 outline-none transition focus:border-blue-500 focus:bg-white"
          placeholder="Ask anything about your journey..."
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !loading) {
              onSend();
            }
          }}
          disabled={loading}
        />
        <button
          onClick={onSend}
          disabled={loading}
          className="inline-flex h-14 items-center justify-center rounded-3xl bg-blue-600 px-8 text-sm font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-slate-400"
        >
          {loading ? "Thinking..." : "Send"}
        </button>
      </div>
    </div>
  );
}