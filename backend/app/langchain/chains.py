from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv
load_dotenv()
import json
import os

# ===================== SCHEMA =====================

class Bug(BaseModel):
    line: int = Field(...)
    severity: str = Field(...)
    description: str = Field(...)
    suggestion: str = Field(...)

class ReviewResult(BaseModel):
    summary: str
    bugs: List[Bug]

# ===================== LLM =====================

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant",
    temperature=0
)

# ===================== PROMPT =====================

prompt = PromptTemplate(
    input_variables=["code"],
    template="""
You are a senior software engineer.

Analyze the following Python code and identify:
- Runtime errors
- Type errors
- Logic bugs
- Bad practices

STRICT RULES:
- Output ONLY valid JSON
- Do NOT include markdown
- Do NOT include explanations
- Do NOT include code blocks
- JSON must match EXACTLY this format:

{{
  "summary": "short summary",
  "bugs": [
    {{
      "line": 1,
      "severity": "HIGH",
      "description": "what is wrong",
      "suggestion": "how to fix"
    }}
  ]
}}

If no issues exist, return:

{{
  "summary": "No issues found",
  "bugs": []
}}

Code:
{code}
"""
)

# ===================== CHAIN =====================

def review_chain(code: str) -> dict:
    response = llm.invoke(prompt.format(code=code))

    try:
        return json.loads(response.content)
    except Exception as e:
        print("JSON PARSE ERROR:", e)
        print("RAW MODEL OUTPUT:", response.content)
        return {
            "summary": "Model output parsing failed",
            "bugs": []
        }
