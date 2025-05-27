#!/usr/bin/env python3
"""
Test script to debug the embedding extraction function.
"""

import ast
import re

def test_extract_embedding_from_text():
    """Test the embedding extraction function."""
    
    # Read the actual file content
    with open("reports/embed_curriculum_report.md", 'r') as f:
        content = f.read()
    
    print("=== Testing Embedding Extraction ===")
    print(f"Content length: {len(content)}")
    print(f"Starts with '[': {content.startswith('[')}")
    print(f"Ends with ']': {content.endswith(']')}")
    print(f"First 100 chars: {content[:100]}")
    print(f"Last 100 chars: {content[-100:]}")
    
    # Test the truncated case handling
    text = content.strip()
    
    if text.startswith('[') and not text.endswith(']'):
        print("\n=== Handling truncated embedding ===")
        # Find the last comma and complete number
        last_comma = text.rfind(',')
        print(f"Last comma position: {last_comma}")
        
        if last_comma > 0:
            # Try to find the end of the last complete number
            truncated_text = text[:last_comma] + ']'
            print(f"Truncated text ends with: {truncated_text[-20:]}")
            
            try:
                embedding = ast.literal_eval(truncated_text)
                print(f"✅ Successfully parsed {len(embedding)} values")
                print(f"First 5 values: {embedding[:5]}")
                print(f"Last 5 values: {embedding[-5:]}")
                return embedding
            except (ValueError, SyntaxError) as e:
                print(f"❌ Error parsing truncated embedding: {e}")
    
    return []

def main():
    """Run the test."""
    embedding = test_extract_embedding_from_text()
    if embedding:
        print(f"\n✅ Successfully extracted embedding with {len(embedding)} dimensions")
    else:
        print("\n❌ Failed to extract embedding")

if __name__ == "__main__":
    main()
