# The simple rest endpoint /review/?text=data is implemented here, in the main file.
# Please refer to 'tests/test_main.py' to understand how the endpoint is consumed.
import uvicorn
from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from models.document import Document
from pipeline.text_pipeline import TextPipeline
from pipeline.ngram_pipeline import NgramPipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow only this frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

class InputText(BaseModel):
    input_text: str

@app.post("/review")
async def review_text(data: InputText):
    # Create and initialize payload container for text process pipelines.
    doc = Document(data.input_text)
    processor = TextPipeline()
    processor.execute_asc_pipeline(doc)

    ngramProcessor = NgramPipeline(3)
    doc = ngramProcessor.check_sentence(doc)

    if processor.err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=processor.err_msg)

    return {"doc": doc}

@app.post("/ngram")
async def build_ngram(data: InputText):
    models = {
        "bigram": 2,
        "trigram": 3
    }

    for model_name, n in models.items():
        ngramProcessor = NgramPipeline(n)
        ngramProcessor.preprocess_build_model(data.input_text)
        ngramProcessor.print_model()

    return {"result": "N-gram model updated"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
