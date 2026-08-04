"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

const BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export default function LoginPage() {
  const router = useRouter();
  const [mode, setMode] = useState<"login" | "register">("login");
  const [email, setEmail] = useState("");
  const [fullName, setFullName] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit(e: React.FormEvent) {
    e.preventDefault(); setLoading(true); setError("");
    try {
      const endpoint = mode === "login" ? "/auth/login" : "/auth/register";
      const body = mode === "login" ? { email, password } : { email, full_name: fullName, password };
      const res = await fetch(`${BASE}${endpoint}`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Failed");
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("user", JSON.stringify(data.user));
      router.push("/"); router.refresh();
    } catch (e) { setError(e instanceof Error ? e.message : "Failed"); }
    setLoading(false);
  }

  return (
    <main className="mx-auto max-w-sm p-6 mt-20">
      <h1 className="text-2xl font-semibold text-center">OpenSchoolOS</h1>
      <p className="text-sm text-neutral-500 text-center mt-1">{mode === "login" ? "Sign in" : "Create account"}</p>
      <form onSubmit={submit} className="mt-6 space-y-3">
        <label className="block text-sm"><span className="text-neutral-600">Email</span><input type="email" value={email} onChange={e => setEmail(e.target.value)} required className="mt-1 w-full rounded border p-2" /></label>
        {mode === "register" && <label className="block text-sm"><span className="text-neutral-600">Full Name</span><input type="text" value={fullName} onChange={e => setFullName(e.target.value)} required className="mt-1 w-full rounded border p-2" /></label>}
        <label className="block text-sm"><span className="text-neutral-600">Password</span><input type="password" value={password} onChange={e => setPassword(e.target.value)} required minLength={6} className="mt-1 w-full rounded border p-2" /></label>
        {error && <p className="text-sm text-red-700">{error}</p>}
        <button type="submit" disabled={loading} className="w-full rounded bg-neutral-900 px-3 py-2 text-sm text-white disabled:opacity-50">{loading ? "..." : mode === "login" ? "Sign In" : "Create Account"}</button>
      </form>
      <p className="mt-4 text-center text-sm text-neutral-500">
        {mode === "login" ? <><>No account?</> <button onClick={() => setMode("register")} className="text-neutral-900 underline">Register</button></> : <><>Have an account?</> <button onClick={() => setMode("login")} className="text-neutral-900 underline">Sign In</button></>}
      </p>
    </main>
  );
}
