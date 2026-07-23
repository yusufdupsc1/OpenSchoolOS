// @openschoolos/domain — Student aggregate (Sprint 001).
// Pure domain. No ORM, no framework, no I/O.
//
// A Student is one learner. Identity (StudentId) is immutable once assigned.
// The aggregate guards its own invariants; cross-aggregate rules (e.g. roll
// number uniqueness within a class) are enforced by the repository, which
// raises DomainError on violation.

import { DomainError } from "./errors";

export class StudentId {
  private constructor(private readonly value: string) {}

  static create(value: string): StudentId {
    if (!value || value.trim().length === 0) {
      throw new DomainError("StudentId cannot be empty.");
    }
    return new StudentId(value.trim());
  }

  equals(other: StudentId): boolean {
    return this.value === other.value;
  }

  toString(): string {
    return this.value;
  }
}

export type StudentStatus = "active" | "inactive" | "graduated" | "transferred";

export interface StudentProps {
  id: StudentId;
  fullName: string;
  rollNumber: string;
  grade: string;
  section: string;
  status: StudentStatus;
}

export class Student {
  private constructor(private readonly props: StudentProps) {}

  static create(input: {
    id: StudentId;
    fullName: string;
    rollNumber: string;
    grade: string;
    section: string;
    status?: StudentStatus;
  }): Student {
    const fullName = input.fullName?.trim() ?? "";
    const rollNumber = input.rollNumber?.trim() ?? "";
    const grade = input.grade?.trim() ?? "";
    const section = input.section?.trim() ?? "";

    if (fullName.length === 0) {
      throw new DomainError("Student full name cannot be empty.");
    }
    if (rollNumber.length === 0) {
      throw new DomainError("Student roll number cannot be empty.");
    }
    if (grade.length === 0) {
      throw new DomainError("Student grade cannot be empty.");
    }
    if (section.length === 0) {
      throw new DomainError("Student section cannot be empty.");
    }

    return new Student({
      id: input.id,
      fullName,
      rollNumber,
      grade,
      section,
      status: input.status ?? "active",
    });
  }

  get id(): StudentId {
    return this.props.id;
  }

  get fullName(): string {
    return this.props.fullName;
  }

  get rollNumber(): string {
    return this.props.rollNumber;
  }

  get grade(): string {
    return this.props.grade;
  }

  get section(): string {
    return this.props.section;
  }

  get status(): StudentStatus {
    return this.props.status;
  }

  // Identity is immutable. RollNumber/grade/section may change, but the
  // StudentId (and therefore who this learner is) cannot.
  changeSection(section: string): void {
    const next = section?.trim() ?? "";
    if (next.length === 0) {
      throw new DomainError("Student section cannot be empty.");
    }
    this.props.section = next;
  }

  setStatus(status: StudentStatus): void {
    this.props.status = status;
  }

  equals(other: Student): boolean {
    return this.props.id.equals(other.props.id);
  }
}
