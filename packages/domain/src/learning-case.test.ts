// @openschoolos/domain — LearningCase aggregate unit tests (Sprint 001).
import { describe, it, expect } from "vitest";
import { LearningCase, LearningCaseId } from "./learning-case";
import { StudentId } from "./student";
import { DomainError } from "./errors";

const studentId = StudentId.create("S-001");

const base = {
  id: LearningCaseId.create("LC-001"),
  studentId,
  subject: "Mathematics",
  competency: "Fractions",
  possibleRootGap: "Place value",
  evidence: "Counts 1,2,3 but cannot compare 1/2 and 1/4",
  strategy: "Use physical fraction tiles for two weeks",
  nextReview: "2026-08-01",
};

describe("LearningCase creation", () => {
  it("opens a valid case with required fields", () => {
    const lc = LearningCase.open(base);
    expect(lc.subject).toBe("Mathematics");
    expect(lc.competency).toBe("Fractions");
    expect(lc.possibleRootGap).toBe("Place value");
    expect(lc.evidence).toBe("Counts 1,2,3 but cannot compare 1/2 and 1/4");
    expect(lc.strategy).toBe("Use physical fraction tiles for two weeks");
    expect(lc.nextReview).toBe("2026-08-01");
    expect(lc.status).toBe("open");
    expect(lc.studentId.equals(studentId)).toBe(true);
  });

  it("trims whitespace from inputs", () => {
    const lc = LearningCase.open({ ...base, subject: "  Math ", strategy: " tiles " });
    expect(lc.subject).toBe("Math");
    expect(lc.strategy).toBe("tiles");
  });
});

describe("Invalid data", () => {
  it("rejects empty subject", () => {
    expect(() => LearningCase.open({ ...base, subject: "" })).toThrow(DomainError);
  });
  it("rejects empty competency", () => {
    expect(() => LearningCase.open({ ...base, competency: "" })).toThrow(DomainError);
  });
  it("rejects empty possible root gap", () => {
    expect(() => LearningCase.open({ ...base, possibleRootGap: "" })).toThrow(DomainError);
  });
  it("rejects empty evidence", () => {
    expect(() => LearningCase.open({ ...base, evidence: "" })).toThrow(DomainError);
  });
  it("rejects empty strategy", () => {
    expect(() => LearningCase.open({ ...base, strategy: "" })).toThrow(DomainError);
  });
  it("rejects empty next review", () => {
    expect(() => LearningCase.open({ ...base, nextReview: "" })).toThrow(DomainError);
  });
});

describe("Business rules", () => {
  it("identity (id) is immutable", () => {
    const lc = LearningCase.open(base);
    const original = lc.id;
    lc.reviseStrategy("New plan");
    lc.close();
    expect(lc.id).toBe(original);
  });

  it("reviseStrategy updates strategy and rejects empty", () => {
    const lc = LearningCase.open(base);
    lc.reviseStrategy("Daily 5-minute drill");
    expect(lc.strategy).toBe("Daily 5-minute drill");
    expect(() => lc.reviseStrategy("  ")).toThrow(DomainError);
  });

  it("reviseRootGap updates the gap and rejects empty", () => {
    const lc = LearningCase.open(base);
    lc.reviseRootGap("Number line");
    expect(lc.possibleRootGap).toBe("Number line");
    expect(() => lc.reviseRootGap("")).toThrow(DomainError);
  });

  it("close marks the case closed", () => {
    const lc = LearningCase.open(base);
    expect(lc.status).toBe("open");
    lc.close();
    expect(lc.status).toBe("closed");
  });

  it("equality is by identity", () => {
    const a = LearningCase.open(base);
    const b = LearningCase.open({ ...base, strategy: "Different" });
    expect(a.equals(b)).toBe(true);
  });

  it("links to the correct student by identity", () => {
    const lc = LearningCase.open(base);
    expect(lc.studentId.equals(StudentId.create("S-001"))).toBe(true);
    expect(lc.studentId.equals(StudentId.create("S-999"))).toBe(false);
  });
});

describe("LearningCaseId", () => {
  it("creates trimmed, non-empty id", () => {
    expect(LearningCaseId.create("  LC-1  ").toString()).toBe("LC-1");
  });
  it("throws on empty", () => {
    expect(() => LearningCaseId.create("")).toThrow(DomainError);
  });
  it("equals by value", () => {
    expect(LearningCaseId.create("LC-1").equals(LearningCaseId.create("LC-1"))).toBe(true);
  });
});
