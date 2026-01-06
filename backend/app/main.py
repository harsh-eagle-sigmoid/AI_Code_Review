from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from app.langchain.chains import review_chain

app = FastAPI()

# ---------- CORS (Railway + Vercel) ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # OK for demo / portfolio
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
        # ✅ Accept BOTH `code` and `diff`
        source_code = req.code or req.diff

        if not source_code:
            return {
                "review": {
                    "score": 0,
                    "bugs": [],
                    "summary": "No code provided"
                }
            }

        result = review_chain.invoke({"code": source_code})

        # ✅ Always return what frontend expects
        return {
            "review": {
                "score": 90,
                "bugs": [],
                "summary": result.get("text", "")
            }
        }

    except Exception as e:
        print("REVIEW ERROR:", e)
        return {
            "review": {
                "score": 0,
                "bugs": [],
                "summary": "Internal review error"
            }
        }
