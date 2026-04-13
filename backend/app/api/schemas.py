from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    model: str = "llama3"
    cloud_provider: str = ""
    workspace: str = "."
    session_id: str | None = None


class ChatResponse(BaseModel):
    session_id: str
    output: str


class MessageRecord(BaseModel):
    role: str
    content: str
    created_at: str


class SessionRecord(BaseModel):
    session_id: str
    model: str
    cloud_provider: str
    workspace: str
    created_at: str
