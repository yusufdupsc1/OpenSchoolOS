"use client";

import { useState, useRef } from "react";
import { useRouter } from "next/navigation";
import { api } from "../lib/api";

export default function BulkImport() {
  const router = useRouter();
  const fileRef = useRef<HTMLInputElement>(null);
  const [result, setResult] = useState<{ created: number; errors: string[] } | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleUpload(e: React.FormEvent) {
    e.preventDefault();
    const file = fileRef.current?.files?.[0];
    if (!file) return;
    setLoading(true);
    setResult(null);
    try {
      const r = await api.importStudents(file);
      setResult(r);
      router.refresh();
    } catch (err) {
      setResult({ created: 0, errors: [err instanceof Error ? err.message : "Upload failed"] });
    }
    setLoading(false);
  }

  return (
    <div className="mt-6 rounded border p-4">
      <h2 className="font-semibold">Import Students (CSV)</h2>
      <p className="text-xs text-neutral-500 mt-1 mb-3">Columns: full_name, roll_number, grade, section</p>
      <form onSubmit={handleUpload} className="flex gap-2">
        <input ref={fileRef} type="file" accept=".csv" className="flex-1 text-sm" />
        <button type="submit" disabled={loading} className="rounded bg-neutral-900 px-3 py-2 text-sm text-white disabled:opacity-50">{loading ? "Importing..." : "Upload"}</button>
      </form>
      {result && (
        <div className="mt-3 text-sm">
          <p className="text-green-700">{result.created} students imported.</p>
          {result.errors.map((e, i) => <p key={i} className="text-red-600 text-xs">{e}</p>)}
        </div>
      )}
    </div>
  );
}
