from agents import Agent,Runner,function_tool,RunContextWrapper
from config import config
from agents.exceptions import UserError
from typing import Any


def tool_error(ctx: RunContextWrapper[Any], error: Exception) -> str:
    """The default tool error function, which just returns a generic error message."""
    return f"An error occurred while running the tool. Please try again. Error: {str(error)}"


@function_tool(
        name_override="get_weather", #this must be camal case means small leter and _ in the place of space
        use_docstring_info=True,
        # failure_error_function=None
        failure_error_function=tool_error,
)
async def fetch_weather(city:str)->str:
    """
    fetch weadther according to given loction
    args:
    city: the location to give weather condition

    """
    # return f"the weather in {city} is sunny"
    raise UserError(f"the error occured")
agent = Agent(
    name="smple agent",
    instructions="you are simple assistan",
    tools=[fetch_weather]
)

result= Runner.run_sync(
    agent,
    "what is the weather in karachi",
    run_config=config
)
print(result.final_output)