from fastapi import FastAPI
from pydantic import BaseModel
from app.langchain.chains import review_chain

app = FastAPI()

class ReviewRequest(BaseModel):
    code: str

@app.post("/review")
async def review_code(req: ReviewRequest):
    result = review_chain.invoke({"code": req.code})

    # result is an AIMessage, NOT a dict
    return {
        "review": result.content
    }
