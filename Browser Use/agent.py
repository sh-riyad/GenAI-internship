from langchain_openai import ChatOpenAI
from browser_use import Agent, Controller, ActionResult
from dotenv import load_dotenv
import rich
load_dotenv()

import asyncio

# from browser_use.browser.browser import Browser, BrowserConfig

# Initialize the controller
controller = Controller()

@controller.action('Ask user for information')
def ask_human(question: str) -> str:
    answer = input(f'\n{question}\nInput: ')
    return ActionResult(extracted_content=answer)

llm = ChatOpenAI(model="gpt-4o")

async def main():
    agent = Agent(
        task="""find a water battle from daraz and order it in chittagong. for loging perpose use this google account. \
        gmail: 'corionmyth@gmail.com', password: '%ZkyBRvk!eVdcy8R!BFj' \
        my location is chawkbazar, chittagong. And mobile no. 01623979057""",
        llm=llm,
        controller=controller,
    )
    result = await agent.run()
    rich.print(result)

asyncio.run(main())