
from langgraph.graph import StateGraph,START,END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from typing import TypedDict
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file




class State(TypedDict):
    topic :str
    poem:str
    feedback:str
    count:int

llm = ChatOpenAI(model_name="gpt-3.5-turbo")

def write_node(state: State):
    print(f"--Writing attempt {state['count']+1}--\n")

    prompt =f"Write a short poem on the topic: {state['topic']}.It must be exactly  2 lines long."

    if(state["feedback"]):
        prompt+=f"Last time you failse : Feedback: {state['feedback']}. Please improve the poem based on this feedback."

    poem = llm.invoke([HumanMessage(content=prompt)])

    return {"poem": poem.content, "count": state.get("count", 0) + 1}


def auditor_node(state: State):
    print(f"--Auditing attempt {state['count']}--\n")
    lines = state["poem"].split("\n")
    if len(lines) == 2:
        return {"feedback": "Good job!"}
    else:
        return {"feedback": "The poem must be exactly 2 lines long."}


def should_continue(state: State):
    if state["feedback"] == "Good job!" or state.get("count", 0) >= 3:   
        return "end"
    else:
        return "retry"



builder = StateGraph(State)

builder.add_node("write_poem", write_node)
builder.add_node("audit_poem", auditor_node)

builder.add_edge(START, "write_poem")
builder.add_edge("write_poem", "audit_poem")

builder.add_conditional_edges("audit_poem", should_continue, {
    "retry": "write_poem",
    "end": END
})

graph = builder.compile()

topic = input("Enter a topic for Poem: ")

result = graph.invoke({"topic": topic, "count": 0, "poem": "", "feedback": ""})


print(f"Final result: {result['poem']}")  