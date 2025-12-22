from agents import Agent,Runner,handoff,RunContextWrapper
from config import config
from pydantic import BaseModel

class refund_data(BaseModel):
    reason:str 

refund_agent = Agent(name="refund_agent")
bulling_agent = Agent(name="billing_agent")



def on_handoff(context:RunContextWrapper,input:refund_data):
    print(f"on handoff occurd reason {input.reason}")

agent = Agent(
    name= "simple agent",
    instructions="you are simple agent use handoffs",
    handoffs=[
       
        bulling_agent,
        handoff(
            agent=refund_agent,
            input_type=refund_data,
            on_handoff=on_handoff
        )
    ]
)

result = Runner.run_sync(agent,"i want to refund the product cost 200 dollar, becaouse the product is not working as expected",run_config=config)
print(result.final_output)