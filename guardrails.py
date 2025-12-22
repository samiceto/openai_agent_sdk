from config import config
from agents import Agent,Runner,input_guardrail,RunContextWrapper,TResponseInputItem,GuardrailFunctionOutput
from dataclasses import dataclass
@input_guardrail
async def main_guardrail(
        context:RunContextWrapper[None],
        agent:Agent,
        input:str|list[TResponseInputItem]

)->GuardrailFunctionOutput:
    print("input>>>",input)
    user_type = "user"
    return GuardrailFunctionOutput(
        output_info="Guardrail fails",
        tripwire_triggered=user_type == "admin"
    )

agent = Agent(
    name="simple agent",
    instructions="you are simple agent",
    input_guardrails=[main_guardrail]
)

result = Runner.run_sync(
    agent,
    "what is america capital",
    run_config=config
)
print(result.final_output)