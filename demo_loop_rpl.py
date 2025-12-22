import asyncio
from agents import Agent, run_demo_loop,OpenAIChatCompletionsModel
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

key_gemini = os.getenv("key_gemini")
model=os.getenve("GEMINI_MODEL")
base_url_gemini = "https://generativelanguage.googleapis.com/v1beta/openai/"

client = AsyncOpenAI(
    api_key=key_gemini,
    base_url=base_url_gemini
)

model1 = OpenAIChatCompletionsModel(
    model=model,
    openai_client=client
)

async def main() -> None:
    agent = Agent(name="Assistant", instructions="You are a helpful assistant.",model =model1)
    
    await run_demo_loop(agent)

if __name__ == "__main__":
    asyncio.run(main())