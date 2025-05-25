#!/usr/bin/env python3
"""
Simple debug to find where the issue is
"""

import os
import tempfile
import shutil

def test_streamlit_import():
    """Test if imports work"""
    print("=== Testing imports ===")
    try:
        from src.streamlit_runner import run_with_streamlit_inputs
        print("✅ Import successful")
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False
    return True

def test_file_access():
    """Test if file access works"""
    print("=== Testing file access ===")
    
    original_resume_path = "input/curriculum.tex"
    
    # Check if file exists
    if not os.path.exists(original_resume_path):
        print(f"❌ Original file does not exist: {original_resume_path}")
        return False
    
    print(f"✅ Original file exists: {original_resume_path}")
    
    # Test temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"✅ Temp directory created: {temp_dir}")
        
        temp_resume_path = os.path.join(temp_dir, "curriculum.tex")
        shutil.copy2(original_resume_path, temp_resume_path)
        
        if os.path.exists(temp_resume_path):
            print(f"✅ File copied to temp: {temp_resume_path}")
            return True
        else:
            print(f"❌ Failed to copy file to temp")
            return False

def test_crew_creation():
    """Test if crew can be created"""
    print("=== Testing crew creation ===")
    try:
        from src.crew import create_crew
        crew = create_crew()
        print("✅ Crew created successfully")
        return True
    except Exception as e:
        print(f"❌ Crew creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🔍 Debugging Streamlit issues step by step...")
    print("=" * 60)
    
    # Test 1: Imports
    if not test_streamlit_import():
        return
    
    # Test 2: File access
    if not test_file_access():
        return
        
    # Test 3: Crew creation
    if not test_crew_creation():
        return
    
    print("\n✅ All basic tests passed!")
    print("The issue might be in the crew execution itself.")

if __name__ == "__main__":
    main()
