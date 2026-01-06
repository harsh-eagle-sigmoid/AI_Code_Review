from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.langchain.chains import review_chain

app = FastAPI()

# CORS (Vercel + local)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ReviewRequest(BaseModel):
    code: str

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/review")
async def review_code(req: ReviewRequest):
    try:
        result = review_chain.invoke({"code": req.code})

        # 🔒 SAFE RESPONSE SHAPE (frontend expects this)
        return {
            "summary": result.get("text", ""),
            "issues": [],   # ALWAYS an array
            "score": 90     # SAFE default score
        }

    except Exception as e:
        print("REVIEW ERROR:", e)
        return {
            "summary": "Review failed",
            "issues": [],
            "score": 0
        }
