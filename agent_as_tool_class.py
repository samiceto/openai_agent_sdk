from agents import Agent,Runner
from config import config


spanish_agnt = Agent(
    name= "spanish_agent",
    instructions="you only speak spanish"
)
agent = Agent(
    name="smple agent",
    instructions="you are simple assistan",
    tools = [
        spanish_agnt.as_tool(
            tool_name="spanish_agent",
            tool_description="only speaks spanish"
        )
    ]
    
)

result= Runner.run_sync(
    agent,
    "translate this in spanish, what is the capital of america",
    run_config=config,
    max_turns=2 # by default it's value is 10
)
print(result.final_output)