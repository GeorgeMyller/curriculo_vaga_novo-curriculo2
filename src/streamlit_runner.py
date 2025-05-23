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
    
    # Prepare inputs for the crew
    inputs = {
        'resume_path': resume_file_path if resume_file_path.endswith('.tex') else None,
        'file_path': resume_file_path if resume_file_path.endswith('.pdf') else None,
        'job_url': job_url,
        'job_text': job_text,
        'output_dir': output_dir
    }
    
    # Get the configured crew and run it
    crew = create_crew()
    result = crew.kickoff(inputs=inputs)
    
    # Create output file path with timestamp
    file_name = Path(resume_file_path).stem
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file_path = os.path.join(output_dir, f"optimized_{file_name}_{timestamp}.tex")
    
    # Save result to file
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(str(result))
    
    return str(result), output_file_path
