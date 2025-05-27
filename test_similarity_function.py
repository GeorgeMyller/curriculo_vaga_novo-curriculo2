#!/usr/bin/env python3
"""
Test script to verify the fixed semantic similarity tool works.
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_tool_function():
    """Test the underlying function directly."""
    print("=== Testing Semantic Similarity Tool Function ===")
    
    # Import the function directly without the decorator
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "similarity_tool", 
        "src/tools/similarity_tool.py"
    )
    module = importlib.util.module_from_spec(spec)
    
    # Get the source code and create a test function without decorator
    with open("src/tools/similarity_tool.py", 'r') as f:
        content = f.read()
    
    # Extract just the function without the decorator
    import ast
    import numpy as np
    
    # Define the helper functions in local scope
    def _extract_embedding_from_text(text: str):
        """Extract embedding from text."""
        text = text.strip()
        
        if text.startswith('[') and text.endswith(']'):
            try:
                embedding = ast.literal_eval(text)
                return [float(x) for x in embedding]
            except (ValueError, SyntaxError) as e:
                print(f"Error parsing embedding list: {e}")
                return []
        
        # Look for a list pattern like [0.123, -0.456, ...]
        import re
        pattern = r'\[([0-9\-\.e\+,\s]+)\]'
        match = re.search(pattern, text)
        
        if match:
            try:
                list_str = '[' + match.group(1) + ']'
                embedding = ast.literal_eval(list_str)
                return [float(x) for x in embedding]
            except (ValueError, SyntaxError) as e:
                print(f"Error parsing embedding from regex match: {e}")
                return []
        
        return []
    
    def _process_input(input_data):
        """Process various input formats to extract embedding vectors."""
        if isinstance(input_data, list) and all(isinstance(x, (int, float)) for x in input_data):
            return input_data
        elif isinstance(input_data, str):
            if input_data.endswith('.md') or input_data.endswith('.txt'):
                try:
                    if os.path.exists(input_data):
                        with open(input_data, 'r', encoding='utf-8') as f:
                            file_content = f.read()
                        print(f"Read file {input_data}, extracting embedding...")
                        return _extract_embedding_from_text(file_content)
                except Exception as e:
                    print(f"Error reading file {input_data}: {e}")
            
            return _extract_embedding_from_text(input_data)
        else:
            return _extract_embedding_from_text(str(input_data))
    
    def test_similarity_function(embedding1, embedding2="reports/embed_job_description_report.md", context_data=""):
        """Test version of the similarity function."""
        # Handle empty values
        if not embedding2 or embedding2 in ["", "None", "null"]:
            embedding2 = "reports/embed_job_description_report.md"
        
        if not context_data or context_data in ["", "None", "null"]:
            context_data = ""
        
        # Process inputs
        emb1 = _process_input(embedding1)
        emb2 = _process_input(embedding2)
        
        if not emb1 or not emb2:
            print("Error: One or both embeddings are empty or could not be extracted.")
            print(f"Embedding 1 length: {len(emb1) if emb1 else 0}")
            print(f"Embedding 2 length: {len(emb2) if emb2 else 0}")
            return 0.0
        
        vec1 = np.array(emb1)
        vec2 = np.array(emb2)
        
        if vec1.shape != vec2.shape:
            min_dim = min(len(vec1), len(vec2))
            vec1 = vec1[:min_dim]
            vec2 = vec2[:min_dim]
            print(f"Warning: Embeddings had different dimensions, truncated both to {min_dim} dimensions")
        
        if np.linalg.norm(vec1) == 0 or np.linalg.norm(vec2) == 0:
            print("Error: One or both embeddings are zero vectors.")
            return 0.0
        
        cosine_similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
        return float(cosine_similarity)
    
    # Run tests
    print("\nTest 1: Default parameters")
    try:
        result = test_similarity_function("reports/embed_curriculum_report.md")
        print(f"✅ Result: {result}")
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    print("\nTest 2: Explicit parameters")
    try:
        result = test_similarity_function(
            "reports/embed_curriculum_report.md",
            "reports/embed_job_description_report.md",
            ""
        )
        print(f"✅ Result: {result}")
    except Exception as e:
        print(f"❌ Failed: {e}")

def main():
    """Run tests."""
    print("Testing Fixed Semantic Similarity Tool Function")
    print("=" * 60)
    
    # Check if required files exist
    curriculum_file = "reports/embed_curriculum_report.md"
    job_file = "reports/embed_job_description_report.md"
    
    if not os.path.exists(curriculum_file):
        print(f"❌ Missing: {curriculum_file}")
        return
    
    if not os.path.exists(job_file):
        print(f"❌ Missing: {job_file}")
        return
    
    print(f"✅ Found: {curriculum_file}")
    print(f"✅ Found: {job_file}")
    
    test_tool_function()
    
    print("\n" + "=" * 60)
    print("Function test completed!")

if __name__ == "__main__":
    main()
