import os
from crewai import Agent
from tools import yt_tool
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"] = "gpt-4o"

# llm = LLM(
#     model="openai/gpt-4o",
#     temperature=0.8,
#     max_tokens=150,
#     top_p=0.9,
#     frequency_penalty=0.1,
#     presence_penalty=0.1,
#     stop=["END"],
#     seed=42
# )

# Content Researcher
blog_researcher = Agent(
    role="Blog Researcher from Youtube Videos",
    goal="Get the relevant video content for the {topic} from YT Channels",
    verbose=True,
    backstory=(
        "Expert in understanding videos in AI, Data Science, Machine Learning and GenAI and providing suggestions"
    ),
    tools=[yt_tool],
    allow_delegation=True
)

# Blog Writer Agent
blog_writer = Agent(
    role="Blog Writer",
    goal="Narrate compelling tech stories about the {topic} from YT Channels",
    verbose=True,
    backstory=(
        "With a flair for simplifying complex topics, you craft "
        "engaging narratives that captivate and educate, bringing new "
        "discoveries to light in an accessible manner"
    ),
    tools=[yt_tool],
    allow_delegation=False
)