from fastapi import HTTPException
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from app.models.review_schema import ReviewResult
from app.core.config import settings

parser = PydanticOutputParser(pydantic_object=ReviewResult)

PROMPT = """
You are a SENIOR Python engineer and strict code reviewer.

MANDATORY:
- Detect ALL logical, runtime, and type errors
- Do NOT return empty bugs if code has issues
- Explain each bug clearly
- Assign severity: LOW, MEDIUM, HIGH, CRITICAL

Return STRICT JSON only.

Code:
{code}

{format_instructions}
"""

llm = ChatGroq(
    api_key=settings.GROQ_API_KEY,
    model=settings.GROQ_MODEL,
    temperature=0
)

prompt = PromptTemplate(
    template=PROMPT,
    input_variables=["code"],
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    }
)

def run_ai_review(code: str) -> ReviewResult:
    try:
        chain = prompt | llm
        response = chain.invoke({"code": code})
        result = parser.parse(response.content)

        if len(code.strip()) > 30 and len(result.bugs) == 0:
            raise ValueError("Invalid AI output: no bugs found")

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
