"""
Quick test of LangChain and LangGraph functionality
NOTE: Requires OPENAI_API_KEY in environment
"""

import os
from typing import TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

# Load environment variables
load_dotenv()

# Check for API key
if not os.getenv("OPENAI_API_KEY"):
    print("Warning: OPENAI_API_KEY not found in environment")
    print("Set it in .env file or export it: export OPENAI_API_KEY='your-key'")
    exit(1)

# Define a simple state
class SimpleState(TypedDict):
    message: str
    count: int

# Create a simple agent node
def agent_node(state: SimpleState) -> dict:
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    response = llm.invoke(f"Say hello in a creative way. Current count: {state['count']}")
    return {
        "message": response.content,
        "count": state["count"] + 1
    }

# Build the graph
def test_langgraph():
    print("Testing LangGraph with LangChain...\n")
    
    # Create graph
    graph = StateGraph(SimpleState)
    
    # Add node
    graph.add_node("agent", agent_node)
    
    # Set entry point
    graph.set_entry_point("agent")
    
    # Add edge to end
    graph.add_edge("agent", END)
    
    # Compile
    app = graph.compile()
    
    # Run
    initial_state = {
        "message": "",
        "count": 0
    }
    
    print("Running graph...")
    result = app.invoke(initial_state)
    
    print(f"\n✓ Graph executed successfully!")
    print(f"Message: {result['message']}")
    print(f"Count: {result['count']}")

if __name__ == "__main__":
    test_langgraph()