from email import message
from json import load
from llm_factory import LLMFactory
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
import os
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# Load system prompt from a markdown file
with open("system_prompt.md", "r", encoding="utf-8") as f:
    system_prompt = f.read()

llm: BaseChatModel = LLMFactory.create(
        temperature=0.7,
        streaming=True
    )

chat_template = ChatPromptTemplate.from_messages(
    [
        ("system", "{system}."),
        ("human", "{user_input}"),
    ]
)

user_input = """
create for login flows: login with username password, login with OTP
"""

prompt = chat_template.format_messages(system=system_prompt, user_input=user_input)

parser = StrOutputParser()

from pydantic import BaseModel, Field
from typing import List, Literal


def health():
    """
    Check the health of the LLM.
    """
    res = llm.invoke("Who are you")
    print(llm.get_name())
    print(res)

def structure_response():

    res = llm.invoke("Who are you")
    print(res)

async def stream_chunks(llm, prompt):
    """
    Streams chunks from the LLM and returns them as a list.
    """
    chunks = []
    async for chunk in llm.astream(prompt):
        chunks.append(chunk)
        print(chunk.content, end="|", flush=True)
    return chunks

def main():
    # Call the async function to stream chunks
    import asyncio
    chunks = asyncio.run(stream_chunks(llm, prompt))
    print("\nCollected chunks:", chunks)




if __name__ == "__main__":
    structure_response()
