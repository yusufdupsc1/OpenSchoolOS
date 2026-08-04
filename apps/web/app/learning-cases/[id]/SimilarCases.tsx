import Link from "next/link";
import { type SimilarCasesResult } from "../../../lib/api";

function outcomeLabel(o: string | null) {
  if (!o) return null;
  const c: Record<string, string> = { improved: "bg-green-100 text-green-700", plateaued: "bg-amber-100 text-amber-700", worsened: "bg-red-100 text-red-700", unknown: "bg-neutral-100 text-neutral-500" };
  return <span className={`ml-1 rounded px-1.5 py-0.5 text-xs font-medium ${c[o] ?? "bg-neutral-100"}`}>{o}</span>;
}

function simLabel(s: string) {
  const m: Record<string, string> = { same_root_gap: "↻ Same root gap", same_subject: "📚 Same subject", same_strategy: "🎯 Same strategy" };
  return m[s] ?? s;
}

export default function SimilarCasesView({ data }: { data: SimilarCasesResult }) {
  if (data.results.length === 0) {
    return (
      <div className="mt-6 rounded border bg-neutral-50 p-4">
        <h2 className="text-sm font-semibold">Similar Cases</h2>
        <p className="mt-1 text-xs text-neutral-400">No similar cases found. As you record more cases with similar root gaps, strategies, or subjects, they will appear here.</p>
      </div>
    );
  }

  return (
    <div className="mt-6 rounded border bg-neutral-50 p-4">
      <h2 className="text-sm font-semibold">Similar Cases ({data.results.length})</h2>
      <p className="mt-1 text-xs text-neutral-400">Cases sharing the same root gap, subject, or strategy. Click to learn from similar practice.</p>
      <div className="mt-3 space-y-2">
        {data.results.map((c) => (
          <Link key={c.case_id} href={`/learning-cases/${c.case_id}`} className="block rounded border bg-white p-3 hover:shadow-sm transition-shadow">
            <div className="flex items-start justify-between">
              <div>
                <span className="text-sm font-medium">{c.subject} — {c.competency}</span>
                <span className="ml-2 text-xs text-neutral-400">{c.student_name}</span>
              </div>
              <span className="text-xs text-neutral-400">{simLabel(c.similarity)}</span>
            </div>
            <div className="mt-1 flex flex-wrap items-center gap-x-3 gap-y-0.5 text-xs text-neutral-500">
              <span>Gap: <span className="font-medium">{c.possible_root_gap}</span></span>
              <span>Strategy: <span className="font-medium">{c.strategy}</span></span>
              <span>{c.observation_count} obs</span>
              <span className={c.status === "open" ? "text-green-600" : "text-neutral-400"}>{c.status}</span>
              {outcomeLabel(c.outcome)}
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
