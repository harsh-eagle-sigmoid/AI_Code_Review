import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = ChatGroq(
    groq_api_key=os.environ["GROQ_API_KEY"],
    model_name="llama-3.1-8b-instant",
    temperature=0,
)

prompt = ChatPromptTemplate.from_template(
    """
You are an expert code reviewer.

Return ONLY valid JSON.
Do NOT include markdown, explanations, or extra text.

Example format (follow exactly):

{{
  "issues": [
    {{
      "file": "file.py",
      "line": 1,
      "severity": "HIGH | MEDIUM | LOW",
      "issue_type": "Security | Bug | Performance | Style",
      "description": "explain issue",
      "suggestion": "how to fix"
    }}
  ],
  "summary": "overall review"
}}

Code:
{code}
"""
)

# Modern runnable chain
review_chain = prompt | llm
