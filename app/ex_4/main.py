from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import os


def load_environment():
    load_dotenv()


def initialize_llm():
    return ChatOpenAI(model="gpt-4o-mini")


def start_chat(llm):
    print("Welcome to the chat! Type 'exit' to end the conversation.")
    conversation = [SystemMessage(content="You are a helpful assistant who answers clearly and politely.")]
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Ending the conversation. Goodbye!")
            break

        conversation.append(HumanMessage(content=user_input))
        response = llm.invoke(conversation)
        print(f"Assistant: {response.content}")
        conversation.append(AIMessage(content=response.content))


if __name__ == "__main__":
    load_environment()
    llm = initialize_llm()
    start_chat(llm)


