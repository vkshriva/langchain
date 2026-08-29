
from langgraph.graph import StateGraph
from typing import TypedDict


class State(TypedDict):
    msg:str
    count:int

def greet(state):
    return {"msg": "Hello", "count": 0}

def add_name(state):
    return {"msg": state["msg"] + " Varun", "count": state.get("count", 0) + 1}


def check_loop(state):
    if state.get("count", 0) < 3:
        return "AageBadho"
    else:
        return "RukJaoo"



builder = StateGraph(State)

builder.add_node("greet", greet)
builder.add_node("add_name", add_name)

builder.set_entry_point("greet")
builder.add_edge("greet", "add_name")
builder.add_conditional_edges("add_name", check_loop, {
    "AageBadho": "add_name",
    "RukJaoo": "__end__"
})



graph = builder.compile()

result = graph.invoke({})

print(f"Final result: {result}")  