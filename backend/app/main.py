import os

# 🚨 MUST BE FIRST — before ANY other imports
for key in [
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "ALL_PROXY",
    "http_proxy",
    "https_proxy",
]:
    os.environ.pop(key, None)

from fastapi import FastAPI
from app.langchain.chains import review_chain

app = FastAPI()

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/review")
async def review_code(payload: dict):
    code = payload.get("code", "")
    result = review_chain.invoke({"code": code})
    return result
