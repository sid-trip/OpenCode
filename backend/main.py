from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import uvicorn
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up NeuralDesk FastAPI backend...")
    yield
    print("Shutting down NeuralDesk FastAPI backend...")

app = FastAPI(title="NeuralDesk API", version="1.0.0", lifespan=lifespan)

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
