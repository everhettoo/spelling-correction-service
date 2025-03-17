from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app_config import Configuration
from models.document import Document
from pipeline.bigram_pipeline import BigramPipeline
from pipeline.text_pipeline import TextPipeline
from utils.duration import Timer

# Import app config.
config = Configuration()

# Declare BigramPipeline globally
bigram_processor = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global bigram_processor

    print(f'[Service] - initializing ...')
    bigram_processor = BigramPipeline()  # Load once at startup
    yield
    bigram_processor = None  # Cleanup on shutdown
    print(f'[Service] - shutting down ...')


app = FastAPI(lifespan=lifespan)

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
    """Processes input text using text pipeline and bi-gram model."""
    global bigram_processor
    timer = Timer()

    print(f'[Service] - received request ...')
    timer.start()
    print(f'[Service] - text preprocessing ...')
    doc = Document(data.input_text)
    processor = TextPipeline(config)
    processor.execute_asc_pipeline(doc)
    print(f'[Service] - text preprocessing completed in {timer.stop()} seconds.')

    if processor.err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=processor.err_msg)

    print(f'[Service] - bi-gram processing ...')
    timer.start()
    doc = bigram_processor.check_sentence(doc)
    print(f'[Service] - bi-gram processing completed in {timer.stop()} seconds.')

    if bigram_processor.err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=bigram_processor.err_msg)

    return doc


@app.post("/bigrams")
async def update_bi_grams_model(data: InputText):
    """Updates the bigram model dynamically."""
    global bigram_processor

    if not bigram_processor:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Bi-gramPipeline not initialized")

    bigram_processor.update_bigrams(data.input_text)
    return {"result": "N-gram model updated"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
