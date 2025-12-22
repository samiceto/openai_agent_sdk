# Agent level

from __future__ import annotations
import asyncio

from openai.resources.chat.chat import AsyncChat
from config import config
from agents import Agent,Runner,OpenAIChatCompletionsModel,set_tracing_disabled
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
load_dotenv()



client = AsyncOpenAI(
    base_url = os.environ.get("GEMINI_BASE_URL"),
    api_key = os.environ.get("key_gemini")
)


agent = Agent(
    name = "simple_agent",
    model =OpenAIChatCompletionsModel(model=os.environ.get("GEMINI_MODEL"),openai_client=client)
)

async def main():
    result =await Runner.run(agent,"what llm are you")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())

