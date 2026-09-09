import ReactMarkdown from "react-markdown";
import type { Message } from "../../types/chat";

interface Props {
  message: Message;
}

function formatTime(d: Date) {
  return d.toLocaleTimeString([], { hour: "numeric", minute: "2-digit" });
}

export default function MessageBubble({ message }: Props) {
  const isUser = message.role === "user";

  // Minimal timestamp (front-end only; message model doesn't carry a timestamp)
  const now = new Date();
  const time = formatTime(now);

  return (
    <div className={`w-full mb-4 ${isUser ? "flex justify-end" : "flex justify-start"}`}>
      <div className="max-w-3xl w-full">
        <div
          className={`flex items-center gap-3 ${
            isUser ? "justify-end" : "justify-start"
          }`}
        >
          {!isUser && (
            <div className="h-9 w-9 rounded-2xl bg-slate-900 text-white flex items-center justify-center">
              <span className="text-sm font-bold">W</span>
            </div>
          )}

          <div className="flex items-center gap-2">
            {isUser ? (
              <div className="h-9 w-9 rounded-2xl bg-slate-50 border border-slate-200 text-slate-700 flex items-center justify-center">
                <span className="text-sm font-semibold">U</span>
              </div>
            ) : null}

            <div className="text-right">
              <div className="text-xs text-slate-500">
                {isUser ? "Aditya" : "WonderWise AI"}{" "}
                <span className="text-slate-400">{time}</span>
              </div>
            </div>
          </div>
        </div>

        <div className={`mt-2 text-slate-700 leading-relaxed text-[15px] break-words overflow-x-auto ${isUser ? "text-right" : "text-left"}`}>
          <ReactMarkdown
            components={{
              p: ({ children }) => <p className="mb-3 last:mb-0 leading-7 text-[15px] text-slate-700">{children}</p>,
              ul: ({ children }) => <ul className="list-disc pl-5 my-3 space-y-2 text-left">{children}</ul>,
              ol: ({ children }) => <ol className="list-decimal pl-5 my-3 space-y-2 text-left">{children}</ol>,
              li: ({ children }) => <li className="leading-7 text-slate-700">{children}</li>,
              strong: ({ children }) => <strong className="font-semibold text-slate-900">{children}</strong>,
              em: ({ children }) => <em className="italic text-slate-600">{children}</em>,
              a: ({ href, children }) => (
                <a href={href} className="text-blue-600 underline underline-offset-2" target="_blank" rel="noreferrer">
                  {children}
                </a>
              ),
              h1: ({ children }) => <h1 className="text-lg font-semibold text-slate-900 mt-4 mb-2">{children}</h1>,
              h2: ({ children }) => <h2 className="text-base font-semibold text-slate-900 mt-4 mb-2">{children}</h2>,
              h3: ({ children }) => <h3 className="text-sm font-semibold text-slate-900 mt-3 mb-1">{children}</h3>,
              hr: () => <hr className="my-4 border-slate-200" />,
              blockquote: ({ children }) => (
                <blockquote className="border-l-2 border-slate-300 pl-3 my-3 italic text-slate-600">
                  {children}
                </blockquote>
              ),
            }}
          >
            {message.content}
          </ReactMarkdown>
        </div>
      </div>
    </div>
  );
}
