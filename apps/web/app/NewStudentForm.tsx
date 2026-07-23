"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { api, type StudentCreate } from "../lib/api";

const FIELDS: { key: keyof StudentCreate; label: string }[] = [
  { key: "full_name", label: "Full Name" },
  { key: "roll_number", label: "Roll Number" },
  { key: "grade", label: "Grade" },
  { key: "section", label: "Section" },
];

export default function NewStudentForm() {
  const router = useRouter();
  const [form, setForm] = useState<StudentCreate>({
    full_name: "",
    roll_number: "",
    grade: "",
    section: "",
  });
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  function update(field: keyof StudentCreate, value: string) {
    setForm((f) => ({ ...f, [field]: value }));
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setSaving(true);
    setError(null);
    try {
      await api.createStudent(form);
      router.refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save student.");
      setSaving(false);
    }
  }

  return (
    <form onSubmit={submit} className="mt-6 space-y-3 rounded border p-4">
      <h2 className="font-semibold">New Student</h2>
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
        {saving ? "Saving…" : "Add Student"}
      </button>
    </form>
  );
}
