import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

prompt = PromptTemplate.from_template(
"""welcome to the {city} travel guide
   If you 're visiting in {month} Here is what  you can do:
    1: Must visit places
    2: Local food to try
    3: Useful phrases in {language}
    4: Tips for Travelling on a {budget} budget
"""
)
st.title("Travel Guide")
city = st.text_input("Enter the city you are visiting:")
month = st.text_input("Enter the month you are visiting:")
language = st.text_input("Enter the local language:")
budget = st.text_selectbox("Select your budget:", ["Low", "Medium", "High"])

if city and month and language and budget:
    user_input = prompt.format(city=city, month=month, language=language, budget=budget)
    response = llm.invoke(user_input)
    st.subheader("Travel Guide")
    st.write(response.content)
    