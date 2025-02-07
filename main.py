from fastapi import FastAPI, status

from models.text_payload import TextPayload
import uvicorn

app = FastAPI()


@app.get("/review/")
async def review_text(text: str):
    # Create payload for process pipelines.
    payload = TextPayload(text)

    # Detect character encoding and language. Returns tokens if the language is English.
    payload.tokenize_words()

    if payload.error:
        return {"status": status.HTTP_400_BAD_REQUEST, "payload": payload.error_msg}
    else:
        return {"status": status.HTTP_200_OK, "payload": payload}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
