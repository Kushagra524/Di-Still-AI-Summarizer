from fastapi import FastAPI
from pydantic import BaseModel
from app import summarize_url

app = FastAPI()

class URLRequest(BaseModel):
    url : str

@app.post("/summarize")
async def summarize(request : URLRequest):
    summary = summarize_url(request.url)
    return {"summary" : summary}
