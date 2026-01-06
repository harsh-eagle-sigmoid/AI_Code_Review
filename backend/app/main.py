from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.langchain.chains import review_chain

# -------------------------
# App initialization
# -------------------------
app = FastAPI(title="AI Code Review API")

# -------------------------
# CORS CONFIG (VERY IMPORTANT)
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ai-code-review-z5wd.vercel.app",   # Vercel frontend
        "http://localhost:5173",                    # Vite local
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Request schema
# -------------------------
class ReviewRequest(BaseModel):
    code: str

# -------------------------
# Routes
# -------------------------
@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/review")
async def review_code(req: ReviewRequest):
    if not req.code.strip():
        raise HTTPException(status_code=400, detail="Code is empty")

    try:
        result = review_chain.invoke({"code": req.code})

        # LangChain returns {"text": "..."}
        return {
            "review": result["text"]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
