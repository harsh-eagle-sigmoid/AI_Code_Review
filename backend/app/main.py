from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from app.langchain.chains import review_chain

app = FastAPI()

# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # OK for portfolio / demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Request Schema ----------
class ReviewRequest(BaseModel):
    code: Optional[str] = None
    diff: Optional[str] = None

# ---------- Health ----------
@app.get("/")
def root():
    return {"status": "ok"}

# ---------- Review ----------
@app.post("/review")
async def review_code(req: ReviewRequest):
    try:
        # Accept BOTH `code` and `diff`
        source_code = req.code or req.diff

        if not source_code or not source_code.strip():
            return {
                "summary": "No code provided",
                "bugs": []
            }

        # SINGLE invocation (very important)
        result: Dict[str, Any] = review_chain.invoke(
            {"code": source_code}
        )

        # HARD guarantee of response shape
        return {
            "summary": result.get("summary", "Review completed"),
            "bugs": result.get("bugs", [])
            if isinstance(result.get("bugs"), list)
            else []
        }

    except Exception as e:
        print("REVIEW ERROR:", e)
        return {
            "summary": "AI review failed. Please try again.",
            "bugs": []
        }
