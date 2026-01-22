"""Agent implementations for the multi-agent RAG flow.

This module defines three LangChain agents (Retrieval, Summarization,
Verification) and thin node functions that LangGraph uses to invoke them.
"""

from typing import List

from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI
from .state import QAState
from ..llm.factory import create_chat_model

from .prompts import (
    RETRIEVAL_SYSTEM_PROMPT,
    SUMMARIZATION_SYSTEM_PROMPT,
    VERIFICATION_SYSTEM_PROMPT,
    PLANNING_SYSTEM_PROMPT
)
from .state import QAState
from .tools import retrieval_tool

def _extract_last_ai_content(messages: List[object]) -> str:
    """Extract the content of the last AIMessage in a messages list."""
    for msg in reversed(messages):
        if isinstance(msg, AIMessage):
            return str(msg.content)
    return ""

# Define agents at module level for reuse
retrieval_agent = create_agent(
    model=create_chat_model()   ,
    tools=[retrieval_tool],
    system_prompt=RETRIEVAL_SYSTEM_PROMPT,
)

summarization_agent = create_agent(
    model=create_chat_model(),
    tools=[],
    system_prompt=SUMMARIZATION_SYSTEM_PROMPT,
)

verification_agent = create_agent(
    model=create_chat_model(),
    tools=[],
    system_prompt=VERIFICATION_SYSTEM_PROMPT,
)

verification_agent = create_agent(
    model=create_chat_model(),
    tools=[],
    system_prompt=PLANNING_SYSTEM_PROMPT,
)

def create_planning_agent():
    """
    Creates the Query Planning Agent.
    This agent analyzes questions and creates search strategies.
    
    Returns:
        ChatOpenAI: Configured planning agent
    """
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",  
        temperature=0.0  
    )
    
    return llm

def planning_agent_node(state: dict) -> dict:
    """
    Node function that executes the planning agent.
    
    This is what gets called in the graph.
    
    Args:
        state: Current QAState
        
    Returns:
        dict: Updated state with plan and sub_questions
    """
    # Get the user's question
    question = state["question"]
    
    # Create the planning agent
    agent = create_planning_agent()
    
    # Create the message for the agent
    messages = [
        {"role": "system", "content": PLANNING_SYSTEM_PROMPT},
        {"role": "user", "content": f"Question: {question}"}
    ]
    
    # Invoke the agent
    response = agent.invoke(messages)
    
    # Extract the response content
    plan_response = response.content
    
    # Parse the response to extract plan and sub-questions
    plan, sub_questions = parse_planning_response(plan_response)
    
    # Print for debugging
    print("\n" + "="*60)
    print("🧠 PLANNING AGENT OUTPUT")
    print("="*60)
    print(f"Original Question: {question}")
    print(f"\nPlan:\n{plan}")
    print(f"\nSub-questions: {sub_questions}")
    print("="*60 + "\n")
    
    # Return updated state
    return {
        "plan": plan,
        "sub_questions": sub_questions
    }


def parse_planning_response(response: str) -> tuple[str, list[str]]:
    """
    Parse the planning agent's response to extract plan and sub-questions.
    
    Args:
        response: Raw response from planning agent
        
    Returns:
        tuple: (plan_text, list_of_sub_questions)
    """
    plan = ""
    sub_questions = []
    
    lines = response.split('\n')
    current_section = None
    
    for line in lines:
        line = line.strip()
        
        # Detect sections
        if 'PLAN:' in line.upper():
            current_section = 'plan'
            # Get text after "PLAN:"
            plan_text = line.split(':', 1)[-1].strip()
            if plan_text:
                plan = plan_text
            continue
            
        if 'SUB-QUESTION' in line.upper() or 'SUB QUESTION' in line.upper():
            current_section = 'sub_questions'
            continue
        
        # Collect content
        if current_section == 'plan' and line:
            if not line.startswith(('1.', '2.', '3.', '4.', '5.', '-')):
                plan += " " + line
                
        elif current_section == 'sub_questions' and line:
            # Extract sub-question (remove numbering and quotes)
            if line[0].isdigit() or line.startswith('-'):
                # Remove leading number/dash and quotes
                cleaned = line.lstrip('0123456789.-) ').strip('"\'')
                if cleaned:
                    sub_questions.append(cleaned)
    
    # Fallback: if parsing failed, use the whole response as plan
    if not plan and not sub_questions:
        plan = response
        # Try to extract any quoted strings as sub-questions
        import re
        quoted = re.findall(r'"([^"]*)"', response)
        sub_questions = quoted if quoted else [response]
    
    return plan.strip(), sub_questions


def retrieval_node(state: QAState) -> dict:
    """
    Enhanced Retrieval Agent node: gathers context from vector store using planning.

    This node:
    - Reads the user's question AND the planning output (plan, sub_questions)
    - Sends an enhanced message to the Retrieval Agent that includes:
      * Original question
      * Search strategy from planning
      * Decomposed sub-questions
    - The agent uses the retrieval tool to fetch document chunks
    - Extracts the tool's content (CONTEXT string) from ToolMessage
    - Stores the consolidated context string in state["context"]
    
    The planning information helps the agent make more targeted,
    comprehensive retrieval calls.
    """
    # Get data from state
    question = state["question"]
    plan = state.get("plan", "")
    sub_questions = state.get("sub_questions", [])
    
    # Debug logging
    print("\n" + "="*70)
    print("📚 RETRIEVAL NODE - Enhanced with Planning")
    print("="*70)
    print(f"Original Question: {question}")
    print(f"Has Plan: {bool(plan)}")
    print(f"Sub-questions: {len(sub_questions) if sub_questions else 0}")
    print("="*70)
    
    # Build enhanced retrieval message
    # If we have planning information, use it. Otherwise, use just the question.
    if plan and sub_questions:
        # ENHANCED MODE: Include planning information
        retrieval_message = f"""You are retrieving information to answer this question: {question}

SEARCH STRATEGY:
{plan}

FOCUS AREAS (Sub-questions to address):
"""
        for i, sub_q in enumerate(sub_questions, 1):
            retrieval_message += f"{i}. {sub_q}\n"
        
        retrieval_message += """
Use the retrieval tool to search for relevant information. You may:
- Make multiple retrieval calls for different aspects
- Search for each sub-question if needed
- Gather comprehensive context covering all focus areas

Focus on retrieving diverse, relevant chunks that address all aspects of the question."""
    
    else:
        # FALLBACK MODE: No planning available, use original question
        retrieval_message = question
        print("ℹ️  No planning information available - using direct question")
    
    print(f"\n📤 Sending to Retrieval Agent:")
    print(f"{retrieval_message[:200]}..." if len(retrieval_message) > 200 else retrieval_message)
    print()
    
    # Invoke the retrieval agent
    result = retrieval_agent.invoke({"messages": [HumanMessage(content=retrieval_message)]})
    
    messages = result.get("messages", [])
    context = ""
    
    # Extract context from ToolMessage(s)
    # Prefer the last ToolMessage content (from retrieval_tool)
    tool_messages_found = 0
    for msg in reversed(messages):
        if isinstance(msg, ToolMessage):
            context = str(msg.content)
            tool_messages_found += 1
            break
    
    print(f"✓ Retrieved context: {len(context)} characters")
    print(f"✓ Tool messages found: {tool_messages_found}")
    print("="*70 + "\n")
    
    return {
        "context": context,
    }

def summarization_node(state: QAState) -> QAState:
    """Summarization Agent node: generates draft answer from context.

    This node:
    - Sends question + context to the Summarization Agent.
    - Agent responds with a draft answer grounded only in the context.
    - Stores the draft answer in `state["draft_answer"]`.
    """
    question = state["question"]
    context = state.get("context")

    user_content = f"Question: {question}\n\nContext:\n{context}"

    result = summarization_agent.invoke(
        {"messages": [HumanMessage(content=user_content)]}
    )
    messages = result.get("messages", [])
    draft_answer = _extract_last_ai_content(messages)

    return {
        "draft_answer": draft_answer,
    }


def verification_node(state: QAState) -> QAState:
    """Verification Agent node: verifies and corrects the draft answer.

    This node:
    - Sends question + context + draft_answer to the Verification Agent.
    - Agent checks for hallucinations and unsupported claims.
    - Stores the final verified answer in `state["answer"]`.
    """
    question = state["question"]
    context = state.get("context", "")
    draft_answer = state.get("draft_answer", "")

    user_content = f"""Question: {question}

Context:
{context}

Draft Answer:
{draft_answer}

Please verify and correct the draft answer, removing any unsupported claims."""

    result = verification_agent.invoke(
        {"messages": [HumanMessage(content=user_content)]}
    )
    messages = result.get("messages", [])
    answer = _extract_last_ai_content(messages)

    return {
        "answer": answer,
    }
