from llm_factory import LLMFactory
from settings import settings

import json
import os
    
client = None
system_prompt = None
response_format = None
model = None

def init():
    global client, system_prompt, response_format, model
    
    client, model = LLMFactory.create(provider = 'gemini')


    with open("../prompt/system_prompt.md", "r", encoding="utf-8") as f:
        system_prompt = f.read()

    with open("../json/schema_v2.json", "r", encoding="utf-8") as f:
        response_format =  json.load(f)

    print(f"init status: model {model}")

def health():
    completion = client.chat.completions.create(
        model="gemini-2.0-flash-lite",
        messages=[
            {"role": "developer", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the capital of vietnam!"}
        ],
        stream=True
    )

    for chunk in completion:
        print(chunk.choices[0].delta.content, end='')



def generate_test_case(input: str):
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "developer", "content": system_prompt},
            {"role": "user", "content": input}
        ],
        response_format=response_format
    )
    with open("../json/response.json", "w", encoding="utf-8") as f:
        f.write(completion.choices[0].message.content)
    print(f"Model used: {completion.model}")
    print(f"Usage: {completion.usage.total_tokens} tokens")


if __name__ == "__main__":
    init()
    user_input = """
        Login flow with username and password
"""
    # health()
    generate_test_case(user_input)
    # check_format()

    # print(response_format)