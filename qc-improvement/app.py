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
from settings import settings

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

class UserInput(BaseModel):
    input: str
    response_format: object = response_format
    model: str = "gemini-2.0-flash-lite"

@app.on_event("startup")
async def startup_event():
    """Initialize resources when the application starts"""
    global client, system_prompt, response_format, model, table_heads
    
    try:
        client, model = LLMFactory.create(provider='gemini')

        with open("../prompt/system_prompt.md", "r", encoding="utf-8") as f:
            system_prompt = f.read()

        with open("../json/schema_v2.json", "r", encoding="utf-8") as f:
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

@app.post("/generate")
async def generate_test_case(user_request: UserInput = Body(...)):
    """Generate test cases based on user input"""
    try:
        # Check if initialization was successful
        if client is None or model is None:
            raise HTTPException(status_code=500, detail="API not properly initialized")
        
        # Generate completion
        completion = client.chat.completions.create(
            model=user_request.model if user_request.model else model,
            messages=[
                {"role": "developer", "content": system_prompt},
                {"role": "user", "content": user_request.input}
            ],
            response_format=user_request.response_format if user_request.response_format else response_format
        )
        
        # Process and save output
        output = json.loads(completion.choices[0].message.content)
        output["test_case_properties"] = table_heads
        
        os.makedirs("../json", exist_ok=True)
        with open("../json/response.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(output, indent=2))
        
        # Return stats and output
        return {
            "model_used": completion.model,
            "tokens_used": completion.usage.total_tokens,
            "result": output
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating test case: {str(e)}")


class ExportRequest(BaseModel):
    data: Dict[str, Any]
    filename: Optional[str] = None


@app.post("/export/excel")
async def export_to_excel(request: ExportRequest = Body(...)):
    filename = request.filename if request.filename else f"test_case_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    data = request.model_dump().get("data", {})
    head_data = data.get("test_case_properties", {})
    user_stories = data.get("user_stories", [])
    row_data = []
    for story in user_stories:
        if "test_cases" in story:
            row_data.extend(story["test_cases"])

    heads = {key: head_data[key]["value"] 
                   for key in head_data}
    
    df = pd.DataFrame(data=row_data )
    
    return StreamingResponse(
        iter([df.to_csv(index=False)]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=data.csv"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)