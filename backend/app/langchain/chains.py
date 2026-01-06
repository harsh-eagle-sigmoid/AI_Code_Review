import os
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(
    api_key=os.environ["GROQ_API_KEY"],
    model="llama-3.1-8b-instant",
    temperature=0,
)

prompt = PromptTemplate(
    input_variables=["code"],
    template="""
You are a senior software engineer.
Review the following code and return:
1. Critical bugs
2. Warnings
3. Clean suggestions

Code:
{code}
"""
)

review_chain = prompt | llm
