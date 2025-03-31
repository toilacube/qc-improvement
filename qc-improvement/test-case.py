from email import message
from json import load
import json
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
with open("../prompt/system_prompt.md", "r", encoding="utf-8") as f:
    system_prompt = f.read()

client, model = LLMFactory.create(provider="gemini")

with open("../json/html.md", "r", encoding="utf-8") as f:
    cleaned_html = f.read()

story_dataa =     {
          "system": "Login",
          "menu": "Login Page",
          "priority": "High",
          "steps_to_execute": [
            "1. Navigate to the login page.",
            "2. Enter a valid username.",
            "3. Enter a valid password.",
            "4. Click the 'Login' button."
          ],
          "scenario_name": "Successful Login with Valid Credentials",
          "progress": "Ready",
          "expected_result": "User is successfully logged in and redirected to the home page or a designated landing page.",
          "testing_type": "Functional",
          "id": "AP-P4-01"
        }

with open("../prompt/playwright-code-gen.txt", "r", encoding="utf-8") as f:
    code_gen_prompt = f.read()

with open("../json/test_case_gen_schema.json", "r", encoding="utf-8") as f:
    case_gen_schema = json.load(f)

with open("../prompt/playwright-code-gen_v2.txt", "r", encoding="utf-8") as f:
    code_gen_prompt = f.read()

values = {
    "story_data": story_dataa,
    "cleaned_html": cleaned_html,
}

# Format the string with provided values
formatted_prompt = code_gen_prompt.format(**values)

def health():
    """
    Check the health of the LLM.
    """
    models = client.models.list()
    for model in models:
        print(model.id)

def field_require():
    history = [
        {
            "role": "developer",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": formatted_prompt
        }
    ]

    response = client.chat.completions.create(
        model=model,
        messages=history,
        response_format=case_gen_schema,
    )

    print (f"tokens_used: {response.usage.total_tokens}")

    with open("../json/playwright_code_gen_output.json", "w", encoding="utf-8") as f:
        f.write(response.choices[0].message.content)
    with open("../json/playwright_code_gen_output.py", "w", encoding="utf-8") as f:
        f.write(json.loads(response.choices[0].message.content).get("code"))

    print ()


if __name__ == "__main__":
    field_require()
