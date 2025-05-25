#!/usr/bin/env python3
"""
Debug script to test what the Streamlit app is passing to the crew
"""

import os
from src.streamlit_runner import run_with_streamlit_inputs

def test_streamlit_inputs():
    """Test the Streamlit runner with the same inputs that Streamlit would pass"""
    
    # Test with job text (like the working test)
    job_text = """Data Analyst Position

We are looking for a skilled Data Analyst to join our team.

Requirements:
- Bachelor's degree in a relevant field
- Experience with Python, SQL, and data visualization tools
- Strong analytical and communication skills
- Experience with statistical analysis and machine learning
"""
    
    resume_path = "input/curriculum.tex"
    output_dir = "output"
    
    print("Testing Streamlit runner with job text...")
    print(f"Resume path: {resume_path}")
    print(f"Job text length: {len(job_text)} chars")
    print(f"Output dir: {output_dir}")
    print("-" * 50)
    
    try:
        result, output_path = run_with_streamlit_inputs(
            resume_file_path=resume_path,
            job_url=None,  # This is what Streamlit passes when using text input
            job_text=job_text,
            output_dir=output_dir
        )
        print("✅ SUCCESS! Streamlit runner worked.")
        print(f"Output file: {output_path}")
        print(f"Result length: {len(result)} chars")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_streamlit_inputs()
