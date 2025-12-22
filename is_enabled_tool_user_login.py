from dataclasses import dataclass
from config import config
from agents import Agent, HandoffInputData,Runner,handoff,RunContextWrapper,function_tool
from agents.extensions import handoff_filters



@function_tool
def weather(location:str)->str:
    return f"the weather in {location} is sunny"


@dataclass
class user:
    userlogedin:bool

user1=user(userlogedin=True)

def is_enabled(ctx:RunContextWrapper[user],agent:Agent):
    return ctx.context.userlogedin

def main():

    refund_agent= Agent(
        name="refundAgent",
        tools=[weather],
        is_enabled=is_enabled
    )


    result = Runner.run_sync(refund_agent,"what is the weather today in karachi",context=user1)
    print(result.final_output)
if __name__=="__main__":
    main()


