// @openschoolos/domain — Observation repository interface (Sprint 001).
// Pure domain contract. No ORM, no SQL. Infrastructure implements this.

import type { Observation, ObservationId } from "./observation";
import type { LearningCaseId } from "./learning-case";

export interface NewObservation {
  id: ObservationId;
  learningCaseId: LearningCaseId;
  observed: string;
  possibleRootGap: string;
  evidence: string;
  strategy: string;
  nextReview: string;
}

export interface ObservationRepository {
  save(observation: Observation): Promise<void> | void;
  nextIdentity(): ObservationId;
  getById(id: ObservationId): Observation | undefined;
  listByCase(learningCaseId: LearningCaseId): Observation[];
}
