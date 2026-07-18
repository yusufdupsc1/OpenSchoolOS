export interface Student {
  id: number;
  name: string;
  createdAt: string;
  updatedAt: string;
}

export type LearningCaseStatus = "open" | "closed";

export interface LearningCase {
  id: number;
  studentId: number;
  subject: string;
  competency: string;
  possibleRootGap: string;
  evidence: string;
  strategy: string;
  nextReview: string;
  status: LearningCaseStatus;
  createdAt: string;
  updatedAt: string;
}

export interface Observation {
  id: number;
  learningCaseId: number;
  observed: string;
  possibleRootGap: string;
  evidence: string;
  strategy: string;
  nextReview: string;
  createdAt: string;
}

export interface StudentRepository {
  create(input: { name: string }): Student;
  getById(id: number): Student | undefined;
  list(): Student[];
}

export interface LearningCaseRepository {
  create(input: Omit<LearningCase, "id" | "createdAt" | "updatedAt" | "status"> & { status?: LearningCaseStatus }): LearningCase;
  getById(id: number): LearningCase | undefined;
  listByStudent(studentId: number): LearningCase[];
}

export interface ObservationRepository {
  create(input: Omit<Observation, "id" | "createdAt">): Observation;
  getById(id: number): Observation | undefined;
  listByCase(learningCaseId: number): Observation[];
}
