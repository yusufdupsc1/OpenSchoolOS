"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { api, type LearningCaseOut, type LearningCaseUpdate } from "../../../lib/api";

export default function EditCaseForm({
  lc,
  caseId,
}: {
  lc: LearningCaseOut;
  caseId: string;
}) {
  const router = useRouter();
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState<LearningCaseUpdate>({
    subject: lc.subject,
    competency: lc.competency,
    possible_root_gap: lc.possible_root_gap,
    evidence: lc.evidence,
    strategy: lc.strategy,
    next_review: lc.next_review,
  });
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  if (!open) {
    return (
      <button
        onClick={() => setOpen(true)}
        className="rounded border px-2 py-1 text-xs hover:bg-neutral-50"
      >
        Edit
      </button>
    );
  }

  const fields: { key: keyof LearningCaseUpdate; label: string }[] = [
    { key: "subject", label: "Subject" },
    { key: "competency", label: "Competency" },
    { key: "possible_root_gap", label: "Possible Root Gap" },
    { key: "evidence", label: "Evidence" },
    { key: "strategy", label: "Strategy" },
    { key: "next_review", label: "Next Review" },
  ];

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setSaving(true);
    setError(null);
    try {
      await api.updateLearningCase(caseId, form);
      router.refresh();
      setOpen(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save.");
      setSaving(false);
    }
  }

  return (
    <form
      onSubmit={submit}
      className="fixed inset-0 z-10 flex items-center justify-center bg-black/20"
      onClick={(e) => {
        if (e.target === e.currentTarget) setOpen(false);
      }}
    >
      <div className="w-full max-w-md space-y-3 rounded border bg-white p-6 shadow-lg">
        <h2 className="font-semibold">Edit Learning Case</h2>
        {fields.map((f) => (
          <label key={f.key} className="block text-sm">
            <span className="text-neutral-600">{f.label}</span>
            <input
              value={(form[f.key] as string) ?? ""}
              onChange={(e) =>
                setForm((prev) => ({ ...prev, [f.key]: e.target.value }))
              }
              className="mt-1 w-full rounded border p-2"
            />
          </label>
        ))}
        {error && <p className="text-sm text-red-700">{error}</p>}
        <div className="flex gap-2">
          <button
            type="submit"
            disabled={saving}
            className="rounded bg-neutral-900 px-3 py-2 text-sm text-white disabled:opacity-50"
          >
            {saving ? "Saving…" : "Save"}
          </button>
          <button
            type="button"
            onClick={() => setOpen(false)}
            className="rounded border px-3 py-2 text-sm"
          >
            Cancel
          </button>
        </div>
      </div>
    </form>
  );
}
