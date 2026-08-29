
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableParallel


load_dotenv()

llm = ChatOpenAI(model_name="gpt-4", temperature=0)

explaination_prompt = ChatPromptTemplate.from_template("Expalin {topic} in simple terms")
question_prompt = ChatPromptTemplate.from_template("Generate 5 interview   question on {topic} ")
examples_prompt = ChatPromptTemplate.from_template("Write a simple code example for {topic}")

explaination_runnable = explaination_prompt | llm | StrOutputParser()
question_runnable = question_prompt | llm | StrOutputParser()
examples_runnable = examples_prompt | llm | StrOutputParser()

chain = RunnableParallel(explanation=explaination_runnable, question=question_runnable, examples=examples_runnable)

result = chain.invoke({"topic": "Python Lambdas"})


print("Expalanation: \n",result["explanation"])
print("Questions: \n",result["question"])
print("Code Examples: \n",result["examples"])
