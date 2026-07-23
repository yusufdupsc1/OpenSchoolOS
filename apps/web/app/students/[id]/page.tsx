import Link from "next/link";
import { api } from "../../../lib/api";
import NewLearningCaseForm from "./NewLearningCaseForm";

export default async function StudentDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  let cases: Awaited<ReturnType<typeof api.listLearningCases>> = [];
  let error: string | null = null;
  try {
    cases = await api.listLearningCases(id);
  } catch (e) {
    error = e instanceof Error ? e.message : "Failed to load cases.";
  }

  return (
    <main className="mx-auto max-w-2xl p-6">
      <Link href="/" className="text-sm text-neutral-500 hover:underline">
        ← Students
      </Link>
      <h1 className="mt-2 text-2xl font-semibold">Learning Cases</h1>
      <p className="mt-1 text-sm text-neutral-600">
        Every active struggle for this learner.
      </p>

      {error && (
        <p className="mt-4 rounded bg-red-50 p-3 text-sm text-red-700">{error}</p>
      )}

      <ul className="mt-6 divide-y border rounded">
        {cases.map((c) => (
          <li key={c.id} className="p-3">
            <Link href={`/learning-cases/${c.id}`} className="hover:underline">
              <div className="font-medium">{c.subject}</div>
              <div className="text-sm text-neutral-500">
                Root gap: {c.possible_root_gap}
              </div>
              <div className="text-sm text-neutral-500">Status: {c.status}</div>
            </Link>
          </li>
        ))}
        {cases.length === 0 && !error && (
          <li className="p-3 text-sm text-neutral-500">No learning cases yet.</li>
        )}
      </ul>

      <NewLearningCaseForm studentId={id} />
    </main>
  );
}
