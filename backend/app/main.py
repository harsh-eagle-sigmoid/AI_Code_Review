from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from app.langchain.chains import review_chain

app = FastAPI()

# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # OK for demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Request ----------
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
    source_code = req.code or req.diff

    if not source_code:
        return {
            "summary": "No code provided",
            "bugs": []
        }

    try:
        result = review_chain.invoke({"code": source_code})

        # 🔒 HARD NORMALIZATION
        return {
            "summary": result.get("summary", "Review completed"),
            "bugs": result.get("bugs", []) if isinstance(result.get("bugs"), list) else []
        }

    except Exception as e:
        print("REVIEW ERROR:", e)
        return {
            "summary": "AI review failed",
            "bugs": []
        }
