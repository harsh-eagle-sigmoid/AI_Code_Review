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
        return {"summary": "No code provided", "bugs": []}

    result = review_chain(source_code)
    return result
