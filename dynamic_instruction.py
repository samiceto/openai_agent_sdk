from dataclasses import dataclass
from agents import Agent,Runner,RunContextWrapper
from config import config



@dataclass
class User:
    name: str
    age: int
    conversation:list[str]

    def update_conversation(self, message):
        self.conversation.append(message)

def system_prompts(context:RunContextWrapper[User],agent):
    print("context",context.context.name)
    return "you are simple asisstent"
agent = Agent(
    name="simple agent",
    instructions=system_prompts

)


user1 =User(name="ameen", age=20,conversation=[])


result = Runner.run_sync(
    agent,
    "hi",
    run_config=config,
    context=user1
)
print(result.final_output)
user1.update_conversation(result.final_output)
print(user1)