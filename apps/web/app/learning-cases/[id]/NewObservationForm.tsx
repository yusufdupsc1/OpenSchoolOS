"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { api, type ObservationCreate } from "../../../lib/api";

export default function NewObservationForm({ learningCaseId }: { learningCaseId: string }) {
  const router = useRouter();
  const [form, setForm] = useState<ObservationCreate>({
    learning_case_id: learningCaseId,
    observed: "",
    possible_root_gap: "",
    evidence: "",
    strategy: "",
    next_review: "",
  });
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  function update(field: keyof ObservationCreate, value: string) {
    setForm((f) => ({ ...f, [field]: value }));
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setSaving(true);
    setError(null);
    try {
      await api.createObservation(form);
      router.refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save observation.");
      setSaving(false);
    }
  }

  const fields: { key: "observed" | "possible_root_gap" | "evidence" | "strategy" | "next_review"; label: string }[] = [
    { key: "observed", label: "Observed" },
    { key: "possible_root_gap", label: "Possible Root Gap" },
    { key: "evidence", label: "Evidence" },
    { key: "strategy", label: "Strategy" },
    { key: "next_review", label: "Next Review" },
  ];

  return (
    <form onSubmit={submit} className="mt-6 space-y-3 rounded border p-4">
      <h2 className="font-semibold">New Observation</h2>
      {fields.map((f) => (
        <label key={f.key} className="block text-sm">
          <span className="text-neutral-600">{f.label}</span>
          <textarea
            value={form[f.key]}
            onChange={(e) => update(f.key, e.target.value)}
            rows={2}
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
        {saving ? "Saving…" : "Save Observation"}
      </button>
    </form>
  );
}
