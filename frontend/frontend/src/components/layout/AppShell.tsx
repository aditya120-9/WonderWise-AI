import type { ReactNode } from "react";
import Sidebar from "./Sidebar";
import ModelStatusHeader from "./ModelStatusHeader";

interface Props {
  children: ReactNode;
  onNewChat: () => void;
}

export default function AppShell({ children, onNewChat }: Props) {
  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar onNewChat={onNewChat} />

      <div className="flex min-w-0 flex-1 flex-col pl-[280px]">
        <ModelStatusHeader />

        <div className="min-w-0 flex-1 overflow-y-auto pt-0">
          <div className="mx-auto w-full max-w-[1400px] px-6 py-6">
            {children}
          </div>
        </div>
      </div>
    </div>
  );
}

