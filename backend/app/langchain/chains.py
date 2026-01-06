import os
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

llm = ChatGroq(
    groq_api_key=os.environ["GROQ_API_KEY"],
    model_name="llama3-70b-8192"
)

prompt = PromptTemplate(
    input_variables=["code"],
    template="""
You are an expert code reviewer.
Analyze the following code and list bugs, issues, and improvements.

Code:
{code}
"""
)

review_chain = LLMChain(
    llm=llm,
    prompt=prompt
)
