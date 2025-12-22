from __future__ import annotations
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from config import config
from agents import Agent, RunContextWrapper,Runner,handoff
from pydantic import BaseModel

from dotenv import load_dotenv
load_dotenv()


math_agent= Agent(
    name="math_agent",
    instructions = "you are math agent only respond to the math query",
)

class user_info(BaseModel):
    user_tair:str
    log_in:bool

context = user_info(user_tair="expire",log_in=False)

def premuim_user(ctx:RunContextWrapper,agent:Agent)->str:
    print("in_func",ctx.context.user_tair)
    return ctx.context.user_tair in ["premium","new"]

def on_handded(ctx:RunContextWrapper):
    print("checking "+ str(premuim_user(ctx,agent)))
handed_off = handoff(
    agent=math_agent,
    is_enabled=premuim_user,
    # on_handoff=on_handded
)

agent = Agent(
    name = "simple_agent",
    handoffs=[handed_off]
)

async def main():
    result =await Runner.run(agent,"what is the sum of 3.7 and 8.9",run_config=config,context=context)
    print(result.final_output)
    print(result.last_agent.name)


if __name__ == "__main__":
    asyncio.run(main())