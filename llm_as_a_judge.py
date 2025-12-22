from __future__ import annotations
import asyncio
from agents import Agent,Runner,trace,ItemHelpers,TResponseInputItem
from dataclasses import dataclass
from config import config
from typing import Literal


story_outline_agent= Agent(
    name="story_outline_agent",
    instructions="you are story outline agent to create short story outline based on inpout",
)
@dataclass
class story_outline_feedback:
    feedback:str
    score:Literal["pass","need_improvement","fail"]


evaluator = Agent(
    name="evaluator",
    instructions="you are evaluator to evaluate story outline based on feedback never give the pass on first call after 5 attempts you can give the pass if the story outline is good enough dot go ro perfection",
    output_type=story_outline_feedback
)

async def main():
    mesg = input("Enter the story outline subject")
    input_items: list[TResponseInputItem]=[{"content":mesg,"role":"user"}]
    letest_outline:str|None=None

    with trace("llm as judge"):
        while True:
            story_outline_result = await Runner.run(story_outline_agent,input_items,run_config=config)

            input_items = story_outline_result.to_input_list()
            letest_outline = ItemHelpers.text_message_outputs(story_outline_result.new_items)
            print("story outline generated")

            feedback_result = await Runner.run (evaluator,input_items,run_config=config)
            result:story_outline_feedback=feedback_result.final_output

            if result.score=="pass":
                print("story is good breaking")
                break

            print("story is not good, running again")
            input_items.append({"role":"assistant","content":result.feedback})
    print(f"\n\n story outline {letest_outline}")

if __name__=="__main__":
    asyncio.run(main())
