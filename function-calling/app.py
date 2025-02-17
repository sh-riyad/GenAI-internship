import os
import requests
from dotenv import load_dotenv
import streamlit as st

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.tools import tool

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")



@tool
def get_temperature(city: str) -> str:
    """
    Retrieves the current temperature for a given city using OpenWeatherMap API.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")  # Make sure to set this in .env
    base_url = "http://api.openweathermap.org/data/2.5/weather"

    params = {"q": city, "appid": api_key, "units": "metric"}
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        return f"The current temperature in {city} is {temp}°C."
    else:
        return "Could not fetch the temperature. Please check the city name."


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are you helpful assistance."),
        ("user", "Question {question}")

    ]
)

st.title("Groq AI Chatbot With Custom Functions")
input_text = st.text_input("Ask Something")

model = ChatGroq(model="llama-3.3-70b-versatile", api_key= os.environ["GROQ_API_KEY"])

output_parser = StrOutputParser()
chain = prompt|model|output_parser

if input_text:
    response = chain.invoke({"question":input_text})
    st.write(response)