// @openschoolos/domain — LearningCase aggregate (Sprint 001).
// Pure domain. No ORM, no framework, no I/O.
//
// A LearningCase is ONE active struggle for ONE student. It carries the
// teacher's current hypothesis: the possible root gap, the evidence that
// supports it, the strategy (intervention) chosen, and when to look again.
// The case opens and eventually closes. An intervention is part of the case
// (the strategy field), NOT a separate model.
//
// Identity (LearningCaseId) is immutable. The link to a student (StudentId)
// is fixed for the life of the case.

import { DomainError } from "./errors";
import type { StudentId } from "./student";

export class LearningCaseId {
  private constructor(private readonly value: string) {}

  static create(value: string): LearningCaseId {
    if (!value || value.trim().length === 0) {
      throw new DomainError("LearningCaseId cannot be empty.");
    }
    return new LearningCaseId(value.trim());
  }

  equals(other: LearningCaseId): boolean {
    return this.value === other.value;
  }

  toString(): string {
    return this.value;
  }
}

export type LearningCaseStatus = "open" | "closed";

export interface LearningCaseProps {
  id: LearningCaseId;
  studentId: StudentId;
  subject: string;
  competency: string;
  possibleRootGap: string;
  evidence: string;
  strategy: string;
  nextReview: string;
  status: LearningCaseStatus;
}

export class LearningCase {
  private constructor(private readonly props: LearningCaseProps) {}

  static open(input: {
    id: LearningCaseId;
    studentId: StudentId;
    subject: string;
    competency: string;
    possibleRootGap: string;
    evidence: string;
    strategy: string;
    nextReview: string;
  }): LearningCase {
    const subject = input.subject?.trim() ?? "";
    const competency = input.competency?.trim() ?? "";
    const possibleRootGap = input.possibleRootGap?.trim() ?? "";
    const evidence = input.evidence?.trim() ?? "";
    const strategy = input.strategy?.trim() ?? "";
    const nextReview = input.nextReview?.trim() ?? "";

    if (subject.length === 0) {
      throw new DomainError("LearningCase subject cannot be empty.");
    }
    if (competency.length === 0) {
      throw new DomainError("LearningCase competency cannot be empty.");
    }
    if (possibleRootGap.length === 0) {
      throw new DomainError("LearningCase possible root gap cannot be empty.");
    }
    if (evidence.length === 0) {
      throw new DomainError("LearningCase evidence cannot be empty.");
    }
    if (strategy.length === 0) {
      throw new DomainError("LearningCase strategy cannot be empty.");
    }
    if (nextReview.length === 0) {
      throw new DomainError("LearningCase next review cannot be empty.");
    }

    return new LearningCase({
      id: input.id,
      studentId: input.studentId,
      subject,
      competency,
      possibleRootGap,
      evidence,
      strategy,
      nextReview,
      status: "open",
    });
  }

  get id(): LearningCaseId {
    return this.props.id;
  }

  get studentId(): StudentId {
    return this.props.studentId;
  }

  get subject(): string {
    return this.props.subject;
  }

  get competency(): string {
    return this.props.competency;
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

  get status(): LearningCaseStatus {
    return this.props.status;
  }

  // Strategy (intervention) may be revised as the teacher's thinking changes.
  reviseStrategy(strategy: string): void {
    const next = strategy?.trim() ?? "";
    if (next.length === 0) {
      throw new DomainError("LearningCase strategy cannot be empty.");
    }
    this.props.strategy = next;
  }

  reviseRootGap(possibleRootGap: string): void {
    const next = possibleRootGap?.trim() ?? "";
    if (next.length === 0) {
      throw new DomainError("LearningCase possible root gap cannot be empty.");
    }
    this.props.possibleRootGap = next;
  }

  close(): void {
    this.props.status = "closed";
  }

  equals(other: LearningCase): boolean {
    return this.props.id.equals(other.props.id);
  }
}
