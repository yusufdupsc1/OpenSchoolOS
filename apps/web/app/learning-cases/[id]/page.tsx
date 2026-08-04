import Link from "next/link";
import { api } from "../../../lib/api";
import NewObservationForm from "./NewObservationForm";
import CaseActions from "./CaseActions";
import EditCaseForm from "./EditCaseForm";
import ReasoningTimelineView from "./ReasoningTimeline";
import SimilarCasesView from "./SimilarCases";
import ObservationSummaryView from "./ObservationSummary";
import type { LearningCaseOut, ObservationOut, ReasoningTimeline, SimilarCasesResult, ObservationSummary } from "../../../lib/api";

async function LearningCaseDetailPageContent({
  caseId,
}: {
  caseId: string;
}) {
  let lc: LearningCaseOut | null = null;
  let observations: ObservationOut[] = [];
  let timeline: ReasoningTimeline | null = null;
  let similar: SimilarCasesResult | null = null;
  let summary: ObservationSummary | null = null;
  let error: string | null = null;

  try {
    [lc, observations, timeline, similar, summary] = await Promise.all([
      api.getLearningCase(caseId),
      api.listObservations(caseId),
      api.getReasoningTimeline(caseId),
      api.similarCases(caseId).catch(() => null),
      api.observationSummary(caseId).catch(() => null),
    ]);
  } catch (e) {
    error = e instanceof Error ? e.message : "Failed to load.";
  }

  if (error) {
    return (
      <main className="mx-auto max-w-2xl p-6">
        <Link href="/" className="text-sm text-neutral-500 hover:underline">
          &larr; Students
        </Link>
        <p className="mt-4 rounded bg-red-50 p-3 text-sm text-red-700">{error}</p>
      </main>
    );
  }

  if (!lc) {
    return (
      <main className="mx-auto max-w-2xl p-6">
        <Link href="/" className="text-sm text-neutral-500 hover:underline">
          &larr; Students
        </Link>
        <p className="mt-4 text-sm text-neutral-500">Learning case not found.</p>
      </main>
    );
  }

  return (
    <main className="mx-auto max-w-2xl p-6">
      <Link
        href={`/students/${lc.student_id}`}
        className="text-sm text-neutral-500 hover:underline"
      >
        &larr; Student
      </Link>

      {/* Case header */}
      <div className="mt-2">
        <div className="flex items-start justify-between">
          <h1 className="text-2xl font-semibold">
            {lc.subject} &mdash; {lc.competency}
          </h1>
          <div className="flex items-center gap-2">
            <span
              className={`text-sm font-medium ${
                lc.status === "open" ? "text-green-600" : "text-neutral-400"
              }`}
            >
              {lc.status}
            </span>
            <EditCaseForm lc={lc} caseId={caseId} />
            <CaseActions
              caseId={caseId}
              status={lc.status}
              studentId={lc.student_id}
            />
          </div>
        </div>

        {/* Case detail card */}
        <div className="mt-4 rounded border p-4 space-y-2">
          <div>
            <span className="text-xs font-medium text-neutral-400">
              POSSIBLE ROOT GAP
            </span>
            <p className="text-sm">{lc.possible_root_gap}</p>
          </div>
          <div>
            <span className="text-xs font-medium text-neutral-400">EVIDENCE</span>
            <p className="text-sm">{lc.evidence}</p>
          </div>
          <div>
            <span className="text-xs font-medium text-neutral-400">STRATEGY</span>
            <p className="text-sm">{lc.strategy}</p>
          </div>
          <div>
            <span className="text-xs font-medium text-neutral-400">
              NEXT REVIEW
            </span>
            <p className="text-sm">{lc.next_review}</p>
          </div>
          {lc.closed_at && (
            <div>
              <span className="text-xs font-medium text-neutral-400">CLOSED</span>
              <p className="text-sm">{new Date(lc.closed_at).toLocaleDateString()}</p>
            </div>
          )}
        </div>

        {/* Reflection */}
        {lc.reflection && (
          <div className="mt-3 rounded border-l-4 border-green-500 bg-green-50 p-3">
            <span className="text-xs font-medium text-green-700">TEACHER REFLECTION</span>
            <p className="text-sm italic mt-1">{lc.reflection}</p>
          </div>
        )}
      </div>

      {/* Reasoning Timeline (replaces raw observations list) */}
      {timeline && <ReasoningTimelineView timeline={timeline} />}

      {/* Observation list (compact, for reference) */}
      {observations.length > 0 && (
        <details className="mt-4">
          <summary className="cursor-pointer text-sm font-medium text-neutral-400 hover:text-neutral-600">
            Raw observation list ({observations.length})
          </summary>
          <ul className="mt-2 divide-y border rounded">
            {observations.map((o) => (
              <li key={o.id} className="p-3">
                <div className="flex flex-wrap items-center gap-x-2 gap-y-0.5">
                  <span className="font-medium text-sm">{o.observed}</span>
                  {o.confidence && (
                    <span className={`rounded px-1.5 py-0.5 text-xs font-medium ${
                      o.confidence === "low" ? "bg-red-100 text-red-700" :
                      o.confidence === "medium" ? "bg-amber-100 text-amber-700" :
                      "bg-green-100 text-green-700"
                    }`}>
                      {o.confidence}
                    </span>
                  )}
                  {o.evidence_strength && (
                    <span className="rounded bg-neutral-100 px-1.5 py-0.5 text-xs text-neutral-600">
                      {o.evidence_strength.replace("_", " ")}
                    </span>
                  )}
                </div>
                <div className="text-sm text-neutral-500">Root gap: {o.possible_root_gap}</div>
                <div className="text-sm text-neutral-500">Evidence: {o.evidence}</div>
                <div className="text-sm text-neutral-500">Strategy: {o.strategy}</div>
                <div className="text-sm text-neutral-500">Next review: {o.next_review}</div>
              </li>
            ))}
          </ul>
        </details>
      )}

      {/* AI Extension Points */}
      {similar && <SimilarCasesView data={similar} />}
      {summary && <ObservationSummaryView data={summary} />}

      <NewObservationForm learningCaseId={caseId} caseSubject={lc.subject} />
    </main>
  );
}

export default async function LearningCaseDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  return <LearningCaseDetailPageContent caseId={id} />;
}
