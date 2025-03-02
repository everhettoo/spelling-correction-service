# The simple rest endpoint /review/?text=data is implemented here, in the main file.
# Please refer to 'tests/test_main.py' to understand how the endpoint is consumed.
import uvicorn
import pandas as pd
from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app_config import Configuration
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

    ngramProcessor = NgramPipeline(3)
    doc = ngramProcessor.check_sentence(doc)

    if processor.err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=processor.err_msg)

    # return {"doc": doc}
    return doc

@app.post("/ngram")
async def build_ngram(data: InputText):
    models = {
        "trigram": 3
    }

    # df = pd.read_csv('data/cleanse-data.csv')
    #
    # i = 0
    # cl_text = ''
    #
    # try:
    #     for text in df['cleansed']:
    #         cl_text = cl_text + '' + text
    #         i += 1
    # except Exception as e:
    #     print(f'Exception {e} in {i}.')
    #
    # print("clean text:", cl_text)

    cl_text = data.input_text
    for model_name, n in models.items():
        ngramProcessor = NgramPipeline(n)
        ngramProcessor.preprocess_build_model(cl_text)
        ngramProcessor.print_model()

    return {"result": "N-gram model updated"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
