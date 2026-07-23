// OpenSchoolOS web — typed API client (Sprint 001).
// Thin boundary to the FastAPI backend. No domain logic here.
const BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export interface StudentOut {
  id: string;
  full_name: string;
  roll_number: string;
  grade: string;
  section: string;
  status: string;
  created_at: string | null;
}

export interface LearningCaseOut {
  id: string;
  student_id: string;
  subject: string;
  competency: string;
  possible_root_gap: string;
  evidence: string;
  strategy: string;
  next_review: string;
  status: string;
  created_at: string | null;
}

export interface ObservationOut {
  id: string;
  learning_case_id: string;
  observed: string;
  possible_root_gap: string;
  evidence: string;
  strategy: string;
  next_review: string;
  created_at: string | null;
}

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`, { cache: "no-store" });
  if (!res.ok) {
    throw new Error(`Request failed: ${res.status}`);
  }
  return res.json() as Promise<T>;
}

export interface ObservationCreate {
  learning_case_id: string;
  observed: string;
  possible_root_gap: string;
  evidence: string;
  strategy: string;
  next_review: string;
}

async function post<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    cache: "no-store",
  });
  if (!res.ok) {
    throw new Error(`Request failed: ${res.status}`);
  }
  return res.json() as Promise<T>;
}

export interface LearningCaseCreate {
  student_id: string;
  subject: string;
  competency: string;
  possible_root_gap: string;
  evidence: string;
  strategy: string;
  next_review: string;
}

export interface StudentCreate {
  full_name: string;
  roll_number: string;
  grade: string;
  section: string;
}

export const api = {
  listStudents: () => get<StudentOut[]>("/students"),
  listLearningCases: (studentId?: string) =>
    get<LearningCaseOut[]>(
      studentId ? `/learning-cases?student_id=${encodeURIComponent(studentId)}` : "/learning-cases"
    ),
  listObservations: (learningCaseId?: string) =>
    get<ObservationOut[]>(
      learningCaseId
        ? `/observations?learning_case_id=${encodeURIComponent(learningCaseId)}`
        : "/observations"
    ),
  createObservation: (body: ObservationCreate) =>
    post<ObservationOut>("/observations", body),
  createLearningCase: (body: LearningCaseCreate) =>
    post<LearningCaseOut>("/learning-cases", body),
  createStudent: (body: StudentCreate) => post<StudentOut>("/students", body),
};
