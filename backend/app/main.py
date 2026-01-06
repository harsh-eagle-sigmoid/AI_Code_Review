from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.langchain.chains import review_chain

app = FastAPI()

# ✅ CORS (already correct, keep it)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ai-code-review-z5wd.vercel.app",
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Health check (Railway needs this)
@app.get("/")
def health():
    return {"status": "ok"}

# ✅ Request schema
class ReviewRequest(BaseModel):
    code: str

# ✅ Review endpoint (SAFE)
@app.post("/review")
def review_code(req: ReviewRequest):
    try:
        result = review_chain.invoke({"code": req.code})

        # LangChain returns dict with "text"
        return {
            "review": result["text"]
        }

    except Exception as e:
        # 🔥 CRITICAL: never let FastAPI crash
        print("REVIEW ERROR:", str(e))
        raise HTTPException(
            status_code=500,
            detail="AI review failed. Please try again."
        )
