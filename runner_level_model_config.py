

# Runner level 
import os
from dotenv import load_dotenv
from agents import OpenAIChatCompletionsModel,AsyncOpenAI
from agents.run import RunConfig

load_dotenv()

key_gemini = os.getenv("key_gemini")
model=os.getenv("GEMINI_MODEL")
base_url_gemini = "https://generativelanguage.googleapis.com/v1beta/openai/"


external_client = AsyncOpenAI(
    api_key = key_gemini,
    base_url = base_url_gemini
)


model_gemini = OpenAIChatCompletionsModel(
    model =model,
    openai_client= external_client
)

config = RunConfig(
    model = model_gemini,
    model_provider=external_client,
    tracing_disabled=True
)
