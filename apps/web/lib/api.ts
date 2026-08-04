// OpenSchoolOS web — typed API client (Sprint 004).
const BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export interface StudentOut { id: string; full_name: string; roll_number: string; grade: string; section: string; status: string; created_at: string | null; deleted_at: string | null; }
export interface LearningCaseOut { id: string; student_id: string; subject: string; competency: string; possible_root_gap: string; evidence: string; strategy: string; next_review: string; status: string; reflection: string | null; closed_at: string | null; created_at: string | null; deleted_at: string | null; }
export interface ObservationOut { id: string; learning_case_id: string; observed: string; possible_root_gap: string; evidence: string; evidence_strength: string | null; strategy: string; confidence: string | null; alternative_hypotheses: string | null; next_review: string; created_at: string | null; deleted_at: string | null; }
export interface TimelineEntry { type: string; id: string; case_id: string; case_subject: string; observed: string; possible_root_gap: string; evidence: string; evidence_strength: string | null; strategy: string; confidence: string | null; alternative_hypotheses: string | null; next_review: string; created_at: string | null; }
export interface ReasoningSnapshot { observation_id: string; index: number; observed: string; root_gap: string; evidence: string; evidence_strength: string | null; strategy: string; confidence: string | null; alternative_hypotheses: string | null; created_at: string | null; root_gap_changed: boolean; strategy_changed: boolean; confidence_changed: boolean; }
export interface ReasoningTimeline { case_id: string; subject: string; competency: string; current_root_gap: string; current_strategy: string; status: string; snapshots: ReasoningSnapshot[]; }
export interface BulkImportResult { created: number; errors: string[]; }

function authHeaders(): Record<string,string> { if (typeof window !== "undefined") { const t = localStorage.getItem("token"); if (t) return { Authorization: `Bearer ${t}` }; } return {}; }
async function get<T>(path: string): Promise<T> { const r = await fetch(`${BASE}${path}`, { cache: "no-store", headers: authHeaders() }); if (!r.ok) throw new Error(`Request failed: ${r.status}`); return r.json() as Promise<T>; }
async function post<T>(path: string, body?: unknown): Promise<T> { const isFd = body instanceof FormData; const h = isFd ? { ...authHeaders() } : { "Content-Type": "application/json", ...authHeaders() }; const r = await fetch(`${BASE}${path}`, { method: "POST", headers: h, body: isFd ? (body as FormData) : JSON.stringify(body), cache: "no-store" }); if (!r.ok) { const d = await r.json().catch(() => ({})); throw new Error((d as { detail?: string }).detail ?? `Request failed: ${r.status}`); } return r.json() as Promise<T>; }
async function patch<T>(path: string, body?: unknown): Promise<T> { const r = await fetch(`${BASE}${path}`, { method: "PATCH", headers: { "Content-Type": "application/json", ...authHeaders() }, body: JSON.stringify(body || {}), cache: "no-store" }); if (!r.ok) { const d = await r.json().catch(() => ({})); throw new Error((d as { detail?: string }).detail ?? `Request failed: ${r.status}`); } return r.json() as Promise<T>; }
async function del(path: string): Promise<void> { const r = await fetch(`${BASE}${path}`, { method: "DELETE", cache: "no-store", headers: authHeaders() }); if (!r.ok) throw new Error(`Request failed: ${r.status}`); }

export interface StudentCreate { full_name: string; roll_number: string; grade: string; section: string; }
export interface StudentUpdate { full_name?: string; roll_number?: string; grade?: string; section?: string; status?: string; }
export interface LearningCaseCreate { student_id: string; subject: string; competency: string; possible_root_gap: string; evidence: string; strategy: string; next_review: string; }
export interface LearningCaseUpdate { subject?: string; competency?: string; possible_root_gap?: string; evidence?: string; strategy?: string; next_review?: string; reflection?: string; }
export interface ObservationCreate { learning_case_id: string; observed: string; possible_root_gap: string; evidence: string; evidence_strength?: string; strategy: string; confidence?: string; alternative_hypotheses?: string; next_review: string; }
export interface ObservationUpdate { observed?: string; possible_root_gap?: string; evidence?: string; evidence_strength?: string; strategy?: string; confidence?: string; alternative_hypotheses?: string; next_review?: string; }

export const api = {
  login: (email: string, password: string) => post<{ access_token: string; user: { id: string; email: string; full_name: string } }>("/auth/login", { email, password }),
  register: (email: string, full_name: string, password: string) => post<{ access_token: string; user: { id: string; email: string; full_name: string } }>("/auth/register", { email, full_name, password }),
  getMe: () => get<{ id: string; email: string; full_name: string }>("/auth/me"),
  getHealth: () => get<{ status: string; db: string; student_count: number; case_count: number; observation_count: number; user_count: number }>("/health"),
  exportData: () => get<{ students: StudentOut[]; learning_cases: LearningCaseOut[]; observations: ObservationOut[] }>("/export"),
  getBackup: () => get<{ version: string; students: unknown[]; learning_cases: unknown[]; observations: unknown[]; users: unknown[] }>("/backup"),
  listStudents: (q?: string) => get<StudentOut[]>(q ? `/students?q=${encodeURIComponent(q)}` : "/students"),
  getStudent: (id: string) => get<StudentOut>(`/students/${id}`),
  createStudent: (body: StudentCreate) => post<StudentOut>("/students", body),
  updateStudent: (id: string, body: StudentUpdate) => patch<StudentOut>(`/students/${id}`, body),
  deleteStudent: (id: string) => del(`/students/${id}`),
  studentTimeline: (id: string) => get<TimelineEntry[]>(`/students/${id}/timeline`),
  importStudents: (file: File) => { const fd = new FormData(); fd.append("file", file); return post<BulkImportResult>("/students/import", fd); },

  listLearningCases: (params?: { student_id?: string; status?: string }) => { const qs = new URLSearchParams(); if (params?.student_id) qs.set("student_id", params.student_id); if (params?.status) qs.set("status", params.status); const s = qs.toString(); return get<LearningCaseOut[]>(s ? `/learning-cases?${s}` : "/learning-cases"); },
  getLearningCase: (id: string) => get<LearningCaseOut>(`/learning-cases/${id}`),
  createLearningCase: (body: LearningCaseCreate) => post<LearningCaseOut>("/learning-cases", body),
  updateLearningCase: (id: string, body: LearningCaseUpdate) => patch<LearningCaseOut>(`/learning-cases/${id}`, body),
  closeLearningCase: (id: string, reflection?: string, outcome?: string) => patch<LearningCaseOut>(`/learning-cases/${id}/close`, { reflection, outcome }),
  reopenLearningCase: (id: string) => patch<LearningCaseOut>(`/learning-cases/${id}/reopen`),
  transferLearningCase: (id: string, student_id: string) => post<LearningCaseOut>(`/learning-cases/${id}/transfer`, { student_id }),
  deleteLearningCase: (id: string) => del(`/learning-cases/${id}`),
  getReasoningTimeline: (id: string) => get<ReasoningTimeline>(`/learning-cases/${id}/reasoning-timeline`),

  listObservations: (lcId?: string) => get<ObservationOut[]>(lcId ? `/observations?learning_case_id=${encodeURIComponent(lcId)}` : "/observations"),
  getObservation: (id: string) => get<ObservationOut>(`/observations/${id}`),
  createObservation: (body: ObservationCreate) => post<ObservationOut>("/observations", body),
  updateObservation: (id: string, body: ObservationUpdate) => patch<ObservationOut>(`/observations/${id}`, body),
  deleteObservation: (id: string) => del(`/observations/${id}`),

  listSubjects: () => get<{ id: string; subject: string; description: string; competencyCount: number }[]>("/knowledge/subjects"),
  getSubject: (subj: string) => get<{ subject: string; description: string; competencies: Competency[]; dependencyGraph: Record<string, string[]> }>(`/knowledge/subjects/${subj}`),
  listCompetencies: (subj: string) => get<Competency[]>(`/knowledge/subjects/${subj}/competencies`),
  getCompetency: (subj: string, cid: string) => get<Competency>(`/knowledge/subjects/${subj}/competencies/${cid}`),
  searchCompetencies: (subj: string, q: string) => get<CompetencySearchResult[]>(`/knowledge/subjects/${subj}/search?q=${encodeURIComponent(q)}`),
  searchAllSubjects: (q: string) => get<CompetencySearchResult[]>(`/knowledge/search?q=${encodeURIComponent(q)}`),
  similarCases: (caseId: string, max?: number) => get<SimilarCasesResult>(`/ai/similar-cases/${caseId}${max ? `?max_results=${max}` : ""}`),
  observationSummary: (caseId: string) => get<ObservationSummary>(`/ai/observation-summary/${caseId}`),
  autocomplete: (q: string, source?: string) => get<AutocompleteResult>(`/ai/autocomplete?q=${encodeURIComponent(q)}${source ? `&source=${source}` : ""}`),
};

export interface Misconception { observed: string; rootGap: string; evidence: string; strategy: string; }
export interface Competency { id: string; label: string; description: string; gradeLevel: string; prerequisites: string[]; misconceptions: Misconception[]; }

export interface SimilarCaseEntry { case_id: string; student_id: string; student_name: string; subject: string; competency: string; possible_root_gap: string; strategy: string; status: string; outcome: string | null; similarity: string; observation_count: number; }
export interface SimilarCasesResult { source_case_id: string; source_root_gap: string; source_subject: string; results: SimilarCaseEntry[]; }
export interface ObservationSummary { case_id: string; subject: string; competency: string; student_name: string; observation_count: number; root_gap_progression: string[]; strategy_progression: string[]; confidence_progression: (string | null)[]; latest_observation: string | null; heuristic_summary: string; raw_context: string; }
export interface AutocompleteResult { matches: string[]; source: string; }
export interface CompetencySearchResult { competencyId?: string; competencyLabel?: string; subjectId?: string; subject?: string; description: string; gradeLevel: string; prerequisites: string[]; matchedMisconceptions?: Misconception[]; }
