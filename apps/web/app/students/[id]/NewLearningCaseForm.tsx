"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { api, type LearningCaseCreate } from "../../../lib/api";
import RootGapPicker from "../../RootGapPicker";
import SubjectTemplatePicker from "../../SubjectTemplatePicker";

export default function NewLearningCaseForm({ studentId }: { studentId: string }) {
  const router = useRouter();
  const [form, setForm] = useState<Omit<LearningCaseCreate, "student_id">>({
    subject: "", competency: "", possible_root_gap: "", evidence: "", strategy: "", next_review: "",
  });
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  function update(field: keyof typeof form, value: string) { setForm((f) => ({ ...f, [field]: value })); }

  async function submit(e: React.FormEvent) {
    e.preventDefault(); setSaving(true); setError(null);
    try { await api.createLearningCase({ student_id: studentId, ...form }); router.refresh(); }
    catch (err) { setError(err instanceof Error ? err.message : "Failed to save."); setSaving(false); }
  }

  const ldgSubjectMap: Record<string, string> = { Mathematics: "math", Math: "math", Reading: "reading", Writing: "writing", English: "english", Bangla: "bangla" };
  const ldgSubject = ldgSubjectMap[form.subject] || undefined;

  return (
    <form onSubmit={submit} className="mt-6 space-y-3 rounded border p-4">
      <h2 className="font-semibold">New Learning Case</h2>

      <SubjectTemplatePicker
        value={form.subject}
        onChange={(v) => update("subject", v)}
        competencyValue={form.competency}
        onCompetencyChange={(v) => update("competency", v)}
        onCompetencySelected={(c) => { if (c.misconceptions[0]) { update("possible_root_gap", c.misconceptions[0].rootGap); update("evidence", c.misconceptions[0].evidence); update("strategy", c.misconceptions[0].strategy); } }}
      />

      <label className="block text-sm">
        <span className="text-neutral-600">Possible Root Gap {ldgSubject && <span className="ml-1 text-xs text-amber-600">(LDG: {form.subject})</span>}</span>
        <RootGapPicker value={form.possible_root_gap} onChange={(v) => update("possible_root_gap", v)} onSelectMisconception={(m) => { update("possible_root_gap", m.rootGap); update("evidence", m.evidence); update("strategy", m.strategy); }} subject={ldgSubject} placeholder="Search LDG or type freely..." />
      </label>
      <label className="block text-sm"><span className="text-neutral-600">Evidence</span>
        <textarea value={form.evidence} onChange={(e) => update("evidence", e.target.value)} rows={2} className="mt-1 w-full rounded border p-2" />
      </label>
      <label className="block text-sm"><span className="text-neutral-600">Strategy</span>
        <textarea value={form.strategy} onChange={(e) => update("strategy", e.target.value)} rows={2} className="mt-1 w-full rounded border p-2" />
      </label>
      <label className="block text-sm"><span className="text-neutral-600">Next Review</span>
        <input type="date" value={form.next_review} onChange={(e) => update("next_review", e.target.value)} className="mt-1 w-full rounded border p-2" />
      </label>
      {error && <p className="text-sm text-red-700">{error}</p>}
      <button type="submit" disabled={saving} className="rounded bg-neutral-900 px-3 py-2 text-sm text-white disabled:opacity-50">
        {saving ? "Saving..." : "Open Learning Case"}
      </button>
    </form>
  );
}
