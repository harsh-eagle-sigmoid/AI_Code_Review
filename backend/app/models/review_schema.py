from pydantic import BaseModel
from typing import List, Literal

Severity = Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]

class Bug(BaseModel):
    issue: str
    severity: Severity

class SecurityIssue(BaseModel):
    issue: str
    severity: Severity

class Optimization(BaseModel):
    suggestion: str

class ReviewResult(BaseModel):
    bugs: List[Bug]
    security: List[SecurityIssue]
    optimizations: List[Optimization]
    score: int
