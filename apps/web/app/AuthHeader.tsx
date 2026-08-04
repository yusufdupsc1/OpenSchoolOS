"use client";

import { useState, useEffect } from "react";
import Link from "next/link";

export default function AuthHeader() {
  const [user, setUser] = useState<{ full_name: string } | null>(null);

  useEffect(() => {
    const stored = localStorage.getItem("user");
    if (stored) setUser(JSON.parse(stored));
  }, []);

  function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    setUser(null);
    window.location.href = "/";
  }

  if (!user) {
    return <Link href="/login" className="text-neutral-500 hover:underline">Sign In</Link>;
  }

  return (
    <span className="flex items-center gap-3">
      <span className="text-neutral-400 text-xs">{user.full_name}</span>
      <button onClick={logout} className="text-neutral-400 hover:text-red-600 text-xs">Sign Out</button>
    </span>
  );
}
