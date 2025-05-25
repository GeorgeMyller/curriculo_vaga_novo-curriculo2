#!/usr/bin/env python3
"""
Final test to simulate exactly what Streamlit does
"""

import os
import tempfile
import shutil
from src.streamlit_runner import run_with_streamlit_inputs

def test_streamlit_final():
    """Final test mimicking Streamlit behavior exactly"""
    print("=== FINAL STREAMLIT TEST ===")
    
    # Job description text (same as working debug)
    job_text = """Data Analyst Position

We are looking for a skilled Data Analyst to join our team.

Requirements:
- Bachelor's degree in a relevant field
- Experience with Python, SQL, and data visualization tools
- Strong analytical and communication skills
- Experience with statistical analysis and machine learning
"""
    
    # Simulate Streamlit file upload
    original_resume_path = "input/curriculum.tex"
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Original file: {original_resume_path}")
    print(f"Output dir: {output_dir}")
    print(f"Job text: {len(job_text)} chars")
    
    # Create temporary directory (like Streamlit does)
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Temp directory: {temp_dir}")
        
        # Copy uploaded file to temp directory
        resume_filename = "curriculum.tex"
        temp_resume_path = os.path.join(temp_dir, resume_filename)
        
        # Read original file and write to temp (simulating upload)
        with open(original_resume_path, 'rb') as source:
            file_content = source.read()
        
        with open(temp_resume_path, 'wb') as target:
            target.write(file_content)
        
        print(f"File copied to temp: {temp_resume_path}")
        print(f"File exists in temp: {os.path.exists(temp_resume_path)}")
        
        try:
            print("\n🚀 Calling run_with_streamlit_inputs...")
            
            # Call exactly like Streamlit does
            result, output_file_path = run_with_streamlit_inputs(
                resume_file_path=temp_resume_path,
                job_url=None,
                job_text=job_text,
                output_dir=output_dir
            )
            
            print("✅ SUCCESS!")
            print(f"Result length: {len(result)} chars")
            print(f"Output file: {output_file_path}")
            
            return True
            
        except Exception as e:
            print(f"❌ FAILED: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    test_streamlit_final()
