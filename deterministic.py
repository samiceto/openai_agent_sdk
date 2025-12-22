# import asyncio

# from pydantic import BaseModel

# from agents import Agent, Runner, trace
# from config import config

# """
# This example demonstrates a deterministic flow, where each step is performed by an agent.
# 1. The first agent generates a story outline
# 2. We feed the outline into the second agent
# 3. The second agent checks if the outline is good quality and if it is a scifi story
# 4. If the outline is not good quality or not a scifi story, we stop here
# 5. If the outline is good quality and a scifi story, we feed the outline into the third agent
# 6. The third agent writes the story
# """

# story_outline_agent = Agent(
#     name="story_outline_agent",
#     instructions="Generate a very short story outline based on the user's input.",
# )


# class OutlineCheckerOutput(BaseModel):
#     good_quality: bool
#     is_scifi: bool


# outline_checker_agent = Agent(
#     name="outline_checker_agent",
#     instructions="Read the given story outline, and judge the quality. Also, determine if it is a scifi story.",
#     output_type=OutlineCheckerOutput,
# )

# story_agent = Agent(
#     name="story_agent",
#     instructions="Write a short story based on the given outline.",
#     output_type=str,
# )


# async def main():
#     input_prompt = input("What kind of story do you want? ")

#     # Ensure the entire workflow is a single trace
#     with trace("Deterministic story flow"):
#         # 1. Generate an outline
#         outline_result = await Runner.run(
#             story_outline_agent,
#             input_prompt,
#             run_config=config
#         )
#         print("Outline generated")

#         # 2. Check the outline
#         outline_checker_result = await Runner.run(
#             outline_checker_agent,
#             outline_result.final_output,
#             run_config=config
#         )

#         # 3. Add a gate to stop if the outline is not good quality or not a scifi story
#         assert isinstance(outline_checker_result.final_output, OutlineCheckerOutput)
#         if not outline_checker_result.final_output.good_quality:
#             print("Outline is not good quality, so we stop here.")
#             exit(0)

#         if not outline_checker_result.final_output.is_scifi:
#             print("Outline is not a scifi story, so we stop here.")
#             exit(0)

#         print("Outline is good quality and a scifi story, so we continue to write the story.")

#         # 4. Write the story
#         story_result = await Runner.run(
#             story_agent,
#             outline_result.final_output,
#             run_config=config
#         )
#         print(f"Story: {story_result.final_output}")


# if __name__ == "__main__":
#     asyncio.run(main())





import asyncio 
from agents import Agent,Runner,trace
from pydantic import BaseModel
from config import config


story_outline_agent = Agent(
    name="story_outline_agent",
    instructions="you are a story outline maker agent, create the short story based on the input and the story should be cifi"
)
class story_outline_output(BaseModel):
    good_quality:bool
    scifi:bool

story_outline_checker= Agent(
    name="story_outline_checker",
    instructions="you check the given story outline wether it is a good quality and cifi",
    output_type=story_outline_output
)

story_agent=Agent(
    name="story_agent",
    instructions="you are the story agent you create a story based on the given outline",
    output_type=str
)


async def main():
    input_prompt=input("what kind of story you want to create?")
    with trace("determinstic trace"):
        story_outline_result = await Runner.run(
            story_outline_agent,
            input_prompt,
            run_config=config
        )
        print("outline generated")

        story_outline_checker_result =await Runner.run(
            story_outline_checker,
            story_outline_result.final_output,
            run_config=config
        )
        assert isinstance(story_outline_checker_result.final_output,story_outline_output)
        if not story_outline_checker_result.final_output.good_quality:
            print("the story is not good quality we have to stop proccessing")
            exit(0)
        if not story_outline_checker_result.final_output.scifi:
            print("the story is not scifi we have to stop proccessing")
            exit(0)

        print("The sory outline is a good quality we are moving forword")

        story_agent_result = await Runner.run(
            story_agent,
            story_outline_result.final_output,
            run_config=config
        )
        print(f"story: {story_agent_result.final_output}")

if __name__=="__main__":
    asyncio.run(main())