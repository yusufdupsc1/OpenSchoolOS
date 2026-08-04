"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "../../../lib/api";

interface Props { caseId: string; status: string; studentId: string; }

export default function CaseActions({ caseId, status, studentId }: Props) {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [showReflection, setShowReflection] = useState(false);
  const [reflection, setReflection] = useState("");
  const [outcome, setOutcome] = useState("");
  const [confirmingDelete, setConfirmingDelete] = useState(false);

  async function handleClose() {
    if (!showReflection) { setShowReflection(true); return; }
    setLoading(true);
    try { await api.closeLearningCase(caseId, reflection || undefined, outcome || undefined); router.refresh(); }
    catch { setLoading(false); }
  }

  async function toggleStatus() {
    setLoading(true);
    try {
      if (status === "open") await api.closeLearningCase(caseId);
      else await api.reopenLearningCase(caseId);
      router.refresh();
    } catch { setLoading(false); }
  }

  async function handleDelete() {
    setLoading(true);
    try { await api.deleteLearningCase(caseId); router.push(`/students/${studentId}`); router.refresh(); }
    catch { setLoading(false); }
  }

  function handlePrint() { window.open(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/learning-cases/${caseId}/print`, "_blank"); }

  const toggleLabel = status === "open" ? "Close Case" : "Reopen";

  return (
    <span className="flex items-center gap-1">
      <button onClick={handlePrint} className="rounded border px-2 py-1 text-xs hover:bg-neutral-50" title="Print for parent meeting">Print</button>
      {showReflection ? (
        <span className="flex items-center gap-1">
          <input type="text" value={reflection} onChange={e => setReflection(e.target.value)} placeholder="Reflection..." className="w-32 rounded border px-2 py-1 text-xs" autoFocus />
          <select value={outcome} onChange={e => setOutcome(e.target.value)} className="rounded border px-1 py-1 text-xs">
            <option value="">— outcome —</option>
            <option value="improved">Improved</option>
            <option value="plateaued">Plateaued</option>
            <option value="worsened">Worsened</option>
            <option value="unknown">Unknown</option>
          </select>
          <button onClick={handleClose} disabled={loading} className="rounded bg-amber-600 px-2 py-1 text-xs text-white disabled:opacity-50">{loading ? "..." : "Confirm Close"}</button>
          <button onClick={() => setShowReflection(false)} className="rounded border px-2 py-1 text-xs">Cancel</button>
        </span>
      ) : (
        <button onClick={status === "open" ? handleClose : toggleStatus} disabled={loading} className={`rounded border px-2 py-1 text-xs ${status === "open" ? "border-amber-600 text-amber-700 hover:bg-amber-50" : "border-green-600 text-green-700 hover:bg-green-50"} disabled:opacity-50`}>{loading ? "..." : toggleLabel}</button>
      )}
      {confirmingDelete ? (<><span className="text-xs text-red-600">Delete?</span><button onClick={handleDelete} disabled={loading} className="rounded bg-red-600 px-2 py-1 text-xs text-white disabled:opacity-50">Yes</button><button onClick={() => setConfirmingDelete(false)} className="rounded border px-2 py-1 text-xs">No</button></>) : (<button onClick={() => setConfirmingDelete(true)} className="rounded border px-2 py-1 text-xs text-red-600 hover:bg-red-50">Delete</button>)}
    </span>
  );
}
