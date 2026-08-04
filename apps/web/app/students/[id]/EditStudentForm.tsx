"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { api, type StudentOut, type StudentUpdate } from "../../../lib/api";

export default function EditStudentForm({ student }: { student: StudentOut }) {
  const router = useRouter();
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState<StudentUpdate>({
    full_name: student.full_name,
    roll_number: student.roll_number,
    grade: student.grade,
    section: student.section,
    status: student.status,
  });
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  if (!open) {
    return (
      <button
        onClick={() => setOpen(true)}
        className="rounded border px-3 py-1 text-sm hover:bg-neutral-50"
      >
        Edit
      </button>
    );
  }

  function update(field: keyof StudentUpdate, value: string) {
    setForm((f) => ({ ...f, [field]: value }));
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setSaving(true);
    setError(null);
    try {
      await api.updateStudent(student.id, form);
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
        <h2 className="font-semibold">Edit Student</h2>
        <label className="block text-sm">
          <span className="text-neutral-600">Full Name</span>
          <input
            value={form.full_name ?? ""}
            onChange={(e) => update("full_name", e.target.value)}
            className="mt-1 w-full rounded border p-2"
          />
        </label>
        <label className="block text-sm">
          <span className="text-neutral-600">Roll Number</span>
          <input
            value={form.roll_number ?? ""}
            onChange={(e) => update("roll_number", e.target.value)}
            className="mt-1 w-full rounded border p-2"
          />
        </label>
        <label className="block text-sm">
          <span className="text-neutral-600">Grade</span>
          <input
            value={form.grade ?? ""}
            onChange={(e) => update("grade", e.target.value)}
            className="mt-1 w-full rounded border p-2"
          />
        </label>
        <label className="block text-sm">
          <span className="text-neutral-600">Section</span>
          <input
            value={form.section ?? ""}
            onChange={(e) => update("section", e.target.value)}
            className="mt-1 w-full rounded border p-2"
          />
        </label>
        <label className="block text-sm">
          <span className="text-neutral-600">Status</span>
          <select
            value={form.status ?? "active"}
            onChange={(e) => update("status", e.target.value)}
            className="mt-1 w-full rounded border p-2"
          >
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
            <option value="graduated">Graduated</option>
            <option value="transferred">Transferred</option>
          </select>
        </label>
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
