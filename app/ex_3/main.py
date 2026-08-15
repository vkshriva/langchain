from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from os import getenv

load_dotenv()

llm = ChatOpenAI(model="gpt-5.1")

response = llm.invoke("where is Delhi located?")

print(response.content)