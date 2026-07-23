// @openschoolos/domain — domain errors (Sprint 001).
// Pure domain. Thrown when an invariant is violated.

export class DomainError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "DomainError";
  }
}
