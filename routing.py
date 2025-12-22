import asyncio
import uuid
from openai.types.responses import ResponseTextDeltaEvent,ResponseContentPartDoneEvent
from agents import Agent,Runner,RawResponsesStreamEvent,TResponseInputItem,trace
from config import config

spanish_agent= Agent(
    name="spanish_agent",
    instructions="you are spanish agent you take the input in english and translate it into spanish"
)

german_agent= Agent(
    name="german_agent",
    instructions="you are german agent you take the input in english and translate it into german"
)

french_agent=Agent(
    name="french_agent",
    instructions="you are french agent you take the input in english and translate it into frech"
)

triage_agent= Agent(
    name="triage_agent",
    instructions="you are triage agent you take the inputs and handoff to the appropriate agent",
    handoffs=[spanish_agent,french_agent,german_agent]
)


async def main():
    msg = input("Hello we can speak spanish german and french what would you like to speak in?")
    input_item:list[TResponseInputItem] = [{"content":msg,"role":"user"}]
    agent = triage_agent

    conversation_id = str(uuid.uuid4().hex[:16])
    while True:
        

        with trace("routing", group_id= conversation_id):
            response = Runner.run_streamed(agent,input_item,run_config=config)
            async for event in response.stream_events():
                # print(event)
                if not isinstance(event,RawResponsesStreamEvent):
                    # print("not rawresponsestreamenent")
                    continue
                data = event.data
                if isinstance(data, ResponseTextDeltaEvent):
                    
                    print(data.delta, end="", flush=True)
                elif isinstance(event, ResponseContentPartDoneEvent):
                    print("\n")
                
            msg = input("Enter the message for translation")
            input_item.append({"role":"user","content":msg})
            agent = response.current_agent
            print("\n")
if __name__=="__main__":
    asyncio.run(main())