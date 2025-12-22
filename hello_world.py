from dotenv import load_dotenv
from agents import Agent,Runner
from config import config

load_dotenv()

agent = Agent(name="simple_hello_world_agent")

result = Runner.run_sync(agent,"what is the capital of pakistan",runconfig=config)
print(result.final_output)