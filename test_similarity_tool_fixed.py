#!/usr/bin/env python3
"""
Test script to verify the fixed semantic similarity tool works with CrewAI.
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from tools.similarity_tool import calculate_semantic_similarity

def test_tool_direct():
    """Test the tool directly with various input scenarios."""
    print("=== Testing Semantic Similarity Tool (Direct) ===")
    
    # Test 1: Default parameters (should use curriculum vs job description)
    print("\nTest 1: Default parameters")
    try:
        result = calculate_semantic_similarity("reports/embed_curriculum_report.md")
        print(f"✅ Default parameters: {result}")
    except Exception as e:
        print(f"❌ Default parameters failed: {e}")
    
    # Test 2: Explicit file paths
    print("\nTest 2: Explicit file paths")
    try:
        result = calculate_semantic_similarity(
            "reports/embed_curriculum_report.md",
            "reports/embed_job_description_report.md"
        )
        print(f"✅ Explicit files: {result}")
    except Exception as e:
        print(f"❌ Explicit files failed: {e}")
    
    # Test 3: With context data
    print("\nTest 3: With context data")
    try:
        result = calculate_semantic_similarity(
            "reports/embed_curriculum_report.md",
            "reports/embed_job_description_report.md",
            "test context"
        )
        print(f"✅ With context: {result}")
    except Exception as e:
        print(f"❌ With context failed: {e}")
    
    # Test 4: Empty string parameters (should use defaults)
    print("\nTest 4: Empty string parameters")
    try:
        result = calculate_semantic_similarity(
            "reports/embed_curriculum_report.md",
            "",
            ""
        )
        print(f"✅ Empty strings: {result}")
    except Exception as e:
        print(f"❌ Empty strings failed: {e}")

def test_tool_crewai_style():
    """Test the tool as CrewAI would call it."""
    print("\n=== Testing Tool (CrewAI Style) ===")
    
    # Import the tool as CrewAI would
    from crewai.tools import tool
    
    # Test the tool with the exact signature CrewAI expects
    print("\nTesting CrewAI-style call...")
    try:
        # This simulates how CrewAI calls the tool based on the task configuration
        result = calculate_semantic_similarity(
            embedding1="reports/embed_curriculum_report.md reports/embed_job_description_report.md",
            embedding2="reports/embed_job_description_report.md",
            context_data=""
        )
        print(f"✅ CrewAI-style call: {result}")
    except Exception as e:
        print(f"❌ CrewAI-style call failed: {e}")

def main():
    """Run all tests."""
    print("Testing Fixed Semantic Similarity Tool")
    print("=" * 50)
    
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
    
    # Run tests
    test_tool_direct()
    test_tool_crewai_style()
    
    print("\n" + "=" * 50)
    print("Test completed! If all tests pass, the tool should work with CrewAI.")

if __name__ == "__main__":
    main()
