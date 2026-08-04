"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "../../../lib/api";

export default function DeleteStudentButton({
  studentId,
}: {
  studentId: string;
}) {
  const router = useRouter();
  const [confirming, setConfirming] = useState(false);
  const [deleting, setDeleting] = useState(false);

  async function handleDelete() {
    setDeleting(true);
    try {
      await api.deleteStudent(studentId);
      router.push("/");
      router.refresh();
    } catch {
      setDeleting(false);
    }
  }

  if (confirming) {
    return (
      <span className="flex items-center gap-1 text-sm">
        <span className="text-red-600">Delete?</span>
        <button
          onClick={handleDelete}
          disabled={deleting}
          className="rounded bg-red-600 px-2 py-1 text-white disabled:opacity-50"
        >
          {deleting ? "…" : "Yes"}
        </button>
        <button
          onClick={() => setConfirming(false)}
          className="rounded border px-2 py-1"
        >
          No
        </button>
      </span>
    );
  }

  return (
    <button
      onClick={() => setConfirming(true)}
      className="rounded border px-3 py-1 text-sm text-red-600 hover:bg-red-50"
    >
      Delete
    </button>
  );
}
