import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os

# Get the OpenAI API key from environment variable
openai_api_key = os.environ.get("OPENAI_API_KEY")

# Check if the API key is available
if openai_api_key is None:
    raise ValueError("OpenAI API key is not set in the environment variable OPENAI_API_KEY")

llm = ChatOpenAI(openai_api_key=openai_api_key)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are world class technical documentation writer."),
    ("user", "{input}")
])

chain = prompt | llm 

result = chain.invoke({"input": "how can langsmith help with testing?"})

print(result.content)

