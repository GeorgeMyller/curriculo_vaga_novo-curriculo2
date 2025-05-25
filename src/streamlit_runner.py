"""
Module for integrating the CrewAI resume optimizer with Streamlit.
Provides functions to run the CrewAI system with dynamic inputs from the web UI.
"""

import os
import tempfile
from pathlib import Path
from datetime import datetime
from .crew import create_crew


def run_with_streamlit_inputs(resume_file_path, job_url=None, job_text=None, output_dir=None):
    """
    Run the CrewAI resume optimizer with inputs from Streamlit.
    
    Args:
        resume_file_path (str): Path to the uploaded resume file (.tex or .pdf)
        job_url (str, optional): URL of the job description
        job_text (str, optional): Plain text of the job description 
                                 (alternative to job_url)
        output_dir (str, optional): Directory to save output files. 
                                   If None, a temp directory is used.
    
    Returns:
        tuple: (result_text, output_file_path) - The optimized resume text and its path
    """
    # Create output directory if specified
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    else:
        output_dir = tempfile.mkdtemp()
    
    # Ensure reports directory exists (for CrewAI task outputs)
    reports_dir = Path('./reports').absolute()
    os.makedirs(reports_dir, exist_ok=True)
    
    # Prepare inputs for the crew - match the YAML task expectations
    job_description = job_text if job_text and job_text.strip() else job_url
    
    # The YAML tasks expect these specific input keys
    inputs = {
        'resume_path': resume_file_path,  # Expected by extract_curriculum_data
        'file_path': resume_file_path,    # Also expected by extract_curriculum_data
        'job_description': job_description,  # Expected by analyze_job_description
        'job_url': job_url if job_url else "",  # Optional
        'job_text': job_text if job_text else "",  # Optional
        'query': "Extract professional experiences, skills, and academic background from the curriculum"  # Expected by some tasks
    }
    
    # Get the configured crew and run it
    crew = create_crew()
    result = crew.kickoff(inputs=inputs)
    
    # The result should be the output from the last task (generate_report)
    # But we want the optimized resume, which is from adjust_resume_for_job
    
    # Check if the optimized resume file was created
    resume_output_files = [
        os.path.join(output_dir, "novo_curriculo.tex"),
        os.path.join(os.getcwd(), "novo_curriculo.tex")
    ]
    
    optimized_resume_content = None
    output_file_path = None
    
    for file_path in resume_output_files:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                optimized_resume_content = f.read()
            output_file_path = file_path
            break
    
    # If no optimized resume file found, use the result as content
    if optimized_resume_content is None:
        optimized_resume_content = str(result)
        # Create output file path with timestamp
        file_name = Path(resume_file_path).stem
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file_path = os.path.join(output_dir, f"optimized_{file_name}_{timestamp}.tex")
        
        # Save result to file
        with open(output_file_path, "w", encoding="utf-8") as f:
            f.write(optimized_resume_content)
    
    return optimized_resume_content, output_file_path
