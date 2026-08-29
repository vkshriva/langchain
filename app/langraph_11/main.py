from langgraph.graph import StateGraph
from typing import TypedDict


class State(TypedDict):
    msg:str

def greet(state):
    return {"msg": "Hello"}

def add_name(state):
    return {"msg": state["msg"] + " " + "Varun"}

def add_surname(state):
    return {"msg": state["msg"] + " " + "Shrivastava"}

def add_welcome(state):
    return {"msg": state["msg"] + " " + "Welcome to LangGraph!"}



builder = StateGraph(State)

builder.add_node("greet", greet)
builder.add_node("add_name", add_name)
builder.add_node("add_surname", add_surname)
builder.add_node("add_welcome", add_welcome)

builder.set_entry_point("greet")

builder.add_edge("greet", "add_name")
builder.add_edge("add_name", "add_surname")
builder.add_edge("add_surname", "add_welcome")
builder.add_edge("add_welcome", "__end__")


graph = builder.compile()

result = graph.invoke({})

print(result)  # Output: {'msg': 'Hello Varun'}