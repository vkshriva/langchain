from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()
llm= ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.9)

prompt = PromptTemplate.from_template(
"""Act as a Software consultant.
Compare the {language_1} and {language_2} programming languages
fora {project_type} project.""")

chain = prompt | llm | StrOutputParser()

response = chain.invoke({"language_1": "Python", "language_2": "JavaScript", "project_type": "web development"})

print(response)