from agents import Agent,Runner,function_tool,enable_verbose_stdout_logging
from config import config
import asyncio


# enable_verbose_stdout_logging()
@function_tool(
        name_override="weather_wala_tool",
        description_override="mosam to bata dy",
        # use_docstring_info=False
)
def weather_tool(location:str)->str:
    """
    fetch weather according to the given location
    
    
    args:
    location:location for getting weather
    """
    return f"sunny"


@function_tool
def sum(a:int,b:int)->int:
    """
    fetch the tow numbers and sum up
    args:
    a: the first number
    b: the second number
    """
    return a+b

async def main():
    weather_agent=Agent(
        name="weather agent",
        instructions="you are weather assistant agent",
        tools = [weather_tool,sum],
        tool_use_behavior="stop_on_first_tool",
    
    )

    result =await Runner.run(
        weather_agent,
        "what is the weather in karachi and give the sum of 2 and 5",
        run_config=config
    )
    print("tools",weather_agent.tools[0])
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())