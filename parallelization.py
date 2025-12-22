import asyncio
from agents import Agent,Runner,ItemHelpers,trace,TResponseInputItem
from config import config 

spanish_agent = Agent(
    name= "spanish_agent",
    instructions="you are spanish agent you take the input in english and translate it into spanish"
)


best_picker= Agent(
    name= "best_picker",
    instructions="you are best picker agent you take the input and pick the best one"
)


async def main():
    msg = input("Enter the message for translation into spanish")
    input_item:TResponseInputItem = [{"content":msg,"role":"user"}]
    with trace("paralization"):
        res1,res2,res3 =await asyncio.gather(
            Runner.run(
                spanish_agent,
                input_item,
                run_config=config
            ),
            Runner.run(
                spanish_agent,
                input_item,
                run_config=config
            ),
            Runner.run(
                spanish_agent,
                input_item,
                run_config=config
            )
        )

        outputs=[
            ItemHelpers.text_message_outputs(res1.new_items),
            ItemHelpers.text_message_outputs(res2.new_items),
            ItemHelpers.text_message_outputs(res3.new_items)
        ]

        translations = "\n\n ".join(outputs)
        print(f"\n\n translations: \n\n{translations}")

        best_translation =await Runner.run(
            best_picker,
            f"input {input_item}\n\n translations: {translations}",
            run_config=config
        )
        print("best translation picked is:",best_translation.final_output)

if __name__=="__main__":
    asyncio.run(main()) 

