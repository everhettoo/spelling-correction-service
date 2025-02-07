import json

from fastapi import FastAPI, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from models.text_payload import TextPayload
import uvicorn

app = FastAPI()


@app.get("/review/")
async def review_text(text: str):
    # Create payload for process pipelines.
    payload = TextPayload(text)

    payload.tokenize_words()

    # Detect character encoding and language. Returns tokens if the language is English.
    if payload.get_error():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=payload.get_error_msg()
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(payload)

        )


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
