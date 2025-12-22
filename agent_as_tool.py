
import asyncio
from agents import Agent,Runner,ItemHelpers,MessageOutputItem,trace
from config import config


spanish_agent=Agent(
    name="spanish_agent",
    instructions="You translate the user's message to Spanish",
    handoff_description="An english to spanish translator",
)

french_agent=Agent(
    name="french_agent",
    instructions="you are french translator agent you translate from english to french",
    handoff_description="An english to french translator",
)
german_agent=Agent(
    name="german_agent",
    instructions="you are german translator agent you translate from english to german",
    handoff_description="An english to german translator",
)  


orchestrator_agent=Agent(
    name="orchestrator_agent",
    instructions="you are a translator agent you use relevent tools to translate the given content never translate your own but always use tools",
    tools=[
        spanish_agent.as_tool(
            tool_name="spanish_agent",
            tool_description="translate from english to spanish",
        ),
        french_agent.as_tool(
            tool_name="french_agent",
            tool_description="translate from english to french",
        ),
        german_agent.as_tool(
            tool_name="german_agent",
            tool_description="translate from english to german",
        ),
    ],
)
synthesizer_agent=Agent(
    name="synthesizer_agent",
    instructions="you are a synthesizer agent you inspect the translation correct if need ad give the final concatination"
)


async def main():
    mesg = input("Hi! What would you like translated, and to which languages? ")
    with trace("orchestrator tracing"):
        orchestrator_result = await Runner.run(orchestrator_agent,mesg)
        for item in orchestrator_result.new_items:
            if isinstance(item,MessageOutputItem):
                text = ItemHelpers.text_message_output(item)
                if text:
                    print(f"=Translate {text}")
        synthesizer_agent_result = await Runner.run(
            synthesizer_agent, orchestrator_result.to_input_list()
        )

        print(f"\n\nFinal Responce {synthesizer_agent_result.final_output}")

if __name__=="__main__":
    asyncio.run(main())    



