<<<<<<< HEAD
from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate

# from langchain.chat_models import ChatOpenAI  -- old method --
#from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI

from langserve import add_routes
import uvicorn
import os
from langchain_ollama import OllamaLLM
from dotenv import load_dotenv
=======
import os
import uvicorn
from fastapi import FastAPI
from langserve import add_routes
from langchain_groq import ChatGroq
from langchain_ollama import OllamaLLM
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate

>>>>>>> b6d9743 (Reconnect local directory and commit changes)

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
<<<<<<< HEAD
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
=======
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
>>>>>>> b6d9743 (Reconnect local directory and commit changes)

app = FastAPI(
    title="Langchain Server",
    version="1.0",
    description="A Simple API Server"
)

add_routes(
    app,
<<<<<<< HEAD
    ChatOpenAI(),
    path="/openai"
)
model = ChatOpenAI()
=======
    ChatGroq(),
    path="/groq"
)
model = ChatGroq(model="llama-3.3-70b-versatile")
>>>>>>> b6d9743 (Reconnect local directory and commit changes)

# ollama Model (llama)
llm = OllamaLLM(model='llama3.2:1b')

prompt1 = ChatPromptTemplate.from_template("Write me an essay about {topic} with 100 words")
prompt2 = ChatPromptTemplate.from_template("Write me a poem about {topic} with 50 words")

add_routes(
    app,
    prompt1|model,
    path="/essay"
)
add_routes(
    app,
    prompt2|llm,
    path="/poem"
)

if __name__=="__main__":
    uvicorn.run(app,host="localhost", port=8000)