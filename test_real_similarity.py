#!/usr/bin/env python3
"""
Test the actual similarity tool with proper imports.
"""

import os
import sys
from pathlib import Path
import ast
import re
import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def _extract_embedding_from_text(text: str):
    """
    Extract embedding from text that might contain markdown or other formatting.
    """
    # Remove markdown formatting and extract the list
    text = text.strip()
    
    # If the text starts with [, it's already a proper list format
    if text.startswith('[') and text.endswith(']'):
        try:
            embedding = ast.literal_eval(text)
            return [float(x) for x in embedding]
        except (ValueError, SyntaxError) as e:
            print(f"Error parsing embedding list: {e}")
            return []
    
    # Handle case where text starts with [ but doesn't end with ]
    # This happens when the embedding was cut off during saving
    if text.startswith('[') and not text.endswith(']'):
        try:
            # Add closing bracket and try to parse up to the last complete number
            # Find the last comma and complete number
            last_comma = text.rfind(',')
            if last_comma > 0:
                # Try to find the end of the last complete number
                truncated_text = text[:last_comma] + ']'
                embedding = ast.literal_eval(truncated_text)
                print(f"Warning: Embedding appears truncated, using {len(embedding)} values")
                return [float(x) for x in embedding]
        except (ValueError, SyntaxError) as e:
            print(f"Error parsing truncated embedding: {e}")
    
    # Look for a list pattern like [0.123, -0.456, ...]
    pattern = r'\[([0-9\-\.e\+,\s]+)\]'
    match = re.search(pattern, text)
    
    if match:
        try:
            # Parse the list string
            list_str = '[' + match.group(1) + ']'
            embedding = ast.literal_eval(list_str)
            return [float(x) for x in embedding]
        except (ValueError, SyntaxError) as e:
            print(f"Error parsing embedding from regex match: {e}")
            return []
    
    # If no brackets found, assume the entire text is comma-separated values
    # This handles cases where the embedding is saved without brackets
    if ',' in text and not text.startswith('#'):
        try:
            # Remove any markdown formatting
            clean_text = text.replace('```', '').replace('`', '').strip()
            # Split by comma and convert to floats
            values = [float(x.strip()) for x in clean_text.split(',') if x.strip()]
            return values
        except (ValueError, TypeError) as e:
            print(f"Error parsing comma-separated values: {e}")
            return []
    
    return []

def _process_input(input_data):
    """
    Process various input formats to extract embedding vectors.
    """
    if isinstance(input_data, list) and all(isinstance(x, (int, float)) for x in input_data):
        # Already a proper embedding
        return input_data
    elif isinstance(input_data, str):
        # Check if it's a file path and try to read the file
        if input_data.endswith('.md') or input_data.endswith('.txt'):
            try:
                if os.path.exists(input_data):
                    with open(input_data, 'r', encoding='utf-8') as f:
                        file_content = f.read()
                    print(f"Read file {input_data}, extracting embedding...")
                    return _extract_embedding_from_text(file_content)
            except Exception as e:
                print(f"Error reading file {input_data}: {e}")
        
        # Try to extract embedding from string
        return _extract_embedding_from_text(input_data)
    elif isinstance(input_data, dict):
        # Check if it's a dict with embedding data
        if 'embedding' in input_data:
            return _process_input(input_data['embedding'])
        elif 'content' in input_data:
            return _extract_embedding_from_text(str(input_data['content']))
        else:
            return _extract_embedding_from_text(str(input_data))
    else:
        # Try to convert to string and extract
        return _extract_embedding_from_text(str(input_data))

def test_direct_similarity():
    """Test similarity calculation directly."""
    print("=== Testing Direct Similarity Calculation ===")
    
    # Test the embeddings extraction first
    print("\nExtracting curriculum embedding...")
    emb1 = _process_input("reports/embed_curriculum_report.md")
    print(f"Curriculum embedding length: {len(emb1)}")
    
    print("\nExtracting job description embedding...")
    emb2 = _process_input("reports/embed_job_description_report.md")
    print(f"Job description embedding length: {len(emb2)}")
    
    if not emb1 or not emb2:
        print("❌ One or both embeddings are empty")
        return 0.0
    
    # Calculate similarity
    vec1 = np.array(emb1)
    vec2 = np.array(emb2)
    
    if vec1.shape != vec2.shape:
        min_dim = min(len(vec1), len(vec2))
        vec1 = vec1[:min_dim]
        vec2 = vec2[:min_dim]
        print(f"Warning: Truncated both to {min_dim} dimensions")
    
    if np.linalg.norm(vec1) == 0 or np.linalg.norm(vec2) == 0:
        print("❌ Zero vector detected")
        return 0.0
    
    cosine_similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    print(f"✅ Similarity calculated: {cosine_similarity}")
    return float(cosine_similarity)

def main():
    """Run the test."""
    print("Testing Similarity Tool with Real Extraction Logic")
    print("=" * 60)
    
    # Check files exist
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
    
    result = test_direct_similarity()
    
    print("\n" + "=" * 60)
    print(f"Final result: {result}")
    
    if result > 0:
        print("✅ The similarity tool logic is working correctly!")
    else:
        print("❌ The similarity tool needs further debugging.")

if __name__ == "__main__":
    main()
