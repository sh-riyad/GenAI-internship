from pydantic_settings import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv


class Settings(BaseSettings):
    """
    Configuration settings for the AI Dermatology Assistant.
    Reads values from the environment using Pydantic.
    """

    # Project Settings
    PROJECT_NAME: str = "AI Dermatology Assistant"

    # API Keys
    OPENAI_API_KEY: str

    # LangSmith Settings
    LANGSMITH_TRACING: bool = True
    LANGSMITH_ENDPOINT: str = "https://api.smith.langchain.com"
    LANGSMITH_API_KEY: str
    LANGSMITH_PROJECT: str = "AI Dermatology Assistant"
    TAVILY_API_KEY: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings():
    load_dotenv(override=True)
    return Settings()


settings = get_settings()