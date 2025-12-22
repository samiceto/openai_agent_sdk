import asyncio
from agents import Agent,Runner
from agents.run import AgentRunner,set_default_agent_runner
import os
from dotenv import load_dotenv

load_dotenv()
from config import config

class custome_runner(AgentRunner):
    async def run(self,starting_agent,input,**kwargs):
        result =await super().run(starting_agent,input,**kwargs)
        result.final_output = result.final_output +"this is the second call"
        # return result
        return await super().run(starting_agent,"who is more powerful men or women",**kwargs)
set_default_agent_runner(custome_runner())

agent=Agent(
    name="simple_agent"
)

async def main():
    result=await Runner.run(agent,"what is the capital of pakistan",run_config=config)
    print(result.final_output)


if __name__=="__main__":
    asyncio.run(main())