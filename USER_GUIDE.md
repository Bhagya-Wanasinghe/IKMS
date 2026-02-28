# User Guide: IKMS Query Planning Feature

## Getting Started

### What is Query Planning?

Query Planning is an intelligent feature that analyzes your question before searching for information. It:

1. **Understands** what you're really asking
2. **Breaks down** complex questions into simpler parts
3. **Plans** the best way to search for answers
4. **Retrieves** more relevant information

### When to Use Query Planning

 **Best for:**
- Complex, multi-part questions
- Comparisons ("X vs Y")
- Questions with multiple aspects
- Unclear or ambiguous questions

 **Not needed for:**
- Simple definitions
- Single-concept questions
- Direct factual queries

## Using the Interface

### Step 1: Enter Your Question

Type your question in the text box. Examples:

**Simple:**
```
What is HNSW indexing?
```

**Complex:**
```
What are the advantages of vector databases compared to 
traditional databases, and how do they handle scalability?
```

**Medium:**
```
How do embeddings work in semantic search?
```

### Step 2: Enable/Disable Planning

Use the toggle switch to turn planning on or off:

- **ON** (recommended): See the planning process
- **OFF**: Direct retrieval without planning

### Step 3: Ask Question

Click the "Ask Question" button or press `Ctrl + Enter`.

### Step 4: View Results

The system shows you:

1. **Search Strategy** - How it plans to find information
2. **Sub-Questions** - What it will search for
3. **Final Answer** - The complete answer
4. **Statistics** - Performance metrics

## Understanding the Output

### Search Strategy

The plan explains how the system will search:

```
PLAN: This question has two distinct parts: 
(1) advantages and comparisons, 
(2) scalability mechanisms...
```

### Sub-Questions

These are the focused searches the system will make:

```
1. vector database advantages benefits
2. vector database vs relational database comparison
3. vector database scalability architecture
```

### Final Answer

The complete answer synthesized from all retrieved information.

### Statistics

- **Sub-Questions**: How many focused searches were made
- **Context Characters**: Amount of information retrieved
- **Response Time**: How long it took to answer

## Tips for Best Results

### 1. Be Specific

 Bad: "Tell me about databases"
 Good: "What are the key differences between SQL and NoSQL databases?"

### 2. Ask Multi-Part Questions

The planning feature shines with complex questions:

 "What is HNSW indexing, how does it work, and what are its performance characteristics?"

### 3. Use Comparisons

 "Compare and contrast vector databases with traditional relational databases"

### 4. Try Different Phrasings

If you don't get good results, rephrase your question:
- "Advantages of X" → "Why use X over Y"
- "How does X work" → "Explain the mechanism of X"

## Troubleshooting

### No Results

**Problem**: No answer generated
**Solution**: 
- Make sure documents are indexed
- Try a simpler question
- Check if backend is running

### Slow Response

**Problem**: Taking too long
**Solution**:
- Normal for complex questions (10-20 seconds)
- Planning adds 1-2 seconds
- Check your internet connection

### Planning Not Showing

**Problem**: Don't see search strategy
**Solution**:
- Make sure planning toggle is ON
- Try a more complex question
- Check browser console for errors

## Example Usage Scenarios

### Scenario 1: Research Question

**Question**: "What are the trade-offs between HNSW and IVF indexing methods?"

**What Happens**:
1. System identifies this as a comparison question
2. Creates sub-questions for each method
3. Searches for advantages and disadvantages of each
4. Synthesizes a comprehensive comparison

### Scenario 2: Definition with Context

**Question**: "What is approximate nearest neighbor search and why is it important?"

**What Happens**:
1. System breaks into definition + importance
2. Searches for concept explanation
3. Searches for use cases and benefits
4. Combines into complete answer

### Scenario 3: How-To Question

**Question**: "How do vector databases handle concurrent writes and reads?"

**What Happens**:
1. System identifies two distinct operations
2. Searches for write mechanisms
3. Searches for read mechanisms
4. Explains both with proper context

## Keyboard Shortcuts

- `Ctrl + Enter` - Submit question
- `Tab` - Navigate between fields

## Privacy & Data

- Questions are processed through OpenAI API
- No data is stored permanently
- Sessions are temporary

## Support

If you encounter issues:
1. Check the browser console (F12)
2. Verify backend is running
3. Check API keys are configured
4. Contact system administrator

## Advanced Features

### Toggle Planning

Compare results with and without planning:
1. Ask question with planning ON
2. Note the answer
3. Toggle planning OFF
4. Ask same question
5. Compare quality and relevance

### Reading the Plan

The plan shows the system's "thinking":
- What it understood from your question
- What aspects it will cover
- How it will structure its search

This transparency helps you:
- Verify it understood correctly
- Refine your question if needed
- Learn better questioning techniques

## Best Practices

1. **Start Simple**: Test with basic questions first
2. **Experiment**: Try same question with/without planning
3. **Read the Plan**: Learn from how the system breaks down questions
4. **Refine**: Use sub-questions to improve your next query
5. **Be Patient**: Complex questions take time to process

## Frequently Asked Questions

**Q: Why does planning make it slower?**
A: Planning adds 1-2 seconds but often results in better, more complete answers.

**Q: Can I see what was retrieved?**
A: Yes, the context section shows what information was used.

**Q: What if I don't want planning?**
A: Simply toggle it off. The system works fine without it.

**Q: How many sub-questions are created?**
A: Typically 1-5, depending on question complexity.

**Q: Does planning work in other languages?**
A: Currently optimized for English.

## Conclusion

The Query Planning feature makes the IKMS system more intelligent and capable of handling complex questions. Experiment with it to get the best results!

For technical documentation, see [README.md](README.md).
