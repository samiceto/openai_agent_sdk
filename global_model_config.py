

#globle config

from __future__ import annotations
import asyncio
from agents import Agent,Runner,set_default_openai_api,set_default_openai_client,set_tracing_disabled
from openai import AsyncOpenAI
import os 
from dotenv import load_dotenv
load_dotenv()

client =AsyncOpenAI(
    base_url = os.environ.get("GEMINI_BASE_URL"),
    api_key= os.environ.get("key_gemini")
   
)

set_default_openai_client(client=client, use_for_tracing=False)
set_default_openai_api("chat_completions")
set_tracing_disabled(disabled=True)

agent = Agent(
    name = "simple_agent",
    model = os.environ.get("GEMINI_MODEL")
)

async def main():
    result =await Runner.run(agent,"what llm are you")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
