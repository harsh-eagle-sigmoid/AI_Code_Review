from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.2,
    groq_api_key=os.environ["GROQ_API_KEY"]
)

prompt = PromptTemplate(
    input_variables=["code"],
    template="""
You are an expert senior software engineer.

Review the following code and provide:
1. Bugs
2. Improvements
3. Security issues
4. Final summary

Code:
{code}
"""
)

review_chain = LLMChain(
    llm=llm,
    prompt=prompt
)
