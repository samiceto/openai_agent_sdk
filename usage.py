from __future__ import annotations
import asyncio

from config import config
from agents import Agent,Runner
from typing import Any

agent = Agent(
    name = "simple_agent"
)

async def main():
    result =await Runner.run(agent,"what is the capital of france",run_config=config)
    print(result.final_output)
    usage = result.context_wrapper.usage
    print("requests",usage.requests)
    print("input tokens",usage.input_tokens)
    print("output tokens ",usage.output_tokens)
    print("input tokens details",usage.input_tokens_details)
    print("output tokens details",usage.output_tokens_details)
    print("total tokens",usage.total_tokens)


if __name__ == "__main__":
    asyncio.run(main())
