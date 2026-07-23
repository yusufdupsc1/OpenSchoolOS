// @openschoolos/domain — Observation aggregate (Sprint 001).
// Pure domain. No ORM, no framework, no I/O.
//
// An Observation is ONE recorded moment in the Educational Loop for ONE case.
// It captures what the teacher saw (observed), the root gap identified in this
// moment, the evidence that confirms it, the strategy (intervention) chosen,
// and when to look again. Observations accumulate inside a case; as they do,
// the teacher's hypothesis changes and the loop turns.
//
// Identity (ObservationId) is immutable. The link to a case (LearningCaseId)
// is fixed for the life of the observation.

import { DomainError } from "./errors";
import type { LearningCaseId } from "./learning-case";

export class ObservationId {
  private constructor(private readonly value: string) {}

  static create(value: string): ObservationId {
    if (!value || value.trim().length === 0) {
      throw new DomainError("ObservationId cannot be empty.");
    }
    return new ObservationId(value.trim());
  }

  equals(other: ObservationId): boolean {
    return this.value === other.value;
  }

  toString(): string {
    return this.value;
  }
}

export interface ObservationProps {
  id: ObservationId;
  learningCaseId: LearningCaseId;
  observed: string;
  possibleRootGap: string;
  evidence: string;
  strategy: string;
  nextReview: string;
}

export class Observation {
  private constructor(private readonly props: ObservationProps) {}

  static record(input: {
    id: ObservationId;
    learningCaseId: LearningCaseId;
    observed: string;
    possibleRootGap: string;
    evidence: string;
    strategy: string;
    nextReview: string;
  }): Observation {
    const observed = input.observed?.trim() ?? "";
    const possibleRootGap = input.possibleRootGap?.trim() ?? "";
    const evidence = input.evidence?.trim() ?? "";
    const strategy = input.strategy?.trim() ?? "";
    const nextReview = input.nextReview?.trim() ?? "";

    if (observed.length === 0) {
      throw new DomainError("Observation observed cannot be empty.");
    }
    if (possibleRootGap.length === 0) {
      throw new DomainError("Observation possible root gap cannot be empty.");
    }
    if (evidence.length === 0) {
      throw new DomainError("Observation evidence cannot be empty.");
    }
    if (strategy.length === 0) {
      throw new DomainError("Observation strategy cannot be empty.");
    }
    if (nextReview.length === 0) {
      throw new DomainError("Observation next review cannot be empty.");
    }

    return new Observation({
      id: input.id,
      learningCaseId: input.learningCaseId,
      observed,
      possibleRootGap,
      evidence,
      strategy,
      nextReview,
    });
  }

  get id(): ObservationId {
    return this.props.id;
  }

  get learningCaseId(): LearningCaseId {
    return this.props.learningCaseId;
  }

  get observed(): string {
    return this.props.observed;
  }

  get possibleRootGap(): string {
    return this.props.possibleRootGap;
  }

  get evidence(): string {
    return this.props.evidence;
  }

  get strategy(): string {
    return this.props.strategy;
  }

  get nextReview(): string {
    return this.props.nextReview;
  }

  // The teacher's thinking may shift between observations. These are the
  // revisable fields of a single recorded moment.
  reviseStrategy(strategy: string): void {
    const next = strategy?.trim() ?? "";
    if (next.length === 0) {
      throw new DomainError("Observation strategy cannot be empty.");
    }
    this.props.strategy = next;
  }

  reviseRootGap(possibleRootGap: string): void {
    const next = possibleRootGap?.trim() ?? "";
    if (next.length === 0) {
      throw new DomainError("Observation possible root gap cannot be empty.");
    }
    this.props.possibleRootGap = next;
  }

  equals(other: Observation): boolean {
    return this.props.id.equals(other.props.id);
  }
}
