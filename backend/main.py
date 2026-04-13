from contextlib import asynccontextmanager
import json

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import uvicorn

from app.agent.core import OpenCodeAgent
from app.api.schemas import ChatRequest, ChatResponse
from app.memory.history import (
    add_message,
    ensure_session,
    get_session_messages,
    init_db,
    list_sessions,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up OpenCode FastAPI backend...")
    init_db()
    yield
    print("Shutting down OpenCode FastAPI backend...")

app = FastAPI(title="OpenCode API", version="1.0.0", lifespan=lifespan)

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/chat/run", response_model=ChatResponse)
def run_chat(payload: ChatRequest):
    session_id = ensure_session(
        model=payload.model,
        cloud_provider=payload.cloud_provider,
        workspace=payload.workspace,
        session_id=payload.session_id,
    )

    add_message(session_id, "user", payload.message)

    agent = OpenCodeAgent(
        model_backend=payload.model,
        cloud_provider=payload.cloud_provider,
        workspace=payload.workspace,
    )
    output = agent.invoke(payload.message)
    add_message(session_id, "assistant", output)
    return ChatResponse(session_id=session_id, output=output)


@app.post("/chat/stream")
def stream_chat(payload: ChatRequest):
    session_id = ensure_session(
        model=payload.model,
        cloud_provider=payload.cloud_provider,
        workspace=payload.workspace,
        session_id=payload.session_id,
    )

    add_message(session_id, "user", payload.message)

    agent = OpenCodeAgent(
        model_backend=payload.model,
        cloud_provider=payload.cloud_provider,
        workspace=payload.workspace,
    )

    def event_stream():
        chunks: list[str] = []
        try:
            for chunk in agent.stream(payload.message):
                chunks.append(chunk)
                data = {"session_id": session_id, "chunk": chunk}
                yield f"data: {json.dumps(data)}\n\n"
        except Exception as exc:  # pragma: no cover
            err = {"session_id": session_id, "error": str(exc)}
            yield f"data: {json.dumps(err)}\n\n"
        finally:
            final_output = "".join(chunks)
            if final_output:
                add_message(session_id, "assistant", final_output)

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@app.get("/history/sessions")
def get_sessions(limit: int = 50):
    return {"sessions": list_sessions(limit=limit)}


@app.get("/history/sessions/{session_id}")
def get_session(session_id: str):
    messages = get_session_messages(session_id)
    if not messages:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"session_id": session_id, "messages": messages}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
