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
import base64

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

with open("../prompt/widget_captioning.md", "r", encoding="utf-8") as f:
    widget_captioning_prompt = f.read()

with open("../json/widget_cationing_schema.json", "r", encoding="utf-8") as f:
    widget_captioning_schema = json.load(f)

values = {
    "story_data": story_dataa,
    "cleaned_html": cleaned_html,
}

# Format the string with provided values
formatted_prompt = code_gen_prompt.format(**values)
with open("../prompt/ui_test_case_prompt_v2.md", "r", encoding="utf-8") as f:
            ui_system_prompt = f.read()
# widget captioning message

def health():
    """
    Check the health of the LLM.
    """
    models = client.models.list()
    for model in models:
        print(model.id)

def code_gen():
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

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def widget_captioning():

    base64_image1 = encode_image("../images/lottemart_login.png")
    base64_image2 = encode_image("../images/lottemart_login_otp.png")

    msg = [
        {
            "role": "developer",
            "content": widget_captioning_prompt
        },
        {
            "role": "user",
            "content": [
                 { "type": "text", 
                  "text":  "Perform widget captioning task on the following image: "
                  },
                  {
                    "type": "image_url",
                      "image_url":  {
                        "url": f"data:image/png;base64,{base64_image1}",
                         "detail": "high",
                    }
                  },
                  {
                    "type": "image_url",
                      "image_url":  {
                        "url": f"data:image/png;base64,{base64_image2}",
                         "detail": "high",
                    }
                  }
            ]
        }
    ]

    response = client.chat.completions.create(
        model=model,
        messages=msg,
        response_format=widget_captioning_schema,
    )

    print (f"tokens_used: {response.usage.total_tokens}")
    with open("../json/widget_captioning_output.json", "w", encoding="utf-8") as f:
        f.write(response.choices[0].message.content)


def create_knowledge(path: str, user_request: str):
    # read a directory and return a list of files with these names:
    # - requirements.md
    # - story-board.md
    # - widget.json
    # - common_rules.md

    with open(os.path.join(path, "requirements.md"), "r", encoding="utf-8") as f:
        requirements = f.read()
    with open(os.path.join(path, "story-board.md"), "r", encoding="utf-8") as f:
        ui_story_board = f.read()
    with open(os.path.join(path, "widget.json"), "r", encoding="utf-8") as f:
        widget = json.load(f)
    with open(os.path.join(path, "common_rules.md"), "r", encoding="utf-8") as f:
        common_rules = f.read()
    
        return f"""
    Based on some common rules and the project knowledge bases please generate test cases for the following user request: {user_request}:
    ## Common rules: {common_rules},
    ## Requirements: {requirements}, 
    ## UI story board: {ui_story_board}
    ## Figma design{ widget}
"""
    
def gen_test_case(user_request: str):

        msg = create_knowledge("../test-template/login-test" ,user_request)
        # Generate completion
        completion = client.chat.completions.create(
            # model=user_request.model if user_request.model else model,
            model = model,
            messages=[
                {"role": "developer", "content": ui_system_prompt},
                {"role": "user", "content": msg}
            ],
            # response_format=user_request.response_format if user_request.response_format else response_format,
            temperature=1.2,
        )

        output = completion.choices[0].message.content

        # Save the completion generate to a file
        with open("../json/request.txt", "w", encoding="utf-8") as f:
            f.write(f"user_request: {msg}\n")
            f.write(f"system_prompt: {ui_system_prompt}\n")
        

        
        os.makedirs("../json", exist_ok=True)
        with open("../json/response.txt", "w", encoding="utf-8") as f:
            f.write(output)
        
        # Return stats and output
        


if __name__ == "__main__":
    gen_test_case("Login UI testing")
