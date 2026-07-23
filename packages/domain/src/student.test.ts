// @openschoolos/domain — Student aggregate unit tests (Sprint 001).
import { describe, it, expect } from "vitest";
import { Student, StudentId } from "./student";
import { DomainError } from "./errors";

describe("StudentId", () => {
  it("creates a trimmed, non-empty id", () => {
    const id = StudentId.create("  S-001  ");
    expect(id.toString()).toBe("S-001");
  });

  it("throws on empty id", () => {
    expect(() => StudentId.create("")).toThrow(DomainError);
    expect(() => StudentId.create("   ")).toThrow(DomainError);
  });

  it("equals by value", () => {
    expect(StudentId.create("S-1").equals(StudentId.create("S-1"))).toBe(true);
    expect(StudentId.create("S-1").equals(StudentId.create("S-2"))).toBe(false);
  });
});

describe("Student creation", () => {
  const base = {
    id: StudentId.create("S-001"),
    fullName: "Aisha Rahman",
    rollNumber: "12",
    grade: "5",
    section: "A",
  };

  it("creates a valid active student with minimal fields", () => {
    const s = Student.create(base);
    expect(s.fullName).toBe("Aisha Rahman");
    expect(s.rollNumber).toBe("12");
    expect(s.grade).toBe("5");
    expect(s.section).toBe("A");
    expect(s.status).toBe("active");
    expect(s.id.equals(StudentId.create("S-001"))).toBe(true);
  });

  it("trims whitespace from inputs", () => {
    const s = Student.create({
      ...base,
      fullName: "  Aisha  ",
      rollNumber: " 12 ",
    });
    expect(s.fullName).toBe("Aisha");
    expect(s.rollNumber).toBe("12");
  });

  it("honors an explicit status", () => {
    const s = Student.create({ ...base, status: "inactive" });
    expect(s.status).toBe("inactive");
  });
});

describe("Invalid data", () => {
  const base = {
    id: StudentId.create("S-001"),
    fullName: "Aisha Rahman",
    rollNumber: "12",
    grade: "5",
    section: "A",
  };

  it("rejects empty full name", () => {
    expect(() => Student.create({ ...base, fullName: "" })).toThrow(DomainError);
    expect(() => Student.create({ ...base, fullName: "   " })).toThrow(DomainError);
  });

  it("rejects empty roll number", () => {
    expect(() => Student.create({ ...base, rollNumber: "" })).toThrow(DomainError);
  });

  it("rejects empty grade", () => {
    expect(() => Student.create({ ...base, grade: "" })).toThrow(DomainError);
  });

  it("rejects empty section", () => {
    expect(() => Student.create({ ...base, section: "" })).toThrow(DomainError);
  });
});

describe("Business rules", () => {
  const base = {
    id: StudentId.create("S-001"),
    fullName: "Aisha Rahman",
    rollNumber: "12",
    grade: "5",
    section: "A",
  };

  it("identity (id) is immutable", () => {
    const s = Student.create(base);
    const original = s.id;
    s.changeSection("B");
    s.setStatus("graduated");
    expect(s.id).toBe(original);
    expect(s.id.equals(StudentId.create("S-001"))).toBe(true);
  });

  it("changeSection updates section and rejects empty", () => {
    const s = Student.create(base);
    s.changeSection("C");
    expect(s.section).toBe("C");
    expect(() => s.changeSection("  ")).toThrow(DomainError);
  });

  it("setStatus updates status", () => {
    const s = Student.create(base);
    s.setStatus("transferred");
    expect(s.status).toBe("transferred");
  });

  it("equality is by identity, not attributes", () => {
    const a = Student.create(base);
    const b = Student.create({ ...base, fullName: "Different Name" });
    expect(a.equals(b)).toBe(true); // same id => same student
  });
});
