import os
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

llm = ChatGroq(
    api_key=os.environ["GROQ_API_KEY"],
    model="llama3-8b-8192",
    temperature=0,
)

prompt = ChatPromptTemplate.from_template(
    """
You are a senior code reviewer.

Review the following code and return JSON with:
- issues: list of issues with line, severity, description
- summary: short summary

Code:
{code}
"""
)

review_chain = prompt | llm
