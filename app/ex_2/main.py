from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
import json
import os
import sys

CHAT_HISTORY = 'ex_2/chat_history.json'


def get_project_root():
    return os.path.dirname(os.path.abspath(__file__))


def load_chat_history(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file), False
    return [{"role": "system", "content": "You are a helpful python tutor. "
             "You must answer only Python related questions."}], True


def save_chat_history(file_path, messages):
    with open(file_path, 'w') as file_obj:
        json.dump(messages, file_obj, indent=4)


def get_llm():
    env_path = os.path.join(get_project_root(), '.env')
    load_dotenv(dotenv_path=env_path)
    return ChatOpenAI(model="gpt-5.1", temperature=0.3)


def to_langchain_messages(messages):
    converted = []
    for message in messages:
        role = message.get("role")
        content = message.get("content", "")

        if role == "system":
            converted.append(SystemMessage(content=content))
        elif role == "user":
            converted.append(HumanMessage(content=content))
        elif role == "assistant":
            converted.append(AIMessage(content=content))

    return converted


def chat_with_ai(messages):
    llm = get_llm()
    response = llm.invoke(to_langchain_messages(messages))
    return response.content


try:
    messages, is_new = load_chat_history(CHAT_HISTORY)
    if is_new:
        print("Welcome to pyMentor! Your Python tutor")
        print("Ask me anything about Python programming. Type 'exit' to end the chat.")
    else:
        print("Welcome back to pyMentor! Your previous chat history has been loaded.")

    while True:
        try:
            user_question = input("You: ")
        except EOFError:
            print("\nNo input received. Exiting.")
            sys.exit(0)

        if user_question.lower() == 'exit':
            save_chat_history(CHAT_HISTORY, messages)
            print("Chat history saved. Goodbye!")
            break

        messages.append({"role": "user", "content": user_question})
        response = chat_with_ai(messages)
        messages.append({"role": "assistant", "content": response})
        print("AI:", response)
except Exception as e:
    print("An error occurred:", e)