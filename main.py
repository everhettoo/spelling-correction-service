# The simple rest endpoint /review/?text=data is implemented here, in the main file.
# Please refer to 'tests/test_main.py to understand how the endpoint is consumed.
import uvicorn
from fastapi import FastAPI, status, HTTPException

from models.document import Document
from pipeline.text_pipeline import TextPipeline

app = FastAPI()


@app.get("/review")
async def review_text(input_text: str):
    # Create and initialize payload container for text process pipelines.
    doc = Document(input_text)
    processor = TextPipeline(doc)
    processor.execute_asc_pipeline()

    if processor.err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=processor.err_msg)

    return {"doc": doc}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
