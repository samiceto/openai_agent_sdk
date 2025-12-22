from agents import Agent,Runner
from config import config
from pydantic import BaseModel
import json





class UserInfo(BaseModel):
    name: str | None = None
    age: int | None = None
    country: str | None = None
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


structural_agent=Agent(
    name="structural agent",
    instructions="take the user input and structure it",
    output_type=UserInfo
)

simple_agent=Agent(
    name="simple_agent",
    instructions="Collect user name, age, and country from their messages",
    tools=[
        structural_agent.as_tool(tool_name="structure_user_info",tool_description="structure user info")
    ],
    tool_use_behavior="stop_on_first_tool",

)

user_input=""
while True:
    
    if user_input == "":
        user = input("inter you name age and country separated by space")
        user_input += user

    result= Runner.run_sync(
        simple_agent,
        user_input,
        run_config=config
    )   


    # print(result.final_output[2])
    json_str = result.final_output


    data = json.loads(json_str)


    user_info = UserInfo(**data)


    if user_info.name is None:
        input_name = input("Enter your name: ")
        user_input += input_name
        continue
    if user_info.age is None:
        input_age = input("Enter your age: ")
        user_input += input_age
        continue
    if user_info.country is None:
        input_country = input("Enter your country: ")
        user_input += input_country
        continue


    # Now you can access fields individually
    print(user_info.name)     # e.g. "Majid"
    print(user_info.age)      # e.g. None or int
    print(user_info.country)  # e.g. None or str
    break
