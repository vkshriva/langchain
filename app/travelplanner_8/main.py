import streamlit as st
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


load_dotenv()

st.set_page_config(page_title="AI Travel Planner", page_icon="🌎")

st.title("🌎 AI Travel Planner")
st.write("Plan your trip step-by-step using AI ✈️")

location = st.text_input("Enter Location")

if st.button("Plan My Trip"):
	if location.strip() == "":
		st.warning("Please enter a location")
	else:
		with st.spinner("Planning your trip..."):
			llm = ChatOpenAI(model="gpt-4o-mini")

			places_prompt = ChatPromptTemplate.from_template(
				"List top tourist places in {location}"
			)
			places_chain = places_prompt | llm | StrOutputParser()

			hotels_prompt = ChatPromptTemplate.from_template(
				"Suggest good hotels in {location}"
			)
			hotels_chain = hotels_prompt | llm | StrOutputParser()

			itinerary_prompt = ChatPromptTemplate.from_template(
				"Create a 3-day itinerary for {location} based on these tourist places:\n{places}"
			)
			itinerary_chain = itinerary_prompt | llm | StrOutputParser()

			budget_prompt = ChatPromptTemplate.from_template(
				"Estimate a budget for a 3-day trip based on this itinerary:\n{itinerary}"
			)
			budget_chain = budget_prompt | llm | StrOutputParser()

			tips_prompt = ChatPromptTemplate.from_template(
				"Give useful travel tips for visiting {location}"
			)
			tips_chain = tips_prompt | llm | StrOutputParser()

			st.subheader("🔍 Tourist Places")
			places = places_chain.invoke({"location": location})
			st.write(places)

			st.subheader("🏨 Hotels")
			hotels = hotels_chain.invoke({"location": location})
			st.write(hotels)

			st.subheader("🗺️ Itinerary")
			itinerary = itinerary_chain.invoke(
				{"location": location, "places": places}
			)
			st.write(itinerary)

			st.subheader("💰 Budget")
			budget = budget_chain.invoke({"itinerary": itinerary})
			st.write(budget)

			st.subheader("💡 Travel Tips")
			tips = tips_chain.invoke({"location": location})
			st.write(tips)

			st.success("✅ Trip planning completed!")
