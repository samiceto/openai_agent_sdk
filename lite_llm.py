import os
from dotenv import load_dotenv
load_dotenv()
from litellm.proxy.proxy_server import general_settings
from agents.extensions.models.litellm_model import LitellmModel
from agents import Agent,Runner

## set ENV variables
key=os.environ["OPENAI_API_KEY"]
model="openai/gpt-4.1"

def main() -> None:
    agent= Agent(
        name="simple_agent",
        model=LitellmModel(model=model,api_key=key),
    )
    result = Runner.run_sync(agent, "What is the capital of France?")
    print(result.final_output)
   

if __name__ == "__main__":
    main()  
