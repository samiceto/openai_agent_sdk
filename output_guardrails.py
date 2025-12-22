from __future__ import annotations
from pydantic import BaseModel, Field
import asyncio
import json
from agents import (
    Agent,
    Runner,
    output_guardrail,
    OutputGuardrailTripwireTriggered,
    GuardrailFunctionOutput,
    RunContextWrapper
)
from config import config


class output_guardrail_output(BaseModel):
    reasoning:str = Field(description="reasoning for the output")
    responce : str = Field(description="response to the user")
    is_phone_number:bool = Field(description="if phone number")


@output_guardrail 
async def output_guardrail(ctx:RunContextWrapper[None],agent:Agent,output:output_guardrail_output)->GuardrailFunctionOutput:
    phone_number_in_reasoning = "716" in output.reasoning
    phone_number_in_responce = "716" in output.responce

    return GuardrailFunctionOutput(
        output_info={
            "phone number in reasoning":phone_number_in_reasoning,
            "phone number in responce":phone_number_in_responce
        },
        tripwire_triggered=phone_number_in_reasoning or phone_number_in_responce
    )


agent = Agent(
    name = "simple agent",
    instructions="you are general agent",
    output_type=output_guardrail_output,
    output_guardrails=[output_guardrail]
)

async def main():
     await Runner.run(agent, "what is america's capital", run_config=config)
     print("the first message pass")
    
     try:
         result = await Runner.run(agent,"my phone number is 716 what is my country", run_config=config)
         print("the second message pass if it is this should not be done, it's alarming")
         print(json.dumps(result.final_output.model.dump(), indent=2))

     except OutputGuardrailTripwireTriggered as e:
        print(f"the output contained the phone number {e.guardrail_result.output.output_info}")

if __name__=="__main__":
    asyncio.run(main())