#!/usr/bin/env python3
"""
Test crew execution with exact Streamlit parameters
"""

import os
import tempfile
import shutil
from src.crew import create_crew

def test_crew_execution():
    """Test crew execution with Streamlit-like parameters"""
    print("=== Testing crew execution ===")
    
    # Job text like in Streamlit
    job_text = """Data Analyst Position

We are looking for a skilled Data Analyst to join our team.

Requirements:
- Bachelor's degree in a relevant field
- Experience with Python, SQL, and data visualization tools
- Strong analytical and communication skills
- Experience with statistical analysis and machine learning
"""
    
    # Prepare files like Streamlit does
    original_resume_path = "input/curriculum.tex"
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Copy file to temp like Streamlit upload
        temp_resume_path = os.path.join(temp_dir, "curriculum.tex")
        shutil.copy2(original_resume_path, temp_resume_path)
        
        # Prepare inputs exactly like streamlit_runner.py does
        inputs = {
            'resume_path': temp_resume_path,  # .tex file path
            'file_path': None,                # No PDF path
            'job_url': None,                  # No URL
            'job_text': job_text,             # Text provided
            'job_description': job_text,      # This is what tasks.yaml expects
            'output_dir': output_dir
        }
        
        print("Inputs prepared:")
        for key, value in inputs.items():
            if value and len(str(value)) > 100:
                print(f"  {key}: {type(value)} = {str(value)[:100]}...")
            else:
                print(f"  {key}: {type(value)} = {value}")
        
        print("\nCreating crew...")
        try:
            crew = create_crew()
            print("✅ Crew created")
        except Exception as e:
            print(f"❌ Crew creation failed: {e}")
            return
        
        print("\nExecuting crew.kickoff()...")
        try:
            result = crew.kickoff(inputs=inputs)
            print(f"✅ Crew execution successful!")
            print(f"Result type: {type(result)}")
            print(f"Result length: {len(str(result))} chars")
            return result
        except Exception as e:
            print(f"❌ Crew execution failed: {e}")
            import traceback
            traceback.print_exc()
            return None

if __name__ == "__main__":
    test_crew_execution()
