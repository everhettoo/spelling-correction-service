# The simple rest endpoint /review/?text=data is implemented here, in the main file.
# Please refer to 'tests/test_main.py' to understand how the endpoint is consumed.
import uvicorn
from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app_config import Configuration
from models.document import Document
from pipeline.text_pipeline import TextPipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow only this frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Import app config.
config = Configuration()


class InputText(BaseModel):
    input_text: str


@app.post("/review")
async def review_text(data: InputText):
    # Create and initialize payload container for text process pipelines.
    doc = Document(data.input_text)
    processor = TextPipeline(config)
    processor.execute_asc_pipeline(doc)

    if processor.err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=processor.err_msg)

    return {"doc": doc}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
