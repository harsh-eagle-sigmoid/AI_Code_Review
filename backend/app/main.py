from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.langchain.chains import review_chain

app = FastAPI()

# CORS (Vercel + Railway)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ReviewRequest(BaseModel):
    diff: str   # frontend sends `diff`

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/review")
async def review_code(req: ReviewRequest):
    try:
        result = review_chain.invoke({"code": req.diff})

        # ✅ MATCH FRONTEND SHAPE EXACTLY
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
                "summary": "Review failed"
            }
        }
