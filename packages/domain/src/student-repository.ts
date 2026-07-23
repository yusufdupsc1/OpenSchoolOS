// @openschoolos/domain — Student repository interface (Sprint 001).
// Pure domain contract. No ORM, no SQL. Infrastructure implements this.
//
// Roll number uniqueness within a class is a repository invariant: the
// implementation must reject a duplicate (grade, section, rollNumber) with
// DomainError. The aggregate itself stays pure.

import type { Student, StudentId, StudentStatus } from "./student";
import type { DomainError } from "./errors";

export interface NewStudent {
  id: StudentId;
  fullName: string;
  rollNumber: string;
  grade: string;
  section: string;
  status?: StudentStatus;
}

export interface StudentRepository {
  save(student: Student): Promise<void> | void;
  // Throws DomainError if a student with the same (grade, section, rollNumber)
  // already exists.
  nextIdentity(): StudentId;
  getById(id: StudentId): Student | undefined;
  list(): Student[];
  listByClass(grade: string, section: string): Student[];
}
