from typing import Annotated, Sequence, TypedDict
import operator
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode

from app.tools.builtins import get_tools
from app.core.models import get_model

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

def create_agent_graph(model_backend: str, cloud_provider: str):
    """Factory to create the LangGraph agent state machine."""
    tools = get_tools()
    llm = get_model(model_backend, cloud_provider)
    llm_with_tools = llm.bind_tools(tools)
    
    def call_model(state: AgentState):
        messages = state["messages"]
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}
        
    def should_continue(state: AgentState):
        last_message = state["messages"][-1]
        
        # If there is no tool call, then we finish
        if not getattr(last_message, "tool_calls", None):
            return "end"
        return "continue"
        
    workflow = StateGraph(AgentState)
    
    # M1 Node: LLM router block (Planner/Agent)
    workflow.add_node("agent", call_model)
    # M1 Node: Tool executor block
    workflow.add_node("tools", ToolNode(tools))
    
    workflow.add_edge(START, "agent")
    
    # Conditional edge from agent down to tools or End
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "tools",
            "end": END
        }
    )
    
    workflow.add_edge("tools", "agent")
    return workflow.compile()
