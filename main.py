# The simple rest endpoint /review/?text=data is implemented here, in the main file.
# Please refer to 'tests/test_main.py to understand how the endpoint is consumed.
from fastapi import FastAPI, status

from models.text_payload import TextPayload
import uvicorn

app = FastAPI()


@app.get("/review/")
async def review_text(text: str):
    # Create and initialize payload container for text process pipelines.
    payload = TextPayload(text)

    payload.detect_language_is_english()
    if payload.error:
        return format_error(payload)

    # Returns tokens if the language is English.
    payload.tokenize_words()
    if payload.error:
        return format_error(payload)

    payload.review()
    if payload.error:
        return format_error(payload)

    payload.text = ""
    return {"status": status.HTTP_200_OK, "payload": payload}


def format_error(payload: TextPayload):
    # Chop original text for payload size.
    payload.text = ""
    return {"status": status.HTTP_400_BAD_REQUEST, "payload": payload.error_msg}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
