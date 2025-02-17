import os
import json
import streamlit as st
import requests
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "Question: {question}")
])

st.title("Groq AI chatbot with Tools")
input_text = st.text_input("Ask Something")

llm = ChatGroq(model="llama-3.3-70b-versatile",api_key = os.environ["GROQ_API_KEY"])

output_parser = StrOutputParser()
chain = prompt|llm|output_parser

if input_text:
    response = chain.invoke({'question': input_text})
    st.write(response)