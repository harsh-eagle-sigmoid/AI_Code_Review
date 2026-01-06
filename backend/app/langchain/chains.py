import os

# 🚨 CRITICAL FIX: remove Railway-injected proxy vars
for key in ["HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy"]:
    os.environ.pop(key, None)

from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

llm = ChatGroq(
    api_key=os.environ["GROQ_API_KEY"],
    model="llama3-8b-8192",
    temperature=0,
)

prompt = ChatPromptTemplate.from_template(
    """
You are a senior software engineer performing static code analysis.

Analyze the following code and return JSON with:
- issues: list of detected issues with line, severity, description
- summary: short overall summary

Code:
{code}
"""
)

review_chain = prompt | llm
