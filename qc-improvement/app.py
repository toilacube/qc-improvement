from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from datetime import datetime

# Add this to your imports
from io import BytesIO
from tempfile import NamedTemporaryFile
import tempfile

import json
import os
from typing import Optional, Dict, List, Any

from llm_factory import LLMFactory
from enums import Agent
from testcase_prompt_factory import TestCasePromptFactory
from settings import settings

import pystache

app = FastAPI(title="Test Case Generator API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Global variables
client = None
system_prompt = None
response_format = None
model = None
table_heads = None
ui_system_prompt = None

class TestCaseGenRequest(BaseModel):
    input: str
    requirements: Optional[str] = None
    agent: str

@app.on_event("startup")
async def startup_event():
    """Initialize resources when the application starts"""
    global client, system_prompt, response_format, model, table_heads, ui_system_prompt
    
    try:
        client, model = LLMFactory.create(provider='gemini')

        with open("../prompt/system_prompt.md", "r", encoding="utf-8") as f:
            system_prompt = f.read()

        with open("../prompt/ui_test_case_prompt_v2.md", "r", encoding="utf-8") as f:
            ui_system_prompt = f.read()

        with open("../json/ui_testcase_schema_v2.json", "r", encoding="utf-8") as f:
            response_format = json.load(f)

        with open("../json/table_heads.json", "r", encoding="utf-8") as f:
            table_heads = json.load(f)
            
        print(f"Initialization complete: model {model}")
    except Exception as e:
        print(f"Error during initialization: {str(e)}")
        raise e

@app.get("/health")
async def health_check():
    """Check if the API and LLM are working"""
    try:
        completion = client.chat.completions.create(
            model="gemini-2.0-flash-lite",
            messages=[
                {"role": "developer", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is the capital of Vietnam?"}
            ],
            max_tokens=10
        )
        return {"status": "healthy", "message": completion.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")
    
def create_knowledge_base(path: str):

    # create data to render in mustache
    with open(os.path.join(path, "requirements.md"), "r", encoding="utf-8") as f:
        requirements = f.read()
    with open(os.path.join(path, "story-board.md"), "r", encoding="utf-8") as f:
        ui_story_board = f.read()
    with open(os.path.join(path, "widget.json"), "r", encoding="utf-8") as f:
        widget = json.load(f)
    with open(os.path.join(path, "common_rules.md"), "r", encoding="utf-8") as f:
        common_rules = f.read()

    knowledge = f"""
    ## Common rules: {common_rules},
    ## Requirements: {requirements}, 
    ## UI story board: {ui_story_board}
    ## Figma design{ widget}
"""

    data = {
        "knowledge_base": knowledge,
        "response_format": response_format,
    }
    with open("../test-template/prompt.mustache", "r", encoding="utf-8") as f:
        prompt_template = f.read()
    output = pystache.render(prompt_template, data)

    with open("../json/knowledge_base.md", "w", encoding="utf-8") as f:
        f.write(output)
    return output


def create_user_request(path: str, user_request: str):
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

@app.post("/generate")
async def generate_test_case(user_request: TestCaseGenRequest = Body(...)):
    """Generate test cases based on user input"""
    try:
        # Check if initialization was successful
        if client is None or model is None:
            raise HTTPException(status_code=500, detail="API not properly initialized")
        
        # Detect which agent to use
        sys_prompt = TestCasePromptFactory.load_template(user_request.agent, user_request.requirements)

        # Generate completion
        completion = client.chat.completions.create(
            model = model,
            messages=[
                {"role": "developer", "content": sys_prompt},
                {"role": "user", "content": user_request.input}
            ],
            response_format=response_format,
            temperature=0.7,
        )
        # Save the completion generate to a file
        with open("../json/request.txt", "w", encoding="utf-8") as f:
            f.write(f"system_prompt: {ui_system_prompt}\n")
        
        # Process and save output
        output = json.loads(completion.choices[0].message.content)
        # Add table heads to the output 
        output["test_case_properties"] = table_heads
        
        os.makedirs("../json", exist_ok=True)
        with open("../json/response.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(output, indent=2))
        
        # Return stats and output
        return {
            "model_used": completion.model,
            "tokens_used": completion.usage.total_tokens,
            "prompt_tokens": completion.usage.prompt_tokens,
            "completion_tokens": completion.usage.completion_tokens,
            "result": output
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating test case: {str(e)}")

# def create_full_output()

class ExportRequest(BaseModel):
    data: Dict[str, Any]
    filename: Optional[str] = None


@app.post("/export/excel")
async def export_to_excel(request: ExportRequest = Body(...)):
    filename = request.filename if request.filename else f"test_case_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    data = request.model_dump().get("data", {})
    head_data = data.get("test_case_properties", {})
    user_stories = data.get("user_stories", [])
    # Define the desired order of columns
    column_order = [
        "id", 
        "scenario_name", 
        "steps_to_execute", 
        "expected_result", 
        "menu", 
        "priority", 
        "automatable"
    ]
    
    # Process test cases
    row_data = []
    for story in user_stories:
        if "test_cases" in story:
            for test_case in story["test_cases"]:
                # Convert steps_to_execute array to string if needed
                if isinstance(test_case.get("steps_to_execute"), list):
                    test_case["steps_to_execute"] = "\n".join(test_case["steps_to_execute"])
                
                # Create ordered test case dict
                ordered_test_case = {field: test_case.get(field, "") for field in column_order}
                row_data.append(ordered_test_case)

    # Create DataFrame with ordered columns
    df = pd.DataFrame(data=row_data, columns=column_order)
    
    return StreamingResponse(
        iter([df.to_csv(index=False)]),
        media_type="text/csv",
        headers={f"Content-Disposition": f"attachment; filename={filename}.csv"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)