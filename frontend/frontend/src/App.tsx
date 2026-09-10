import { lazy, Suspense, useState } from "react";
const DashboardPage = lazy(() => import("./pages/DashboardPage"));
const ChatPage = lazy(() => import("./pages/ChatPage"));
const AuthPage = lazy(() => import("./pages/AuthPage"));
import { getStoredUser, logout } from "./services/auth";

import AppShell from "./components/layout/AppShell";

function App() {
  const [userEmail, setUserEmail] = useState(() => getStoredUser()?.email ?? "");
  const [activePage, setActivePage] = useState<"dashboard" | "chat">("dashboard");
  const [initialPrompt, setInitialPrompt] = useState("");
  const [selectedConversationId, setSelectedConversationId] = useState<number | null>(null);

  function handleStartChat(prompt?: string) {
    if (prompt) {
      setInitialPrompt(prompt);
    } else {
      setInitialPrompt("");
    }
    setSelectedConversationId(null);
    setActivePage("chat");
  }

  function handleSelectConversation(conversationId: number) {
    setSelectedConversationId(conversationId);
    setInitialPrompt("");
    setActivePage("chat");
  }

  function handleLogout() {
    logout();
    setUserEmail("");
  }

  if (!userEmail) {
    return (
      <Suspense fallback={<div className="flex min-h-screen items-center justify-center bg-slate-100 text-slate-500">Loading...</div>}>
        <AuthPage onAuthenticated={setUserEmail} />
      </Suspense>
    );
  }

  return (
    <Suspense fallback={<div className="flex min-h-screen items-center justify-center bg-slate-100 text-slate-500">Loading...</div>}>
      <AppShell
        onNewChat={() => handleStartChat(undefined)}
        onSelectConversation={handleSelectConversation}
        onLogout={handleLogout}
        userEmail={userEmail}
      >
        {activePage === "dashboard" ? (
          <DashboardPage onStartChat={handleStartChat} />
        ) : (
          <ChatPage initialPrompt={initialPrompt} existingConversationId={selectedConversationId} onBack={() => setActivePage("dashboard")} />
        )}
      </AppShell>
    </Suspense>
  );
}

export default App;
