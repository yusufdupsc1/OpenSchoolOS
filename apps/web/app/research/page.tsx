const BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function getDashboard() {
  const res = await fetch(`${BASE}/research/dashboard`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to load");
  return res.json();
}

function badge(value: number, label: string, color: string) {
  return `<span class="badge ${color}">${value} ${label}</span>`;
}

export default async function ResearchPage() {
  let d: any = null;
  let error: string | null = null;
  try { d = await getDashboard(); }
  catch (e) { error = e instanceof Error ? e.message : "Failed to load"; }

  return (
    <main className="mx-auto max-w-2xl p-6">
      <h1 className="text-2xl font-semibold">Research Dashboard</h1>
      <p className="mt-1 text-sm text-neutral-600">Measure whether cases improve learning.</p>

      {error && <p className="mt-4 rounded bg-red-50 p-3 text-sm text-red-700">{error}</p>}

      {d && (
        <>
          {/* Summary cards */}
          <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-4">
            <div className="rounded border p-3 text-center">
              <div className="text-2xl font-bold">{d.total_cases}</div>
              <div className="text-xs text-neutral-400">Total Cases</div>
            </div>
            <div className="rounded border p-3 text-center">
              <div className="text-2xl font-bold text-green-600">{d.open_cases}</div>
              <div className="text-xs text-neutral-400">Open</div>
            </div>
            <div className="rounded border p-3 text-center">
              <div className="text-2xl font-bold text-neutral-400">{d.closed_cases}</div>
              <div className="text-xs text-neutral-400">Closed</div>
            </div>
            <div className="rounded border p-3 text-center">
              <div className="text-2xl font-bold">{d.total_observations}</div>
              <div className="text-xs text-neutral-400">Observations</div>
            </div>
          </div>

          {/* Outcomes */}
          {d.outcomes.length > 0 && (
            <div className="mt-6">
              <h2 className="font-semibold">Outcomes</h2>
              <div className="mt-2 flex flex-wrap gap-2">
                {d.outcomes.map((o: { outcome: string; count: number }) => (
                  <span key={o.outcome} className={`rounded-full px-3 py-1 text-sm font-medium ${
                    o.outcome === "improved" ? "bg-green-100 text-green-700" :
                    o.outcome === "plateaued" ? "bg-amber-100 text-amber-700" :
                    o.outcome === "worsened" ? "bg-red-100 text-red-700" :
                    "bg-neutral-100 text-neutral-600"
                  }`}>
                    {o.outcome}: {o.count}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Duration */}
          <div className="mt-6">
            <h2 className="font-semibold">Time to Close</h2>
            {d.duration.overall.count > 0 ? (
              <>
                <p className="mt-1 text-sm text-neutral-500">
                  Overall: avg {d.duration.overall.avg_days}d, median {d.duration.overall.median_days}d ({d.duration.overall.count} cases)
                </p>
                {d.duration.by_subject.some((s: any) => s.count > 0) && (
                  <ul className="mt-2 space-y-1 text-sm">
                    {d.duration.by_subject.filter((s: any) => s.count > 0).map((s: any) => (
                      <li key={s.group_label} className="flex justify-between border-b py-1">
                        <span className="font-medium">{s.group_label}</span>
                        <span className="text-neutral-500">
                          {s.count} cases · avg {s.avg_days}d · median {s.median_days}d
                        </span>
                      </li>
                    ))}
                  </ul>
                )}
              </>
            ) : (
              <p className="mt-1 text-sm text-neutral-400">No closed cases yet.</p>
            )}
          </div>

          {/* Top Strategies */}
          {d.top_strategies.length > 0 && (
            <div className="mt-6">
              <h2 className="font-semibold">Strategy Effectiveness</h2>
              <div className="mt-2 space-y-2">
                {d.top_strategies.map((s: any) => (
                  <div key={s.strategy} className="rounded border p-3">
                    <div className="text-sm font-medium">{s.strategy}</div>
                    <div className="mt-1 flex gap-3 text-xs">
                      <span className="text-neutral-400">{s.count} cases</span>
                      {s.improved > 0 && <span className="text-green-600">{s.improved} improved</span>}
                      {s.plateaued > 0 && <span className="text-amber-600">{s.plateaued} plateaued</span>}
                      {s.worsened > 0 && <span className="text-red-600">{s.worsened} worsened</span>}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Cases per subject */}
          {d.cases_per_subject.length > 0 && (
            <div className="mt-6">
              <h2 className="font-semibold">Cases by Subject</h2>
              <div className="mt-2 flex flex-wrap gap-2 text-sm">
                {d.cases_per_subject.map((x: any) => (
                  <span key={x.subject} className="rounded border px-3 py-1">
                    {x.subject}: {x.count}
                  </span>
                ))}
              </div>
            </div>
          )}
        </>
      )}
    </main>
  );
}
