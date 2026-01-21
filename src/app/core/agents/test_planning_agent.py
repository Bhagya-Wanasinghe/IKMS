"""
Test the planning agent independently
Run this to make sure it works before integrating into graph
"""

import os
from dotenv import load_dotenv
from src.app.core.agents.agents import planning_agent_node

# Load environment
load_dotenv()

def test_planning():
    """Test the planning agent with sample questions"""
    
    test_questions = [
        "What is HNSW indexing?",
        "What are the advantages of vector databases compared to traditional databases, and how do they handle scalability?",
        "How do embeddings work in machine learning?"
    ]
    
    print("Testing Planning Agent")
    print("="*70)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n📝 Test {i}/{len(test_questions)}")
        print(f"Question: {question}")
        print("-"*70)
        
        # Create minimal state
        state = {
            "question": question,
            "context": None,
            "answer": None,
            "plan": None,
            "sub_questions": None
        }
        
        # Run planning node
        result = planning_agent_node(state)
        
        print(f"✓ Planning complete!")
        print(f"Plan: {result['plan'][:200]}...")
        print(f"Sub-questions ({len(result['sub_questions'])}): {result['sub_questions']}")
        print("="*70)
        
        input("Press Enter for next test...")

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment")
        print("Make sure .env file has your OpenAI API key")
        exit(1)
    
    test_planning()
    print("\n✓ All tests complete!")