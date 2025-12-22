import os 
from dotenv import load_dotenv
from agents import Agent,Runner,function_tool,RunContextWrapper
load_dotenv()
from config import config
import json

@function_tool
async def get_weather(city:str):
    print("the weather tool")
    return f"the weather in {city} is 40cc"


@function_tool
async def samiullah_info(name:str):
    print("samiullah info")
    return f"the person {name} is the ai learner at ciaic"

@function_tool
def My_car_info(ctx:RunContextWrapper,path:str,diractory:str | None = None):
    full_path = os.path.join(path, diractory) if diractory else path
    with open(full_path, "r") as f:
        data = f.read()
        return data


agent = Agent(
    name="simple_agent",
    instructions ="you are simple assistant and you have tools, if you asked about weather or samiullah dont give answer form your end always use tools",
    tools=[get_weather,samiullah_info,My_car_info]
)

async def main():
    # result1,result2,result3=await asyncio.gather(
    #     Runner.run(agent,"tell me what is the waether in karachi and who is samiullah",run_config = config)
    #     ,

    #     Runner.run(agent,"tell me what is the waether in karachi and who is samiullah",run_config = config)
    #    ,

    #    Runner.run(agent,"tell me what is the waether in karachi and who is samiullah",run_config = config)
    #     ,
    # )
    # print(result1.final_output)
    # print(result2.final_output)
    # print(result3.final_output)






    result = await Runner.run(agent, "tell me what is the waether in karachi and who is samiullah and also tell me about my car when did i bought it the path is mycar.text and the directory '.' ")
    print(result.final_output)
    # for tool in agent.tools:
    #     print(json.dumps(tool.params_json_schema,indent=4),"**" *7)

if __name__=="__main__":
    import asyncio
    asyncio.run(main())