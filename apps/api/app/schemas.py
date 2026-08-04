# OpenSchoolOS API — Pydantic schemas (Sprint 006).
from pydantic import BaseModel, Field

# ── Auth ─────────────────────────────────────────────────────────────────
class UserRegister(BaseModel):
    email: str = Field(min_length=3, max_length=255)
    full_name: str = Field(min_length=1)
    password: str = Field(min_length=6)
class UserLogin(BaseModel): email: str; password: str
class UserOut(BaseModel): id: str; email: str; full_name: str
class TokenOut(BaseModel): access_token: str; token_type: str = "bearer"; user: UserOut

# ── Student ─────────────────────────────────────────────────────────────
class StudentCreate(BaseModel):
    full_name: str = Field(min_length=1); roll_number: str = Field(min_length=1)
    grade: str = Field(min_length=1); section: str = Field(min_length=1)
class StudentUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=1)
    roll_number: str | None = Field(default=None, min_length=1)
    grade: str | None = Field(default=None, min_length=1)
    section: str | None = Field(default=None, min_length=1)
    status: str | None = None
class StudentOut(BaseModel):
    id: str; full_name: str; roll_number: str; grade: str; section: str
    status: str; teacher_id: str | None = None
    created_at: str | None = None; deleted_at: str | None = None
class BulkImportResult(BaseModel): created: int = 0; errors: list[str] = []

# ── Learning Case ───────────────────────────────────────────────────────
class LearningCaseCreate(BaseModel):
    student_id: str = Field(min_length=1); subject: str = Field(min_length=1)
    competency: str = Field(min_length=1); possible_root_gap: str = Field(min_length=1)
    evidence: str = Field(min_length=1); strategy: str = Field(min_length=1)
    next_review: str = Field(min_length=1)
class LearningCaseUpdate(BaseModel):
    subject: str | None = Field(default=None, min_length=1)
    competency: str | None = Field(default=None, min_length=1)
    possible_root_gap: str | None = Field(default=None, min_length=1)
    evidence: str | None = Field(default=None, min_length=1)
    strategy: str | None = Field(default=None, min_length=1)
    next_review: str | None = Field(default=None, min_length=1)
    reflection: str | None = None; outcome: str | None = None
class CloseCaseBody(BaseModel):
    reflection: str | None = None; outcome: str | None = None
class TransferCaseBody(BaseModel): student_id: str = Field(min_length=1)
class LearningCaseOut(BaseModel):
    id: str; student_id: str; subject: str; competency: str
    possible_root_gap: str; evidence: str; strategy: str; next_review: str
    status: str; reflection: str | None = None; outcome: str | None = None
    closed_at: str | None = None; created_at: str | None = None; deleted_at: str | None = None

# ── Observation ─────────────────────────────────────────────────────────
class ObservationCreate(BaseModel):
    learning_case_id: str = Field(min_length=1); observed: str = Field(min_length=1)
    possible_root_gap: str = Field(min_length=1); evidence: str = Field(min_length=1)
    evidence_strength: str | None = None; strategy: str = Field(min_length=1)
    confidence: str | None = None; alternative_hypotheses: str | None = None
    next_review: str = Field(min_length=1)
class ObservationUpdate(BaseModel):
    observed: str | None = Field(default=None, min_length=1)
    possible_root_gap: str | None = Field(default=None, min_length=1)
    evidence: str | None = Field(default=None, min_length=1)
    evidence_strength: str | None = None; strategy: str | None = Field(default=None, min_length=1)
    confidence: str | None = None; alternative_hypotheses: str | None = None
    next_review: str | None = Field(default=None, min_length=1)
class ObservationOut(BaseModel):
    id: str; learning_case_id: str; observed: str; possible_root_gap: str
    evidence: str; evidence_strength: str | None = None; strategy: str
    confidence: str | None = None; alternative_hypotheses: str | None = None
    next_review: str; created_at: str | None = None; deleted_at: str | None = None

# ── Timeline / Reasoning ────────────────────────────────────────────────
class TimelineEntry(BaseModel):
    type: str; id: str; case_id: str; case_subject: str; observed: str
    possible_root_gap: str; evidence: str; evidence_strength: str | None = None
    strategy: str; confidence: str | None = None
    alternative_hypotheses: str | None = None; next_review: str
    created_at: str | None = None
class ReasoningSnapshot(BaseModel):
    observation_id: str; index: int; observed: str; root_gap: str
    evidence: str; evidence_strength: str | None = None; strategy: str
    confidence: str | None = None; alternative_hypotheses: str | None = None
    created_at: str | None = None
    root_gap_changed: bool = False; strategy_changed: bool = False; confidence_changed: bool = False
class ReasoningTimeline(BaseModel):
    case_id: str; subject: str; competency: str
    current_root_gap: str; current_strategy: str; status: str
    snapshots: list[ReasoningSnapshot]

# ── Platform ─────────────────────────────────────────────────────────────
class HealthStatus(BaseModel):
    status: str; db: str; student_count: int; case_count: int
    observation_count: int; user_count: int = 0
class DataExport(BaseModel):
    students: list[StudentOut]; learning_cases: list[LearningCaseOut]
    observations: list[ObservationOut]

# ── Research / Analytics (Sprint 006) ────────────────────────────────────
class DurationMetrics(BaseModel):
    """Per-group duration stats in days."""
    group_key: str; group_label: str; count: int
    avg_days: float; min_days: float; max_days: float; median_days: float

class DurationReport(BaseModel):
    by_subject: list[DurationMetrics]
    by_grade: list[DurationMetrics]
    overall: DurationMetrics

class StrategyEffectiveness(BaseModel):
    strategy: str; count: int
    improved: int = 0; plateaued: int = 0; worsened: int = 0; unknown: int = 0

class OutcomeBreakdown(BaseModel):
    outcome: str; count: int

class ResearchDashboard(BaseModel):
    total_cases: int; open_cases: int; closed_cases: int
    total_observations: int
    avg_observations_per_case: float
    outcomes: list[OutcomeBreakdown]
    duration: DurationReport
    top_strategies: list[StrategyEffectiveness]
    cases_per_subject: list[dict]  # {subject: str, count: int}


# ── AI Extension Points (Sprint 007) ────────────────────────────────────

class SimilarCaseEntry(BaseModel):
    case_id: str
    student_id: str
    student_name: str
    subject: str
    competency: str
    possible_root_gap: str
    strategy: str
    status: str
    outcome: str | None = None
    similarity: str  # "same_root_gap" | "same_subject" | "same_strategy"
    observation_count: int = 0

class SimilarCasesResult(BaseModel):
    source_case_id: str
    source_root_gap: str
    source_subject: str
    results: list[SimilarCaseEntry]

class ObservationSummary(BaseModel):
    case_id: str
    subject: str
    competency: str
    student_name: str
    observation_count: int
    root_gap_progression: list[str]  # how root gap changed across obs
    strategy_progression: list[str]
    confidence_progression: list[str | None]
    latest_observation: str | None = None
    heuristic_summary: str  # simple concatenation summary (not AI-generated)
    raw_context: str  # full text for external AI consumption

class AutocompleteResult(BaseModel):
    matches: list[str]  # matching root gap / competency strings
    source: str  # "ldg" | "past_cases"
