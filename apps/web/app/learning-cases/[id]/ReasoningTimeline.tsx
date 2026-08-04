import { type ReasoningTimeline as RT } from "../../../lib/api";

function confidenceBadge(c: string | null) {
  if (!c) return null;
  const colors: Record<string, string> = {
    low: "bg-red-100 text-red-700",
    medium: "bg-amber-100 text-amber-700",
    high: "bg-green-100 text-green-700",
  };
  return (
    <span
      className={`ml-1 rounded px-1.5 py-0.5 text-xs font-medium ${colors[c] ?? "bg-neutral-100 text-neutral-600"}`}
    >
      {c}
    </span>
  );
}

function strengthBadge(s: string | null) {
  if (!s) return null;
  const colors: Record<string, string> = {
    direct_observation: "bg-blue-100 text-blue-700",
    inference: "bg-purple-100 text-purple-700",
    test_result: "bg-teal-100 text-teal-700",
  };
  return (
    <span
      className={`ml-1 rounded px-1.5 py-0.5 text-xs font-medium ${colors[s] ?? "bg-neutral-100 text-neutral-600"}`}
    >
      {s.replace("_", " ")}
    </span>
  );
}

function changeIndicator(changed: boolean) {
  if (!changed) return null;
  return (
    <span className="ml-1 text-xs font-bold text-amber-600" title="Changed from previous observation">
      ↻
    </span>
  );
}

function parseHypotheses(raw: string | null): string[] {
  if (!raw) return [];
  try {
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

export default function ReasoningTimelineView({
  timeline,
}: {
  timeline: RT;
}) {
  if (timeline.snapshots.length === 0) {
    return (
      <div className="mt-8">
        <h2 className="text-lg font-semibold">Reasoning Timeline</h2>
        <p className="mt-1 text-sm text-neutral-500">
          No observations recorded yet. The timeline will show how your thinking evolves.
        </p>
      </div>
    );
  }

  return (
    <div className="mt-8">
      <h2 className="text-lg font-semibold">Reasoning Timeline</h2>
      <p className="mt-1 text-sm text-neutral-600">
        How your hypothesis, strategy, and confidence evolved across{" "}
        {timeline.snapshots.length} observation
        {timeline.snapshots.length > 1 ? "s" : ""}.
      </p>

      {/* Current state summary */}
      <div className="mt-4 rounded border bg-neutral-50 p-3 text-sm">
        <div className="flex flex-wrap items-center gap-x-4 gap-y-1">
          <span>
            <span className="text-neutral-400">Current root gap:</span>{" "}
            <span className="font-medium">{timeline.current_root_gap}</span>
          </span>
          <span>
            <span className="text-neutral-400">Strategy:</span>{" "}
            <span className="font-medium">{timeline.current_strategy}</span>
          </span>
          <span>
            <span className="text-neutral-400">Status:</span>{" "}
            <span
              className={`font-medium ${timeline.status === "open" ? "text-green-600" : "text-neutral-400"}`}
            >
              {timeline.status}
            </span>
          </span>
        </div>
      </div>

      {/* Timeline steps */}
      <div className="mt-6 relative">
        {/* Vertical line */}
        <div className="absolute left-4 top-0 h-full w-0.5 bg-neutral-200" />

        <ol className="space-y-6">
          {timeline.snapshots.map((s) => (
            <li key={s.observation_id} className="relative pl-10">
              {/* Circle marker */}
              <div
                className={`absolute left-2.5 top-1.5 h-3 w-3 rounded-full border-2 ${
                  s.root_gap_changed
                    ? "border-amber-500 bg-amber-100"
                    : "border-neutral-300 bg-white"
                }`}
              />

              {/* Header */}
              <div className="flex flex-wrap items-center gap-x-2 gap-y-0.5">
                <span className="text-xs font-medium text-neutral-400">
                  #{s.index}
                </span>
                {s.created_at && (
                  <span className="text-xs text-neutral-400">
                    {new Date(s.created_at).toLocaleDateString()}
                  </span>
                )}
                {s.root_gap_changed && (
                  <span className="text-xs font-medium text-amber-600">
                    Hypothesis shifted
                  </span>
                )}
                {s.strategy_changed && !s.root_gap_changed && (
                  <span className="text-xs font-medium text-amber-600">
                    Strategy revised
                  </span>
                )}
              </div>

              {/* Content */}
              <div className="mt-1 space-y-1 text-sm">
                <p className="font-medium">{s.observed}</p>

                <div className="flex flex-wrap items-center gap-x-3 gap-y-0.5 text-neutral-500">
                  <span>
                    Root gap:{" "}
                    <span className="font-medium text-neutral-700">
                      {s.root_gap}
                    </span>
                    {changeIndicator(s.root_gap_changed)}
                  </span>
                  {s.confidence && confidenceBadge(s.confidence)}
                  {s.evidence_strength && strengthBadge(s.evidence_strength)}
                </div>

                <div className="text-neutral-500">
                  Evidence: {s.evidence}
                </div>

                <div className="text-neutral-500">
                  Strategy:{" "}
                  <span className="font-medium text-neutral-700">
                    {s.strategy}
                  </span>
                  {changeIndicator(s.strategy_changed)}
                </div>

                {parseHypotheses(s.alternative_hypotheses).length > 0 && (
                  <div className="rounded bg-amber-50 p-2 text-xs">
                    <span className="font-medium text-amber-800">
                      Also considered:
                    </span>{" "}
                    {parseHypotheses(s.alternative_hypotheses).join(" · ")}
                  </div>
                )}
              </div>
            </li>
          ))}
        </ol>
      </div>
    </div>
  );
}
