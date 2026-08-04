"use client";

import { useState, useEffect } from "react";
import { api, type Competency } from "../lib/api";

interface Props {
  value: string;
  onChange: (v: string) => void;
  competencyValue: string;
  onCompetencyChange: (v: string) => void;
  onCompetencySelected?: (c: Competency) => void;
}

export default function SubjectTemplatePicker({ value, onChange, competencyValue, onCompetencyChange, onCompetencySelected }: Props) {
  const [subjects, setSubjects] = useState<{ id: string; subject: string }[]>([]);
  const [comps, setComps] = useState<Competency[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => { api.listSubjects().then(s => setSubjects(s.map(x => ({ id: x.id, subject: x.subject })))).catch(() => {}); }, []);
  useEffect(() => {
    if (!value) { setComps([]); return; }
    const sid = subjects.find(s => s.subject === value)?.id;
    if (!sid) { setComps([]); return; }
    setLoading(true);
    api.listCompetencies(sid).then(setComps).catch(() => setComps([])).finally(() => setLoading(false));
  }, [value, subjects]);

  return (
    <div className="space-y-2">
      <label className="block text-sm"><span className="text-neutral-600">Subject</span>
        <select value={subjects.find(s => s.subject === value)?.id || ""} onChange={e => {
          const sid = e.target.value;
          if (sid === "__other__") { onChange(""); onCompetencyChange(""); return; }
          onChange(subjects.find(s => s.id === sid)?.subject || sid);
        }} className="mt-1 w-full rounded border p-2">
          <option value="">— Select subject (LDG) —</option>
          {subjects.map(s => <option key={s.id} value={s.id}>{s.subject}</option>)}
          <option value="__other__">Other (type below)</option>
        </select>
      </label>
      {value && comps.length > 0 && <label className="block text-sm"><span className="text-neutral-600">Competency {loading && "(loading...)"}</span>
        <select value={comps.find(c => c.label === competencyValue)?.id || ""} onChange={e => {
          const c = comps.find(x => x.id === e.target.value);
          if (c) { onCompetencyChange(c.label); onCompetencySelected?.(c); }
        }} className="mt-1 w-full rounded border p-2">
          <option value="">— Select —</option>
          {comps.map(c => <option key={c.id} value={c.id}>{c.label} ({c.gradeLevel})</option>)}
        </select>
      </label>}
      <label className="block text-sm"><span className="text-neutral-600">Custom subject:</span>
        <input type="text" value={value} onChange={e => onChange(e.target.value)} className="mt-1 w-full rounded border p-2" />
      </label>
      <label className="block text-sm"><span className="text-neutral-600">Custom competency:</span>
        <input type="text" value={competencyValue} onChange={e => onCompetencyChange(e.target.value)} className="mt-1 w-full rounded border p-2" placeholder="e.g., Fractions" />
      </label>
    </div>
  );
}
