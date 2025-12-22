import os 
from dotenv import load_dotenv
from agents import Agent,Runner,SQLiteSession
from agents.run import RunConfig

load_dotenv()
session = SQLiteSession("test.db")

simple_agent = Agent(
    name="simple agent",
    instructions="you are simple assistan"
)


result = Runner.run_sync(
    simple_agent,
    "what is the weather in karachi city ",
    # run_config=config,
    session = session
)
print(result.final_output)