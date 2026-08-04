"use client";

import { useState } from "react";
import { type ObservationSummary } from "../../../lib/api";

export default function ObservationSummaryView({ data }: { data: ObservationSummary }) {
  const [showRaw, setShowRaw] = useState(false);

  return (
    <div className="mt-6 rounded border bg-neutral-50 p-4">
      <h2 className="text-sm font-semibold">Observation Summary</h2>
      <p className="mt-1 text-xs text-neutral-400">{data.observation_count} observations across this case — an AI-readable summary for external tools.</p>

      {/* Heuristic summary */}
      <div className="mt-3 rounded bg-white border p-3 text-sm leading-relaxed">
        {data.heuristic_summary}
      </div>

      {/* Root gap progression */}
      {data.root_gap_progression.length > 1 && (
        <div className="mt-3">
          <span className="text-xs font-medium text-neutral-400">ROOT GAP EVOLUTION</span>
          <div className="mt-1 flex flex-wrap items-center gap-1">
            {data.root_gap_progression.map((g, i) => (
              <span key={i} className="flex items-center">
                <span className="rounded bg-white border px-2 py-0.5 text-xs">{g}</span>
                {i < data.root_gap_progression.length - 1 && <span className="mx-1 text-neutral-300">→</span>}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Confidence progression */}
      {data.confidence_progression.some(c => c) && (
        <div className="mt-2">
          <span className="text-xs font-medium text-neutral-400">CONFIDENCE</span>
          <div className="mt-1 flex items-center gap-1">
            {data.confidence_progression.map((c, i) => c && (
              <span key={i} className={`rounded px-2 py-0.5 text-xs font-medium ${
                c === "low" ? "bg-red-100 text-red-700" : c === "medium" ? "bg-amber-100 text-amber-700" : "bg-green-100 text-green-700"
              }`}>{c}</span>
            ))}
          </div>
        </div>
      )}

      {/* Raw context toggle */}
      <button onClick={() => setShowRaw(!showRaw)} className="mt-3 text-xs text-neutral-400 hover:text-neutral-600">
        {showRaw ? "Hide" : "Show"} raw AI context
      </button>
      {showRaw && (
        <pre className="mt-2 max-h-64 overflow-y-auto rounded border bg-white p-3 text-xs text-neutral-500 whitespace-pre-wrap font-mono">{data.raw_context}</pre>
      )}
    </div>
  );
}
