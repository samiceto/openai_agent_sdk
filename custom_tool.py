import os
from dotenv import load_dotenv
from agents import Agent,Runner, StopAtTools,function_tool,RunContextWrapper,ModelSettings,FunctionTool

load_dotenv()
from config import config
from pydantic import BaseModel


class my_info(BaseModel):
    name: str
    mobile:str

def samiullah_work_info(data:str):
    
    return f"the data:{data} done"
async def run_samiullah_info(ctx:RunContextWrapper,args:my_info):
    parsed = my_info.model_validate_json(args)
    print(args)
    print(type(parsed))
    if isinstance(parsed,my_info):
        print("yes")
        return samiullah_work_info(f"the data from the llm is name{parsed.name} and mobile{parsed.mobile}")
    else:
        print("error while validating the json schema of my_info class")


samiullah_info = FunctionTool(
    name = "samiullah_info",
    description = "this is the function tool to get the samiullah info",
    params_json_schema=my_info.model_json_schema(),
    on_invoke_tool=run_samiullah_info
)

agent = Agent(
    name="simple_agent",
    instructions ="you are simple assistant and you have tools, if you asked about weather or samiullah dont give answer form your end always use tools",
    tools=[samiullah_info],
    tool_use_behavior="stop_on_first_tool"
)

async def main():
    
    result = await Runner.run(agent, "tell me  who is samiullah ")
    print(result.final_output)

if __name__=="__main__":
    import asyncio
    asyncio.run(main())