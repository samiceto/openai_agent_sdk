from agents import Agent,Runner,OpenAIChatCompletionsModel,AsyncOpenAI,function_tool,RunContextWrapper
import os
from dotenv import load_dotenv
from agents.run import RunConfig
from pydantic import BaseModel

class weather(BaseModel):
    city:str
    weather:str
    temperature:str

class user_info(BaseModel):
    name:str
    age:int


userObj = user_info(name="Done",age="30")

load_dotenv()

key_gemini = os.getenv("key_gemini")
base_url_gemini = "https://generativelanguage.googleapis.com/v1beta/openai/"


external_client = AsyncOpenAI(
    api_key = key_gemini,
    base_url = base_url_gemini
)


model_gemini = OpenAIChatCompletionsModel(
    model ="gemini-2.0-flash",
    openai_client= external_client
)

config = RunConfig(
    model = model_gemini,
    model_provider=external_client,
    tracing_disabled=True
)

@function_tool
def weather_tool(wrapper:RunContextWrapper[user_info],location:str)->str:
    print(wrapper.context)
    return f"in the city {location} weather is cloudy temperature is 55c"
simple_agent = Agent(
    name="simple agent",
    instructions="this is a simple agent can provide the simple answers",
    tools=[weather_tool],
    output_type=weather
)

result = Runner.run_sync(
    simple_agent,
    "what is the weather in karachi city ",
    run_config=config,
    context=userObj

)
print(result.final_output)