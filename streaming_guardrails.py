from __future__ import annotations
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent,Runner
from config import config
from dataclasses import dataclass
from pydantic import Field
import asyncio
agent =Agent(
    name="simple agent",
    instructions="you are simple agent you only give long responses",
)

@dataclass
class gardrail_output:
    reasoning:str
    readable_by_ten_year:bool 

guardrail_agent=Agent(
    name="guardrail agent",
    instructions="you are given a response you have to check weather it is readable by 10 year old kid or not",
    output_type=gardrail_output
)

async def gardrail_checker_runner(text:str)->gardrail_output:
    result = await Runner.run(guardrail_agent,text,run_config=config)
    return result.final_output_as(gardrail_output)

async def main():
    question = "what is blackhole and how it behaves"
    result = Runner.run_streamed(agent, question, run_config=config)
    current_text = ""
    next_check_len=300
    guardrail_task = None

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data,ResponseTextDeltaEvent):
            print(event.data.delta,end="",flush=True)
            current_text += event.data.delta
        
        if len(current_text) >= next_check_len and not guardrail_task:
            guardrail_task = asyncio.create_task(gardrail_checker_runner(current_text))
            next_check_len += 300
            print("guardrail started")

        if guardrail_task and guardrail_task.done():
            guardrail_result = guardrail_task.result()
            if not guardrail_result.readable_by_ten_year:
                print(f"guardrail task tripwire triggered{guardrail_result.reasoning}")
                break
        

    guardrail_result = await gardrail_checker_runner(current_text)
    if not guardrail_result.readable_by_ten_year:
        print(f"guardrail task tripwire triggered{guardrail_result.reasoning}")
        print("============="*40)
        print("guardrail task tripwire triggered")


if __name__=="__main__":
    asyncio.run(main())