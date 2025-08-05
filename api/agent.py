from tools import tool_belt, tracer
from langchain_openai import ChatOpenAI
from typing import List, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
import operator
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.documents import Document

model = ChatOpenAI(model="gpt-4.1", temperature=0)
model = model.bind_tools(tool_belt)

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    context: List[Document]

def call_model(state):
    messages = state["messages"]
    response = model.invoke(messages, {
        "tags" : ["Foster research agent"],
        "callbacks": [tracer],
    })
    return {
        "messages": [response],
        "context": state.get("context", [])
    }

tool_node = ToolNode(tool_belt)

uncompiled_graph = StateGraph(AgentState)
uncompiled_graph.add_node("agent", call_model)
uncompiled_graph.add_node("action", tool_node)
uncompiled_graph.set_entry_point("agent")

def should_continue(state):
    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "action"
    
    return END

uncompiled_graph.add_conditional_edges(
    "agent",
    should_continue
)

uncompiled_graph.add_edge("action", "agent")
compiled_graph = uncompiled_graph.compile()