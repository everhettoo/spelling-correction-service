
from fastapi import FastAPI

import spelling_checker
from schemas import ReviewResponse
import uvicorn

app = FastAPI()

@app.get("/review/")
async def review_text(text: str):
    tokens = text.split(' ')

    res = ReviewResponse(text=text, tokens=tokens)
    res.process()
    return res


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
