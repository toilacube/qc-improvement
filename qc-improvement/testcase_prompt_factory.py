# create enum for agent type
import json
import os 
import pystache

from enums import Agent


def create_prompt(requirements: str, template_file_path: str):

    knowledge = f"""
    ## Requirements: {requirements}, 
"""
    with open("../json/ui_testcase_schema_v2.json", "r", encoding="utf-8") as f:
        response_format = json.load(f)

    data = {
        "knowledge_base": knowledge,
        "response_format": response_format,
    }
    with open(template_file_path, "r", encoding="utf-8") as f:
        prompt_template = f.read()
    output = pystache.render(prompt_template, data)

    with open("../json/knowledge_base.md", "w", encoding="utf-8") as f:
        f.write(output)
    return output


class TestCasePromptFactory:
    @staticmethod
    def load_template(testing_type: str, requirements: str):
        """
        Create a test case generation agent instance based on the testing type
        """
        print(f"Creating test case generation agent with type: {testing_type}")

        if testing_type.lower() == Agent.UI.value:
            template_file_path = "../test-template/agent-prompt-template/ui-testing.mustache"
            return create_prompt(requirements, template_file_path)
        elif testing_type.lower() == Agent.FUNCTIONAL.value:
            return 
        else:
            raise ValueError(f"Unsupported testing type: {testing_type}")