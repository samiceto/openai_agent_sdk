from agents import Agent,Runner,set_default_openai_key,WebSearchTool
import os
from dotenv import load_dotenv



load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))
pak = "PAK"
agent= Agent(
    name="websearch",
    instructions="you are simple agent",
    tools= [WebSearchTool()
    ]
)
result = Runner.run_sync(
    agent,
    "open ai agents sdk in handoffs peramitor input_filters  if we want to cutomize it how can we, actually i want to send only the summery not intire conversation history"
)
print(result.final_output)