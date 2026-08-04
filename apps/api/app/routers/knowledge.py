# OpenSchoolOS API — Knowledge routes (Sprint 002).
# Serves curated educational knowledge from the LDG subject graphs.
# Read-only reference data. No persistence through this router.
import json
from pathlib import Path

from fastapi import APIRouter, HTTPException, Query, status

router = APIRouter(prefix="/knowledge", tags=["knowledge"])

# Path: apps/api/app/routers/knowledge.py → 5 levels up = repo root
KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent / "knowledge"

# Cache subjects in memory (they change rarely, only with code deploys)
_cache: dict[str, dict] = {}


def _load_subject(subject: str) -> dict:
    if subject not in _cache:
        path = KNOWLEDGE_DIR / f"{subject}.json"
        if not path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Subject '{subject}' not found.",
            )
        _cache[subject] = json.loads(path.read_text())
    return _cache[subject]


def _list_subject_files() -> list[str]:
    return sorted(
        p.stem for p in KNOWLEDGE_DIR.glob("*.json")
    )


@router.get("/subjects")
def list_subjects() -> list[dict]:
    """List all available LDG subjects with basic metadata."""
    result = []
    for name in _list_subject_files():
        try:
            data = _load_subject(name)
            result.append({
                "id": name,
                "subject": data["subject"],
                "description": data.get("description", ""),
                "competencyCount": len(data.get("competencies", [])),
            })
        except HTTPException:
            continue
    return result


@router.get("/subjects/{subject}")
def get_subject(subject: str) -> dict:
    """Full LDG for one subject: competencies, dependency graph, and misconceptions."""
    return _load_subject(subject)


@router.get("/subjects/{subject}/competencies")
def list_competencies(subject: str) -> list[dict]:
    """Flat list of all competencies for a subject."""
    data = _load_subject(subject)
    return data.get("competencies", [])


@router.get("/subjects/{subject}/competencies/{competency_id}")
def get_competency(subject: str, competency_id: str) -> dict:
    """Single competency with prerequisites and misconception patterns."""
    data = _load_subject(subject)
    for comp in data.get("competencies", []):
        if comp["id"] == competency_id:
            return comp
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Competency '{competency_id}' not found in subject '{subject}'.",
    )


@router.get("/subjects/{subject}/search")
def search_competencies(
    subject: str,
    q: str = Query(min_length=1, description="Search across label, description, and misconception text"),
) -> list[dict]:
    """Search competencies and misconceptions within a subject."""
    data = _load_subject(subject)
    query = q.lower()
    results: list[dict] = []

    for comp in data.get("competencies", []):
        # Search in label and description
        label_match = query in comp["label"].lower()
        desc_match = query in comp.get("description", "").lower()
        m_match = any(
            query in m.get("observed", "").lower()
            or query in m.get("rootGap", "").lower()
            or query in m.get("evidence", "").lower()
            or query in m.get("strategy", "").lower()
            for m in comp.get("misconceptions", [])
        )

        if label_match or desc_match or m_match:
            matched_misconceptions = [
                m for m in comp.get("misconceptions", [])
                if query in m.get("observed", "").lower()
                or query in m.get("rootGap", "").lower()
                or query in m.get("evidence", "").lower()
                or query in m.get("strategy", "").lower()
            ] if m_match else []
            results.append({
                "competencyId": comp["id"],
                "competencyLabel": comp["label"],
                "description": comp.get("description", ""),
                "gradeLevel": comp.get("gradeLevel", ""),
                "prerequisites": comp.get("prerequisites", []),
                "matchedMisconceptions": matched_misconceptions,
            })

    return results


@router.get("/search")
def search_all_subjects(
    q: str = Query(min_length=1, description="Search across all subjects"),
) -> list[dict]:
    """Search competencies and misconceptions across all subjects."""
    query = q.lower()
    results: list[dict] = []

    for name in _list_subject_files():
        try:
            data = _load_subject(name)
        except HTTPException:
            continue
        for comp in data.get("competencies", []):
            label_match = query in comp["label"].lower()
            desc_match = query in comp.get("description", "").lower()
            m_match = any(
                query in m.get("observed", "").lower()
                or query in m.get("rootGap", "").lower()
                for m in comp.get("misconceptions", [])
            )
            if label_match or desc_match or m_match:
                results.append({
                    "subjectId": name,
                    "subject": data["subject"],
                    "competencyId": comp["id"],
                    "competencyLabel": comp["label"],
                    "description": comp.get("description", ""),
                    "gradeLevel": comp.get("gradeLevel", ""),
                    "prerequisites": comp.get("prerequisites", []),
                })
    return results
