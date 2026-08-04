"use client";

import { useState, useEffect, useRef } from "react";
import { api, type CompetencySearchResult } from "../lib/api";

interface Props {
  value: string;
  onChange: (value: string) => void;
  onSelectMisconception?: (m: {
    rootGap: string;
    evidence: string;
    strategy: string;
    observed: string;
  }) => void;
  subject?: string;
  placeholder?: string;
}

export default function RootGapPicker({
  value,
  onChange,
  onSelectMisconception,
  subject,
  placeholder = "Search competencies and misconceptions…",
}: Props) {
  const [open, setOpen] = useState(false);
  const [results, setResults] = useState<CompetencySearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  // Close on outside click
  useEffect(() => {
    function handleClick(e: MouseEvent) {
      if (
        containerRef.current &&
        !containerRef.current.contains(e.target as Node)
      ) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, []);

  async function search(q: string) {
    onChange(q);
    if (q.length < 2) {
      setResults([]);
      setOpen(false);
      return;
    }
    setLoading(true);
    setOpen(true);
    try {
      if (subject) {
        const r = await api.searchCompetencies(subject, q);
        setResults(r);
      } else {
        const r = await api.searchAllSubjects(q);
        setResults(r);
      }
    } catch {
      setResults([]);
    }
    setLoading(false);
  }

  function selectResult(r: CompetencySearchResult) {
    // If there are matched misconceptions, the user picks from them
    const misconception = r.matchedMisconceptions?.[0];
    if (misconception && onSelectMisconception) {
      onSelectMisconception(misconception);
      onChange(misconception.rootGap);
    } else {
      onChange(r.competencyLabel || r.description);
    }
    setOpen(false);
  }

  function selectMisconception(m: {
    rootGap: string;
    evidence: string;
    strategy: string;
    observed: string;
  }) {
    if (onSelectMisconception && m) {
      onSelectMisconception(m);
      onChange(m.rootGap);
    }
    setOpen(false);
  }

  return (
    <div ref={containerRef} className="relative">
      <input
        type="text"
        value={value}
        onChange={(e) => search(e.target.value)}
        onFocus={() => {
          if (results.length > 0) setOpen(true);
        }}
        placeholder={placeholder}
        className="mt-1 w-full rounded border p-2"
      />
      {open && (
        <div className="absolute z-20 mt-1 max-h-64 w-full overflow-y-auto rounded border bg-white shadow-lg">
          {loading && (
            <div className="p-2 text-sm text-neutral-400">Searching…</div>
          )}
          {!loading && results.length === 0 && (
            <div className="p-2 text-sm text-neutral-400">
              No matches found. Type freely or try different words.
            </div>
          )}
          {!loading &&
            results.map((r, i) => (
              <div key={`${r.competencyId ?? i}-${i}`}>
                <button
                  type="button"
                  onClick={() => selectResult(r)}
                  className="w-full px-3 py-2 text-left hover:bg-neutral-50"
                >
                  <div className="text-sm font-medium">
                    {r.competencyLabel || r.description}
                  </div>
                  <div className="text-xs text-neutral-400">
                    {r.subject
                      ? `${r.subject} · ${r.gradeLevel}`
                      : r.gradeLevel}
                  </div>
                </button>
                {/* Show matched misconceptions as sub-options */}
                {r.matchedMisconceptions?.map((m: { observed: string; rootGap: string; evidence: string; strategy: string }, j: number) => (
                  <button
                    key={j}
                    type="button"
                    onClick={() => selectMisconception(m)}
                    className="w-full border-t border-neutral-100 bg-amber-50 px-5 py-2 text-left hover:bg-amber-100"
                  >
                    <div className="text-xs font-medium text-amber-800">
                      Pattern: &ldquo;{m.observed}&rdquo;
                    </div>
                    <div className="text-xs text-amber-600">
                      Root gap: {m.rootGap}
                    </div>
                  </button>
                ))}
              </div>
            ))}
        </div>
      )}
    </div>
  );
}
