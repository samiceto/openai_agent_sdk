from __future__ import annotations
import asyncio
from config import config
from agents import (
    Agent,
    Runner,
    FunctionToolResult,
    ModelSettings,
    ToolsToFinalOutputFunction,
    ToolsToFinalOutputResult,
    function_tool,
    RunContextWrapper
)
from pydantic import BaseModel
from typing import Any,Literal


class weather(BaseModel):
    city: str
    temperature_range: str
    conditions: str
    
@function_tool
def get_weather(city:str)->weather:
    return weather(city=city,temperature_range="14-20C",conditions="Sunny with wind")

async def custom_tool(
        context:RunContextWrapper[Any], results:list[FunctionToolResult]
)->ToolsToFinalOutputResult:
    weather:weather = results[0].output
    return ToolsToFinalOutputResult(
        is_final_output=True,final_output= f"{weather.city} is {weather.conditions}"
    )

async def main(tool_use_behavior:Literal["default","first_tool","custom"]="default"):
    if tool_use_behavior == "default":
        behavior:Literal["stop_on_first_tool","run_llm_again"] | ToolsToFinalOutputFunction = "run_llm_again"
    elif tool_use_behavior == "first_tool":
        behavior = "stop_on_first_tool"
    elif tool_use_behavior == "custom":
        behavior = custom_tool

    agent = Agent(
        name="weather agent",
        instructions="you are the agent to inform the weather of given city using the the tool given",
        tools=[get_weather],
        tool_use_behavior=behavior,
        model_settings = ModelSettings(
            tool_choice="required" if tool_use_behavior !="default" else None)
    )

    result = await Runner.run(agent, input="What's the weather in Tokyo?", run_config=config)
    print(result.final_output)


if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--tool-use-behavior",
        type=str,
        required=True,
        help="The behavior to use for tool use. Default will cause tool outputs to be sent to the model. "
        "first_tool_result will cause the first tool result to be used as the final output. "
        "custom will use a custom tool use behavior function.",
        choices=["default", "first_tool", "custom"]

    )
    args = parser.parse_args()
    asyncio.run(main(args.tool_use_behavior3))