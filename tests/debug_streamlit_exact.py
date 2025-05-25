#!/usr/bin/env python3
"""
Debug script to test exactly what Streamlit does including file upload simulation
"""

import os
import tempfile
import shutil
from src.streamlit_runner import run_with_streamlit_inputs

def test_streamlit_exact_simulation():
    """Test exactly like Streamlit: temporary directory, file copy, etc."""
    
    # Job text like in Streamlit
    job_text = """Data Analyst Position

We are looking for a skilled Data Analyst to join our team.

Requirements:
- Bachelor's degree in a relevant field
- Experience with Python, SQL, and data visualization tools
- Strong analytical and communication skills
- Experience with statistical analysis and machine learning
"""
    
    # Original resume file
    original_resume_path = "input/curriculum.tex"
    
    # Output directory (like Streamlit)
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    print("=== Testing EXACT Streamlit simulation ===")
    print(f"Original resume: {original_resume_path}")
    print(f"Job text length: {len(job_text)} chars")
    print(f"Output dir: {output_dir}")
    
    # Simulate Streamlit's file upload behavior
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Temporary directory: {temp_dir}")
        
        # Simulate uploaded file (copy to temp directory like Streamlit does)
        resume_filename = "curriculum.tex"
        temp_resume_path = os.path.join(temp_dir, resume_filename)
        
        # Copy the file to temp location (simulating Streamlit upload)
        shutil.copy2(original_resume_path, temp_resume_path)
        print(f"Copied resume to: {temp_resume_path}")
        
        # Verify file exists
        if not os.path.exists(temp_resume_path):
            print(f"❌ ERROR: File does not exist at {temp_resume_path}")
            return
            
        print("-" * 60)
        
        try:
            # Call exactly like Streamlit does
            print("Calling run_with_streamlit_inputs...")
            result, output_path = run_with_streamlit_inputs(
                resume_file_path=temp_resume_path,  # Temp path like Streamlit
                job_url=None,                       # URL is None when using text
                job_text=job_text,                 # Job text provided
                output_dir=output_dir              # Output directory
            )
            
            print("✅ SUCCESS! Exact Streamlit simulation worked.")
            print(f"Output file: {output_path}")
            print(f"Result length: {len(result)} chars")
            print(f"Output file exists: {os.path.exists(output_path)}")
            
        except Exception as e:
            print(f"❌ ERROR in exact simulation: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_streamlit_exact_simulation()
