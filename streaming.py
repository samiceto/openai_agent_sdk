from config import config
from agents import Agent,Runner,function_tool,ModelSettings
from agents.agent import StopAtTools

import asyncio
from openai.types.responses import ResponseTextDeltaEvent


@function_tool
def weather(location:str)->str:
    """
    fetch weather according to the given location
    
    
    args:
    location:location for getting weather
    """
    return f"the weathr in {location} is sunny"
agent = Agent(
    name="simple agent",
    instructions="you are simple agent",
    tools = [weather],
    tool_use_behavior=StopAtTools(stop_at_tool_names=["weather"]),
    model_settings=ModelSettings(tool_choice="required"),
    #  model_settings=ModelSettings(parallel_tool_calls=False), #if more then one tool availabe then it wont call them at once but call one tool then got to llm then another one tool the maxturns should be enough or more
    reset_tool_choice=False

    
)

async def main():
    result = Runner.run_streamed(agent,"what is the weather in karachi city",run_config=config)
    async for event in result.stream_events():
        # print("EVENT",event ,"\n")
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
             print(event.data.delta, end="", flush=True)
asyncio.run(main())