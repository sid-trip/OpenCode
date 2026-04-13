from app.agent.graph import create_agent_graph
from langchain_core.messages import HumanMessage


def _to_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict):
                text = item.get("text")
                if text:
                    parts.append(str(text))
            elif item:
                parts.append(str(item))
        return "".join(parts)
    return str(content)


class OpenCodeAgent:
    def __init__(self, model_backend: str, cloud_provider: str, workspace: str):
        self.model_backend = model_backend
        self.cloud_provider = cloud_provider
        self.workspace = workspace
        self.app = create_agent_graph(model_backend, cloud_provider)

    def invoke(self, instruction: str):
        """Invoke a single shot generation with the compiled LangGraph setup."""
        inputs = {"messages": [HumanMessage(content=instruction)]}
        result = self.app.invoke(inputs)
        # result is a dict with our state, the last message is what we want
        return _to_text(result["messages"][-1].content)

    def stream(self, instruction: str):
        """Stream real chunks from the LangGraph agent."""
        inputs = {"messages": [HumanMessage(content=instruction)]}
        # In stream_mode="messages", langgraph emits raw base messages/chunks
        for chunk in self.app.stream(inputs, stream_mode="messages"):
            msg, metadata = chunk
            
            # Print content delta chunks as they arrive for streaming
            if msg.content:
                yield _to_text(msg.content)
                
            # If the model requested tools, tell the user gracefully
            if msg.additional_kwargs.get("tool_calls"):
                for tc in msg.additional_kwargs["tool_calls"]:
                    func = tc["function"]
                    yield f"\n[Agent running tool: {func['name']} with args: {func['arguments']}]\n"
