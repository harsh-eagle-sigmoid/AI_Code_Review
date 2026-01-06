from fastapi import APIRouter, HTTPException
from app.services.ai_reviewer import run_ai_review

router = APIRouter()

SEVERITY_PENALTY = {
    "CRITICAL": 30,
    "HIGH": 20,
    "MEDIUM": 10,
    "LOW": 5,
}

@router.post("")
def review_code(payload: dict):
    code = payload.get("diff")
    if not code:
        raise HTTPException(status_code=400, detail="Missing code diff")

    result = run_ai_review(code)

    score = 100
    for issue in result.bugs + result.security:
        score -= SEVERITY_PENALTY.get(issue.severity, 0)

    score = max(score, 0)

    failed = any(
        issue.severity in ["HIGH", "CRITICAL"]
        for issue in (result.bugs + result.security)
    )

    return {
        "failed": failed,
        "review": {
            **result.model_dump(),
            "score": score
        }
    }
