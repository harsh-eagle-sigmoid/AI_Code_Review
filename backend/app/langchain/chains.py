import os
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

for k in ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"]:
    os.environ.pop(k, None)

llm = ChatGroq(
    model="llama3-8b-8192",
    api_key=os.environ["GROQ_API_KEY"],
    temperature=0,
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
