from agents import Agent, HandoffInputData, ModelSettings, RunContextWrapper,Runner,handoff,function_tool
import sys
import os
from agents.extensions import handoff_filters
import asyncio

from agents.model_settings import ToolChoice
from pydantic import BaseModel
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config 

class input_type_class(BaseModel):
    reason:str

@function_tool
async def city_name(question: str) -> str:
    print(question)  # Simulate asking for input
    return input(question) # Simulate user input (replace with actual async input if needed)
@function_tool
async def weather_tool(city:str):
    return f"the weather in {city} is sunny 30cc"

def filter_input(handoff_input_data:HandoffInputData)->HandoffInputData:
    print("**" *10,handoff_input_data.input_history,"**" *10)
    return HandoffInputData(
            input_history=handoff_input_data.input_history,
            pre_handoff_items=tuple(handoff_input_data.pre_handoff_items),
            new_items=tuple(handoff_input_data.new_items),
        )


async def my_handoff(ctx:RunContextWrapper[None],input_data:input_type_class):
    print(input_data.reason)
    
math_agent=Agent(
    name="math_agent",
    instructions = (
                    "If the city name is not provided in the query, "
        "use the city_name tool to ask for it, then use the weather_tool to get the weather "
        "information for that city. Ensure the city_name tool's output is passed to weather_tool. "),
    tools = [weather_tool,city_name],
    model_settings=ModelSettings(tool_choice="required")
)
on_handoff = handoff(
    agent = math_agent,
    on_handoff=my_handoff,
    input_type = input_type_class,
    input_filter=filter_input,
    # is_enabled=False
)
agent = Agent(
    name="simple_agent",
    instructions=(
        "You are a simple assistant."
        "if asked about math related question use handoff always"
    ),
    # tools = [city_name,weather_tool],
    
    # model_settings=ModelSettings(tool_choice="required"),
    handoffs=[on_handoff],
)

async def main():
    result =await Runner.run(
        agent,"what is the weather in unknown city what is the sum of 4.3 and 6.3 "
    )
    print(result.final_output)


if __name__=="__main__":
    asyncio.run(main())
