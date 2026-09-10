import { useState } from "react";
import type { FormEvent } from "react";
import axios from "axios";
import { LogIn, UserPlus } from "lucide-react";
import { authenticate } from "../services/auth";

interface Props {
  onAuthenticated: (email: string) => void;
}

export default function AuthPage({ onAuthenticated }: Props) {
  const [mode, setMode] = useState<"login" | "register">("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit(event: FormEvent) {
    event.preventDefault();
    setError("");
    setLoading(true);
    try {
      const user = await authenticate(mode, email, password);
      onAuthenticated(user.email);
    } catch (requestError: unknown) {
      if (axios.isAxiosError(requestError)) {
        setError(requestError.response?.data?.detail ?? "Unable to complete authentication");
      } else {
        setError("Unable to complete authentication");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-100 px-4">
      <section className="w-full max-w-md rounded-3xl border border-slate-200 bg-white p-8 shadow-xl">
        <div className="mb-8 flex items-center gap-3">
          <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-blue-600 text-xl text-white">🌍</div>
          <div>
            <h1 className="text-2xl font-bold text-slate-900">WonderWise AI</h1>
            <p className="text-sm text-slate-500">Your private travel companion</p>
          </div>
        </div>
        <h2 className="text-xl font-semibold text-slate-900">{mode === "login" ? "Welcome back" : "Create your account"}</h2>
        <p className="mt-2 text-sm text-slate-500">Your conversations are saved to your account.</p>
        <form className="mt-6 space-y-4" onSubmit={submit}>
          <input className="w-full rounded-xl border border-slate-200 px-4 py-3 outline-none focus:border-blue-500" type="email" required placeholder="Email address" value={email} onChange={(event) => setEmail(event.target.value)} />
          <input className="w-full rounded-xl border border-slate-200 px-4 py-3 outline-none focus:border-blue-500" type="password" required minLength={8} placeholder="Password (8+ characters)" value={password} onChange={(event) => setPassword(event.target.value)} />
          {error && <p className="text-sm text-red-600">{error}</p>}
          <button className="flex w-full items-center justify-center gap-2 rounded-xl bg-blue-600 py-3 font-semibold text-white transition hover:bg-blue-700 disabled:bg-slate-400" disabled={loading}>
            {mode === "login" ? <LogIn size={17} /> : <UserPlus size={17} />}
            {loading ? "Please wait..." : mode === "login" ? "Sign in" : "Create account"}
          </button>
        </form>
        <button className="mt-5 w-full text-sm text-slate-500 hover:text-blue-600" onClick={() => setMode(mode === "login" ? "register" : "login")}>
          {mode === "login" ? "Need an account? Register" : "Already have an account? Sign in"}
        </button>
      </section>
    </main>
  );
}