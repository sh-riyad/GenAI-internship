import requests
import streamlit as st

<<<<<<< HEAD
def get_openai_response(input_text):
=======
def get_groq_response(input_text):
>>>>>>> b6d9743 (Reconnect local directory and commit changes)
    response = requests.post("http://localhost:8000/essay/invoke",
                             json = {'input':{'topic':input_text}})

    return response.json()['output']['content']

def get_ollama_response(input_text):
    response = requests.post("http://localhost:8000/poem/invoke",
                             json = {'input':{'topic':input_text}})

    return response.json()['output']

st.title("Langchain Demo with two llms")
input_text1 = st.text_input("Write and essay on")
input_text2 = st.text_input("Write a poem on")

if input_text1:
<<<<<<< HEAD
    st.write(get_openai_response(input_text1))
=======
    st.write(get_groq_response(input_text1))
>>>>>>> b6d9743 (Reconnect local directory and commit changes)

if input_text2:
    st.write(get_ollama_response(input_text2))