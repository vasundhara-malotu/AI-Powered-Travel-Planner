import os
import streamlit as st
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

# Set up Google API key (replace with your actual API key)
os.environ["GOOGLE_API_KEY"] = "AIzaSyAJjCOTwnpunrZtQ67IPVFku1eTzUz9jCE"  # Replace with your actual key

# Set up ChatPromptTemplate
chat_template = ChatPromptTemplate(
    messages=[
        ("system", "You are a helpful AI Assistant who provides approximated travel costs from the source to destination."),
        ("human", "Plan a trip from {source} to {destination}. Include options for flights, trains, buses, and cabs with their estimated costs.")
    ],
    private_variables={"destination": "Delhi"}  # Default destination, can be overwritten by user input
)

# Set up the Google Gemini Chat Model
chat_model = ChatGoogleGenerativeAI(google_api_key=os.getenv("GOOGLE_API_KEY"), model="gemini-2.0-flash-exp")

# Set up output parser
parser = StrOutputParser()

# Combine the components (chat template -> chat model -> parser)
chain = chat_template | chat_model | parser

# Streamlit UI
st.title("🌍 AI-Powered Travel Planner")

# User inputs
source = st.text_input("Enter Source Location:")
destination = st.text_input("Enter Destination:")

# Trigger to fetch travel options
if st.button("Find Travel Options"):
    if source and destination:
        try:
            # Prepare the input for the chain (source and destination)
            raw_input = {"source": source, "destination": destination}

            # Get the response using LangChain's chain invoke
            travel_options = chain.invoke(raw_input)

            # Display the response in Streamlit UI
            st.subheader("🗺️ Travel Options")
            st.write(travel_options)
        except Exception as e:
            st.error(f"Error occurred: {e}")
    else:
        st.error("Please enter both source and destination.")
