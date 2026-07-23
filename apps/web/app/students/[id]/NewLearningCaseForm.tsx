"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { api, type LearningCaseCreate } from "../../../lib/api";

const FIELDS: { key: "subject" | "competency" | "possible_root_gap" | "evidence" | "strategy" | "next_review"; label: string }[] = [
  { key: "subject", label: "Subject" },
  { key: "competency", label: "Competency" },
  { key: "possible_root_gap", label: "Possible Root Gap" },
  { key: "evidence", label: "Evidence" },
  { key: "strategy", label: "Strategy" },
  { key: "next_review", label: "Next Review" },
];

export default function NewLearningCaseForm({ studentId }: { studentId: string }) {
  const router = useRouter();
  const [form, setForm] = useState<Omit<LearningCaseCreate, "student_id">>({
    subject: "",
    competency: "",
    possible_root_gap: "",
    evidence: "",
    strategy: "",
    next_review: "",
  });
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  function update(field: keyof typeof form, value: string) {
    setForm((f) => ({ ...f, [field]: value }));
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setSaving(true);
    setError(null);
    try {
      await api.createLearningCase({ student_id: studentId, ...form });
      router.refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save learning case.");
      setSaving(false);
    }
  }

  return (
    <form onSubmit={submit} className="mt-6 space-y-3 rounded border p-4">
      <h2 className="font-semibold">New Learning Case</h2>
      {FIELDS.map((f) => (
        <label key={f.key} className="block text-sm">
          <span className="text-neutral-600">{f.label}</span>
          <input
            value={form[f.key]}
            onChange={(e) => update(f.key, e.target.value)}
            className="mt-1 w-full rounded border p-2"
          />
        </label>
      ))}
      {error && <p className="text-sm text-red-700">{error}</p>}
      <button
        type="submit"
        disabled={saving}
        className="rounded bg-neutral-900 px-3 py-2 text-sm text-white disabled:opacity-50"
      >
        {saving ? "Saving…" : "Open Learning Case"}
      </button>
    </form>
  );
}
