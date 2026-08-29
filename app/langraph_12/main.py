
from langgraph.graph import StateGraph
from typing import TypedDict


class State(TypedDict):
    msg:str

def greet(state):
    return {"msg": "Hello"}

def add_name(state):
    return {"msg": state["msg"] + " " + "Varun"}


def check_length(state):
    if  len(state["msg"]) > 30:
        return "AageBadho"
    else:
        return "RukJaoo"




builder = StateGraph(State)

builder.add_node("greet", greet)
builder.add_node("add_name", add_name)

builder.set_entry_point("greet")
builder.add_edge("greet", "add_name")
builder.add_conditional_edges("add_name", check_length, {
    "AageBadho": "add_name",
    "RukJaoo": "__end__"
})



graph = builder.compile()

result = graph.invoke({})

print(result)  # Output: {'msg': 'Hello Varun'}