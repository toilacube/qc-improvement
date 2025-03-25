from json import load
from llm_factory import LLMFactory
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from dotenv import load_dotenv
import os

load_dotenv()

llm: BaseChatModel = LLMFactory.create(
    provider="ollama",
    temperature=0.7,
    streaming=True
)

res: BaseMessage  = llm.invoke("who are you?")  

print(res)

