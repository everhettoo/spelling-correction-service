import uvicorn
from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager

from app_config import Configuration
from models.document import Document
from pipeline.text_pipeline import TextPipeline
from pipeline.bigram_pipeline import BigramPipeline
from datetime import datetime

# Import app config.
config = Configuration()

# Declare BigramPipeline globally
bigram_processor = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global bigram_processor
    bigram_processor = BigramPipeline()  # Load once at startup
    print("BigramPipeline initialized")
    yield
    bigram_processor = None  # Cleanup on shutdown
    print("BigramPipeline cleared")

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
    """Processes input text using text pipeline and bigram model."""
    global bigram_processor

    if not bigram_processor:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="BigramPipeline not initialized")

    current_time = datetime.now().time()
    print("text start Time:", current_time)
    doc = Document(data.input_text)
    processor = TextPipeline(config)
    processor.execute_asc_pipeline(doc)
    current_time = datetime.now().time()
    print("text end Time:", current_time)

    if processor.err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=processor.err_msg)

    current_time = datetime.now().time()
    print("bigrams start Time:", current_time)
    doc = bigram_processor.check_sentence(doc)
    current_time = datetime.now().time()
    print("bigrams end Time:", current_time)

    if bigram_processor.err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=bigram_processor.err_msg)

    return doc


@app.post("/bigrams")
async def update_bi_grams_model(data: InputText):
    """Updates the bigram model dynamically."""
    global bigram_processor

    if not bigram_processor:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="BigramPipeline not initialized")

    bigram_processor.update_bigrams(data.input_text)
    return {"result": "N-gram model updated"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
