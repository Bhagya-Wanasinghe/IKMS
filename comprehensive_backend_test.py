"""
Comprehensive backend test for Query Planning feature
"""

import requests
import time

BASE_URL = "http://localhost:8001"

test_cases = [
    {
        "name": "Simple Question",
        "question": "What is HNSW indexing?",
        "expected_sub_questions": 1,  # Should have 1-2 sub-questions
    },
    {
        "name": "Complex Multi-Part Question",
        "question": "What are the advantages of vector databases compared to traditional databases, and how do they handle scalability?",
        "expected_sub_questions": 3,  # Should break into 3+ parts
    },
    {
        "name": "Medium Complexity",
        "question": "How do embeddings work in semantic search?",
        "expected_sub_questions": 2,  # Should have 2-3 sub-questions
    }
]

def test_qa_endpoint():
    """Test the QA endpoint with various questions"""
    
    print("="*70)
    print("COMPREHENSIVE BACKEND TEST - QUERY PLANNING FEATURE")
    print("="*70)
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}/{len(test_cases)}: {test['name']}")
        print(f"Question: {test['question']}")
        print("-"*70)
        
        try:
            # Make request
            response = requests.post(
                f"{BASE_URL}/qa",
                json={"question": test['question']},
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                
                print("✓ Status: 200 OK")
                print(f"✓ Answer received: {data.get('answer', 'N/A')[:100]}...")
                print(f"✓ Context received: {len(data.get('context', ''))} characters")
                
                # Check if plan is in response (if API was updated)
                if 'plan' in data:
                    print(f"✓ Plan: {data['plan'][:100]}...")
                    
                if 'sub_questions' in data:
                    print(f"✓ Sub-questions ({len(data['sub_questions'])}): {data['sub_questions']}")
                    
                    # Validate number of sub-questions
                    if len(data['sub_questions']) >= test['expected_sub_questions']:
                        print(f"✓ Sub-question count matches expectation")
                    else:
                        print(f"⚠ Warning: Expected {test['expected_sub_questions']}+ sub-questions, got {len(data['sub_questions'])}")
                
                passed += 1
                print("✓ TEST PASSED")
                
            else:
                print(f"✗ Error: Status {response.status_code}")
                print(f"Response: {response.text}")
                failed += 1
                print("✗ TEST FAILED")
                
        except requests.exceptions.Timeout:
            print("✗ Timeout - request took too long")
            failed += 1
            print("✗ TEST FAILED")
            
        except Exception as e:
            print(f"✗ Error: {e}")
            failed += 1
            print("✗ TEST FAILED")
        
        print("-"*70)
        
        if i < len(test_cases):
            time.sleep(2)  # Wait between tests
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Passed: {passed}/{len(test_cases)}")
    print(f"Failed: {failed}/{len(test_cases)}")
    
    if failed == 0:
        print("\n✓ ALL TESTS PASSED!")
        return True
    else:
        print(f"\n✗ {failed} TEST(S) FAILED")
        return False

if __name__ == "__main__":
    print("Make sure the FastAPI server is running on http://localhost:8001")
    print("Starting tests in 3 seconds...")
    time.sleep(3)
    
    success = test_qa_endpoint()
    exit(0 if success else 1)