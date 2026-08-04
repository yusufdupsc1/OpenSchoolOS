import Link from "next/link";
import { api } from "../../../lib/api";
import NewLearningCaseForm from "./NewLearningCaseForm";
import EditStudentForm from "./EditStudentForm";
import DeleteStudentButton from "./DeleteStudentButton";
import type { LearningCaseOut, TimelineEntry } from "../../../lib/api";

async function StudentDetailPageContent({
  studentId,
}: {
  studentId: string;
}) {
  let student: Awaited<ReturnType<typeof api.getStudent>> | null = null;
  let cases: LearningCaseOut[] = [];
  let timeline: TimelineEntry[] = [];
  let error: string | null = null;

  try {
    [student, cases, timeline] = await Promise.all([
      api.getStudent(studentId),
      api.listLearningCases({ student_id: studentId }),
      api.studentTimeline(studentId),
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
        <p className="mt-4 rounded bg-red-50 p-3 text-sm text-red-700">
          {error}
        </p>
      </main>
    );
  }

  if (!student) {
    return (
      <main className="mx-auto max-w-2xl p-6">
        <Link href="/" className="text-sm text-neutral-500 hover:underline">
          &larr; Students
        </Link>
        <p className="mt-4 text-sm text-neutral-500">Student not found.</p>
      </main>
    );
  }

  return (
    <main className="mx-auto max-w-2xl p-6">
      <Link href="/" className="text-sm text-neutral-500 hover:underline">
        &larr; Students
      </Link>

      {/* Student header */}
      <div className="mt-2 flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-semibold">{student.full_name}</h1>
          <p className="text-sm text-neutral-500">
            Grade {student.grade}
            {student.section} &middot; Roll {student.roll_number} &middot;{" "}
            <span
              className={
                student.status === "active" ? "text-green-600" : "text-neutral-400"
              }
            >
              {student.status}
            </span>
          </p>
        </div>
        <div className="flex gap-2">
          <EditStudentForm student={student} />
          <DeleteStudentButton studentId={student.id} />
        </div>
      </div>

      <h2 className="mt-8 text-lg font-semibold">Learning Cases</h2>
      <p className="mt-1 text-sm text-neutral-600">
        Every active struggle for this learner.
      </p>

      <ul className="mt-4 divide-y border rounded">
        {cases.map((c) => (
          <li key={c.id} className="p-3">
            <Link
              href={`/learning-cases/${c.id}`}
              className="hover:underline"
            >
              <div className="font-medium">
                {c.subject} &mdash; {c.competency}
              </div>
              <div className="text-sm text-neutral-500">
                Root gap: {c.possible_root_gap}
              </div>
              <div className="text-sm">
                <span
                  className={
                    c.status === "open" ? "text-green-600" : "text-neutral-400"
                  }
                >
                  {c.status}
                </span>
              </div>
            </Link>
          </li>
        ))}
        {cases.length === 0 && (
          <li className="p-3 text-sm text-neutral-500">
            No learning cases yet.
          </li>
        )}
      </ul>

      <NewLearningCaseForm studentId={studentId} />

      {/* Timeline */}
      {timeline.length > 0 && (
        <>
          <h2 className="mt-8 text-lg font-semibold">Observation Timeline</h2>
          <p className="mt-1 text-sm text-neutral-600">
            All recorded observations across cases, newest first.
          </p>
          <ul className="mt-4 divide-y border rounded">
            {timeline.map((entry) => (
              <li key={entry.id} className="p-3">
                <div className="flex items-center gap-2 text-xs text-neutral-400">
                  <span className="font-medium">{entry.case_subject}</span>
                  {entry.created_at && (
                    <span>
                      {new Date(entry.created_at).toLocaleDateString()}
                    </span>
                  )}
                </div>
                <div className="mt-1 font-medium">{entry.observed}</div>
                <div className="text-sm text-neutral-500">
                  Gap: {entry.possible_root_gap} &middot; Strategy:{" "}
                  {entry.strategy}
                </div>
              </li>
            ))}
          </ul>
        </>
      )}
    </main>
  );
}

export default async function StudentDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  return <StudentDetailPageContent studentId={id} />;
}
