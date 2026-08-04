import type { Metadata } from "next";
import Link from "next/link";
import { api } from "../lib/api";
import NewStudentForm from "./NewStudentForm";
import BulkImport from "./BulkImport";
import StudentSearch from "./StudentSearch";

export const metadata: Metadata = {
  title: "OpenSchoolOS — Students",
};

export default async function StudentsPage({
  searchParams,
}: {
  searchParams: Promise<{ q?: string }>;
}) {
  const { q } = await searchParams;
  let students: Awaited<ReturnType<typeof api.listStudents>> = [];
  let error: string | null = null;
  try {
    students = await api.listStudents(q || undefined);
  } catch (e) {
    error = e instanceof Error ? e.message : "Failed to load students.";
  }

  return (
    <main className="mx-auto max-w-2xl p-6">
      <h1 className="text-2xl font-semibold">Students</h1>
      <p className="mt-1 text-sm text-neutral-600">
        One learner at a time. Search, then open a case.
      </p>

      <StudentSearch defaultValue={q} />

      {error && (
        <p className="mt-4 rounded bg-red-50 p-3 text-sm text-red-700">
          {error}
        </p>
      )}

      <ul className="mt-4 divide-y border rounded">
        {students.map((s) => (
          <li key={s.id} className="p-3">
            <Link
              href={`/students/${s.id}`}
              className="flex items-center justify-between hover:underline"
            >
              <span>
                <span className="font-medium">{s.full_name}</span>
                <span className="ml-2 text-sm text-neutral-500">
                  Grade {s.grade}
                  {s.section} &middot; Roll {s.roll_number}
                </span>
              </span>
              <span className="text-sm text-neutral-400">{s.status}</span>
            </Link>
          </li>
        ))}
        {students.length === 0 && !error && (
          <li className="p-3 text-sm text-neutral-500">
            {q ? "No students match your search." : "No students yet."}
          </li>
        )}
      </ul>

      <NewStudentForm />
      <BulkImport />
    </main>
  );
}
