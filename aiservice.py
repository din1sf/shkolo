import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os

openai_api_key = os.environ.get("OPENAI_API_KEY")
if openai_api_key is None:
    raise ValueError("OpenAI API key is not set in the environment variable OPENAI_API_KEY")

llm = ChatOpenAI(openai_api_key=openai_api_key)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are top movie critic. You are asked to suggest a movie to a friend. Suggested movie must by Oskar nominated."),
    ("user", "{input}")
])

chain = prompt | llm 
result = chain.invoke({"input": "I am looking for a movie to watch. Can you suggest me something?"})

print(result.content)

