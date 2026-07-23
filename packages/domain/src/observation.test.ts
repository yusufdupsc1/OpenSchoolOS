// @openschoolos/domain — Observation aggregate unit tests (Sprint 001).
import { describe, it, expect } from "vitest";
import { Observation, ObservationId } from "./observation";
import { LearningCaseId } from "./learning-case";
import { DomainError } from "./errors";

const caseId = LearningCaseId.create("LC-001");

const base = {
  id: ObservationId.create("OB-001"),
  learningCaseId: caseId,
  observed: "Counted 12 counters but wrote 21",
  possibleRootGap: "Place value",
  evidence: "Consistently reverses two-digit numbers",
  strategy: "Build tens and ones with base-10 blocks",
  nextReview: "2026-08-05",
};

describe("Observation recording", () => {
  it("records a valid observation with required fields", () => {
    const o = Observation.record(base);
    expect(o.observed).toBe("Counted 12 counters but wrote 21");
    expect(o.possibleRootGap).toBe("Place value");
    expect(o.evidence).toBe("Consistently reverses two-digit numbers");
    expect(o.strategy).toBe("Build tens and ones with base-10 blocks");
    expect(o.nextReview).toBe("2026-08-05");
    expect(o.learningCaseId.equals(caseId)).toBe(true);
  });

  it("trims whitespace from inputs", () => {
    const o = Observation.record({ ...base, observed: "  saw this ", strategy: " blocks " });
    expect(o.observed).toBe("saw this");
    expect(o.strategy).toBe("blocks");
  });
});

describe("Invalid data", () => {
  it("rejects empty observed", () => {
    expect(() => Observation.record({ ...base, observed: "" })).toThrow(DomainError);
  });
  it("rejects empty possible root gap", () => {
    expect(() => Observation.record({ ...base, possibleRootGap: "" })).toThrow(DomainError);
  });
  it("rejects empty evidence", () => {
    expect(() => Observation.record({ ...base, evidence: "" })).toThrow(DomainError);
  });
  it("rejects empty strategy", () => {
    expect(() => Observation.record({ ...base, strategy: "" })).toThrow(DomainError);
  });
  it("rejects empty next review", () => {
    expect(() => Observation.record({ ...base, nextReview: "" })).toThrow(DomainError);
  });
});

describe("Business rules", () => {
  it("identity (id) is immutable", () => {
    const o = Observation.record(base);
    const original = o.id;
    o.reviseStrategy("New plan");
    expect(o.id).toBe(original);
  });

  it("reviseStrategy updates and rejects empty", () => {
    const o = Observation.record(base);
    o.reviseStrategy("Daily 5-minute drill");
    expect(o.strategy).toBe("Daily 5-minute drill");
    expect(() => o.reviseStrategy("  ")).toThrow(DomainError);
  });

  it("reviseRootGap updates and rejects empty", () => {
    const o = Observation.record(base);
    o.reviseRootGap("Number line");
    expect(o.possibleRootGap).toBe("Number line");
    expect(() => o.reviseRootGap("")).toThrow(DomainError);
  });

  it("equality is by identity", () => {
    const a = Observation.record(base);
    const b = Observation.record({ ...base, observed: "Different" });
    expect(a.equals(b)).toBe(true);
  });

  it("links to the correct case by identity", () => {
    const o = Observation.record(base);
    expect(o.learningCaseId.equals(LearningCaseId.create("LC-001"))).toBe(true);
    expect(o.learningCaseId.equals(LearningCaseId.create("LC-999"))).toBe(false);
  });
});

describe("ObservationId", () => {
  it("creates trimmed, non-empty id", () => {
    expect(ObservationId.create("  OB-1  ").toString()).toBe("OB-1");
  });
  it("throws on empty", () => {
    expect(() => ObservationId.create("")).toThrow(DomainError);
  });
  it("equals by value", () => {
    expect(ObservationId.create("OB-1").equals(ObservationId.create("OB-1"))).toBe(true);
  });
});
