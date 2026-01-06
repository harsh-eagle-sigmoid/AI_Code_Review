from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.langchain.chains import review_chain
from app.langchain.output_parser import safe_json_parse

app = FastAPI(title="AI Code Review API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeInput(BaseModel):
    code: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/review")
def review_code(payload: CodeInput):
    if not payload.code or not payload.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")

    try:
        response = review_chain.invoke({"code": payload.code})
        result_text = response.content
        return safe_json_parse(result_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
