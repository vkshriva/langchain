from openai import OpenAI
from dotenv import load_dotenv
from os import getenv

load_dotenv()

client = OpenAI(
    api_key=getenv("OPENAI_API_KEY")
)

response = client.responses.create(
    model= "gpt-5.1",
    input="I am Sarun. What about you"
)
print(response.output_text)