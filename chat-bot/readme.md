# GenAI-internship - Chat-Bot Directory

Welcome to the **chat-bot** directory of the **GenAI-internship** repository. This directory contains several Python files used for integrating Langchain with Streamlit, along with necessary configurations to run the chat-bot.

## Prerequisites

Make sure you have **Python 3.x** installed. You can install the required dependencies using the following command:

```bash
cd chat-bot
pip install -r requirements.txt
```

## Files

### 1. Python Files

#### `llama3 2B using ollama`
This script integrates **Langchain** with **Ollama**.  
Before running this file, you need to:

1. Download and install **Ollama** from [Ollama's official website](https://ollama.com).
2. Download the **Llama 3.2 1B** model by running the following command:

   ```bash
   ollama run llama3.2:1b
   ```

3. After downloading the model, run the script using:

   ```bash
   streamlit run llama3_ollama.py
   ```

#### `llama-3.3 using Groq`
Run it using:

```bash
streamlit run llama-3.3_groq.py
```

#### `OpenAI`
Run it using:

```bash
streamlit run openai.py
```

### 2. Configuration Files

- `.env`  
  This file contains your API keys. Ensure it is set up correctly. The following environment variables should be defined in your `.env` file:

  ```plaintext
  LANGCHAIN_API_KEY="***"
  OPENAI_API_KEY="***"
  LANGCHAIN_PROJECT="chatbot"
  GROQ_API_KEY="***"
  ```

## How to Run

1. Make sure your **.env** file is configured with the correct API keys.
2. Install the required packages with `pip install -r requirements.txt`.
3. Download **Ollama** and the Llama 3.2 model (if running `llama3_ollama.py`).
4. Run any of the Python files using Streamlit with the commands listed above.
