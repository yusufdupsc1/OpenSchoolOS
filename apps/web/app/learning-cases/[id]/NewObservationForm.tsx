"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { api, type ObservationCreate } from "../../../lib/api";
import RootGapPicker from "../../RootGapPicker";

export default function NewObservationForm({
  learningCaseId,
  caseSubject,
}: {
  learningCaseId: string;
  caseSubject?: string;
}) {
  const router = useRouter();
  const [form, setForm] = useState<ObservationCreate>({
    learning_case_id: learningCaseId,
    observed: "",
    possible_root_gap: "",
    evidence: "",
    evidence_strength: "",
    strategy: "",
    confidence: "",
    alternative_hypotheses: "",
    next_review: "",
  });
  const [altInput, setAltInput] = useState("");
  const [altList, setAltList] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  function update(field: keyof ObservationCreate, value: string) {
    setForm((f) => ({ ...f, [field]: value }));
  }

  function addAlternative() {
    const trimmed = altInput.trim();
    if (trimmed && !altList.includes(trimmed)) {
      const next = [...altList, trimmed];
      setAltList(next);
      update("alternative_hypotheses", JSON.stringify(next));
      setAltInput("");
    }
  }

  function removeAlternative(idx: number) {
    const next = altList.filter((_, i) => i !== idx);
    setAltList(next);
    update("alternative_hypotheses", next.length ? JSON.stringify(next) : "");
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setSaving(true);
    setError(null);
    try {
      await api.createObservation(form);
      router.refresh();
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to save observation."
      );
      setSaving(false);
    }
  }

  const ldgSubjectMap: Record<string, string> = {
    Mathematics: "math", Math: "math",
    Reading: "reading", Writing: "writing",
    English: "english", Bangla: "bangla", বাংলা: "bangla",
  };
  const ldgSubject = caseSubject ? ldgSubjectMap[caseSubject] || undefined : undefined;

  return (
    <form onSubmit={submit} className="mt-6 space-y-3 rounded border p-4">
      <h2 className="font-semibold">New Observation</h2>

      {/* Observed */}
      <label className="block text-sm">
        <span className="text-neutral-600">Observed</span>
        <textarea
          value={form.observed}
          onChange={(e) => update("observed", e.target.value)}
          rows={2}
          placeholder="What did you actually see the student do?"
          className="mt-1 w-full rounded border p-2"
        />
      </label>

      {/* Root Gap + LDG */}
      <label className="block text-sm">
        <span className="text-neutral-600">
          Possible Root Gap
          {ldgSubject && (
            <span className="ml-1 text-xs text-amber-600">
              (LDG: {caseSubject} — type to search)
            </span>
          )}
        </span>
        <RootGapPicker
          value={form.possible_root_gap}
          onChange={(v) => update("possible_root_gap", v)}
          onSelectMisconception={(m) => {
            update("possible_root_gap", m.rootGap);
            update("evidence", m.evidence);
            update("strategy", m.strategy);
          }}
          subject={ldgSubject}
          placeholder="Search LDG or type freely…"
        />
      </label>

      {/* Evidence */}
      <label className="block text-sm">
        <span className="text-neutral-600">Evidence</span>
        <textarea
          value={form.evidence}
          onChange={(e) => update("evidence", e.target.value)}
          rows={2}
          className="mt-1 w-full rounded border p-2"
        />
      </label>

      {/* Evidence strength */}
      <label className="block text-sm">
        <span className="text-neutral-600">Evidence Strength</span>
        <select
          value={form.evidence_strength ?? ""}
          onChange={(e) => update("evidence_strength", e.target.value)}
          className="mt-1 w-full rounded border p-2"
        >
          <option value="">—</option>
          <option value="direct_observation">Direct Observation</option>
          <option value="inference">Inference</option>
          <option value="test_result">Test Result</option>
        </select>
      </label>

      {/* Strategy */}
      <label className="block text-sm">
        <span className="text-neutral-600">Strategy</span>
        <textarea
          value={form.strategy}
          onChange={(e) => update("strategy", e.target.value)}
          rows={2}
          className="mt-1 w-full rounded border p-2"
        />
      </label>

      {/* Confidence */}
      <label className="block text-sm">
        <span className="text-neutral-600">Confidence</span>
        <select
          value={form.confidence ?? ""}
          onChange={(e) => update("confidence", e.target.value)}
          className="mt-1 w-full rounded border p-2"
        >
          <option value="">—</option>
          <option value="low">Low — I&apos;m guessing</option>
          <option value="medium">Medium — plausible but not certain</option>
          <option value="high">High — strong evidence supports this</option>
        </select>
      </label>

      {/* Alternative hypotheses */}
      <fieldset className="block text-sm">
        <legend className="text-neutral-600">Alternative Hypotheses</legend>
        <p className="text-xs text-neutral-400">
          What else could explain the observed behaviour?
        </p>
        <div className="mt-1 flex gap-2">
          <input
            value={altInput}
            onChange={(e) => setAltInput(e.target.value)}
            onKeyDown={(e) => { if (e.key === "Enter") { e.preventDefault(); addAlternative(); } }}
            placeholder="Another possible root gap…"
            className="flex-1 rounded border p-2"
          />
          <button
            type="button"
            onClick={addAlternative}
            className="rounded border px-3 py-2 text-sm hover:bg-neutral-50"
          >
            Add
          </button>
        </div>
        {altList.length > 0 && (
          <ul className="mt-2 space-y-1">
            {altList.map((h, i) => (
              <li key={i} className="flex items-center gap-2 rounded bg-amber-50 px-2 py-1 text-xs">
                <span className="flex-1 text-amber-800">{h}</span>
                <button
                  type="button"
                  onClick={() => removeAlternative(i)}
                  className="text-amber-500 hover:text-red-600"
                >
                  ✕
                </button>
              </li>
            ))}
          </ul>
        )}
      </fieldset>

      {/* Next Review */}
      <label className="block text-sm">
        <span className="text-neutral-600">Next Review</span>
        <input
          type="date"
          value={form.next_review}
          onChange={(e) => update("next_review", e.target.value)}
          className="mt-1 w-full rounded border p-2"
        />
      </label>

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
