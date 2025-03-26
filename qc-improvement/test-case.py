from email import message
from json import load
from llm_factory import LLMFactory
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
import os
from langchain_core.prompts import ChatPromptTemplate
from settings import settings

load_dotenv()

# Load system prompt from a markdown file
with open("system_prompt.md", "r", encoding="utf-8") as f:
    system_prompt = f.read()

llm = LLMFactory.create()

def health():
    """
    Check the health of the LLM.
    """
    models = llm.models.list()
    for model in models:
        print(model.id)

if __name__ == "__main__":
    health()
