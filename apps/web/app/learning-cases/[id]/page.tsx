import Link from "next/link";
import { api } from "../../../lib/api";
import NewObservationForm from "./NewObservationForm";

export default async function LearningCaseDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  let observations: Awaited<ReturnType<typeof api.listObservations>> = [];
  let error: string | null = null;
  try {
    observations = await api.listObservations(id);
  } catch (e) {
    error = e instanceof Error ? e.message : "Failed to load observations.";
  }

  return (
    <main className="mx-auto max-w-2xl p-6">
      <Link href="/" className="text-sm text-neutral-500 hover:underline">
        ← Students
      </Link>
      <h1 className="mt-2 text-2xl font-semibold">Learning Case</h1>
      <p className="mt-1 text-sm text-neutral-600">
        Recorded moments in the loop. As they accumulate, the hypothesis shifts.
      </p>

      {error && (
        <p className="mt-4 rounded bg-red-50 p-3 text-sm text-red-700">{error}</p>
      )}

      <ul className="mt-6 divide-y border rounded">
        {observations.map((o) => (
          <li key={o.id} className="p-3">
            <div className="font-medium">{o.observed}</div>
            <div className="text-sm text-neutral-500">Root gap: {o.possible_root_gap}</div>
            <div className="text-sm text-neutral-500">Evidence: {o.evidence}</div>
            <div className="text-sm text-neutral-500">Strategy: {o.strategy}</div>
            <div className="text-sm text-neutral-500">Next review: {o.next_review}</div>
          </li>
        ))}
        {observations.length === 0 && !error && (
          <li className="p-3 text-sm text-neutral-500">No observations yet.</li>
        )}
      </ul>

      <NewObservationForm learningCaseId={id} />
    </main>
  );
}
