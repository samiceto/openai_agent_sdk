from config import config
from agents import Agent,Runner,function_tool,RunContextWrapper
from dataclasses import dataclass

@dataclass
class True_False:
    Tr:bool
    Fal:bool

tr = True_False(Tr=True,Fal=False)
def is_enableld_weather_tool(ctx:RunContextWrapper[True_False],agent:Agent)->bool:
    return ctx.context.Fal
@function_tool(is_enabled=is_enableld_weather_tool)
def weather(location:str)->str:
    return f"the weathr in {location} is sunny"




agent= Agent(
    name="simple_agent",
    instructions="you are simple agent",
    tools = [weather]
)

result = Runner.run_sync(
    agent,
    "what is the weather in karachi city ",
    run_config=config,
    context=tr
)
print(result.final_output)