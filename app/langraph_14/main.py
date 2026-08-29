


from langgraph.graph import StateGraph,START,END
from langchain_openai import ChatOpenAI
from typing import TypedDict
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file




class State(TypedDict):
    user_input :str
    response :str

llm = ChatOpenAI(model_name="gpt-3.5-turbo")

def generate_greeting(state: State):
    prompt = (f"Generate a short Friendly Roast for this user input: {state['user_input']}")
    return {"response": llm.invoke(prompt).content}



builder = StateGraph(State)

builder.add_node("generate_greeting", generate_greeting)

builder.add_edge(START, "generate_greeting")
builder.add_edge("generate_greeting", END)


graph = builder.compile()

name = input("Enter your name: ")

result = graph.invoke({"user_input": name, "response": ""})


print(f"Final result: {result}")  