import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains import ConversationChain


load_dotenv()

os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Initialize memory in session state
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory()

def print_history(conv:str ):
    if isinstance(conv, str):
        conv = conv.strip().split("\n")

    for message in conv:
        message = message.strip()
        if message.startswith("Human:"):
            with st.chat_message("user"):
                st.write(message.replace("Human: ", "", 1))

        if message.startswith("AI:"):
            with st.chat_message("assistant"):
                st.write(message.replace("AI: ", "", 1))


st.title("Chat with LLAMA 3.3")
st.sidebar.title("Chat History")
input_text = st.chat_input("Ask something...")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "Question: {question}")
])
llm = ChatGroq(model="llama-3.3-70b-versatile")
output_parser = StrOutputParser()

memory = ConversationBufferMemory()

conversation = ConversationChain(llm = llm,
                                verbose=True,
                                memory=st.session_state.memory)

if input_text:
    conversation.run(input_text)
    history = conversation.memory.buffer
    print_history(history)