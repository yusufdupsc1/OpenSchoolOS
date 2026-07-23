// @openschoolos/domain — LearningCase repository interface (Sprint 001).
// Pure domain contract. No ORM, no SQL. Infrastructure implements this.

import type { LearningCase, LearningCaseId, LearningCaseStatus } from "./learning-case";
import type { StudentId } from "./student";

export interface NewLearningCase {
  id: LearningCaseId;
  studentId: StudentId;
  subject: string;
  competency: string;
  possibleRootGap: string;
  evidence: string;
  strategy: string;
  nextReview: string;
}

export interface LearningCaseRepository {
  save(learningCase: LearningCase): Promise<void> | void;
  nextIdentity(): LearningCaseId;
  getById(id: LearningCaseId): LearningCase | undefined;
  listByStudent(studentId: StudentId): LearningCase[];
  listByStatus(status: LearningCaseStatus): LearningCase[];
}
