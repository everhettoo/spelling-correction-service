from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app_config import Configuration
from models.document import Document
from pipeline.text_pipeline import TextPipeline
from utils.duration import Timer

# Import app config.
config = Configuration()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f'[Service] - initializing ...')
    # TODO: If any config needs initialization.
    yield
    # TODO: If any config needs de-initialization.
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
def review_text(data: InputText):
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

    return doc


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
