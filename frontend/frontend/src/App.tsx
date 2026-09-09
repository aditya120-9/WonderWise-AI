import { useState } from "react";
import DashboardPage from "./pages/DashboardPage";
import ChatPage from "./pages/ChatPage";

import AppShell from "./components/layout/AppShell";

function App() {

  const [activePage, setActivePage] = useState<"dashboard" | "chat">("dashboard");
  const [initialPrompt, setInitialPrompt] = useState("");

  function handleStartChat(prompt?: string) {
    if (prompt) {
      setInitialPrompt(prompt);
    } else {
      setInitialPrompt("");
    }
    setActivePage("chat");
  }

  return (
    <AppShell onNewChat={() => handleStartChat(undefined)}>
      {activePage === "dashboard" ? (
        <DashboardPage onStartChat={handleStartChat} />
      ) : (
        <ChatPage initialPrompt={initialPrompt} onBack={() => setActivePage("dashboard")} />
      )}
    </AppShell>
  );
}

export default App;
