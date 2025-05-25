#!/usr/bin/env python
"""
Test script to debug and fix the job description input issue.
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from crew import ResumeOptimizerCrew

def test_job_description_fix():
    """Test with explicit job description to fix the workflow"""
    
    # Sample job description for testing
    job_description = """Data Analyst Position

Company: Tech Solutions Inc.

JOB DESCRIPTION:
We are seeking a skilled Data Analyst to join our growing team. The ideal candidate will have experience in data analysis, statistical modeling, and business intelligence.

KEY RESPONSIBILITIES:
- Analyze large datasets to identify trends and insights
- Create reports and dashboards for stakeholders
- Collaborate with cross-functional teams
- Develop and maintain data pipelines
- Present findings to management

REQUIRED SKILLS:
- Proficiency in Python, SQL, and Excel
- Experience with data visualization tools (Tableau, Power BI)
- Knowledge of statistical analysis methods
- Strong communication and problem-solving skills
- Bachelor's degree in related field

PREFERRED QUALIFICATIONS:
- Experience with machine learning algorithms
- Knowledge of cloud platforms (AWS, Azure)
- Experience in technology industry"""

    # Resume file path
    resume_path = "input/curriculum.tex"
    
    # Check if resume file exists
    if not os.path.exists(resume_path):
        print(f"Error: Resume file not found at {resume_path}")
        return False
    
    print("=== Testing CrewAI with Job Description Fix ===")
    print(f"Resume: {resume_path}")
    print(f"Job Description Length: {len(job_description)} characters")
    
    # Inputs for the crew
    inputs = {
        'resume_path': resume_path,
        'file_path': resume_path,
        'job_description': job_description,
        'job_url': 'https://example.com/job',  # Placeholder URL
        'query': "Extract professional experiences, skills, and academic background from the curriculum"
    }
    
    try:
        # Create and run the crew
        crew = ResumeOptimizerCrew()
        result = crew.crew().kickoff(inputs=inputs)
        
        print("\n=== Execution Completed ===")
        print("Result type:", type(result))
        print("Result:", str(result)[:500] + "..." if len(str(result)) > 500 else str(result))
        
        # Check output files
        output_files = [
            'extract_curriculum_data_report.md',
            'analyze_job_description_report.md', 
            'embed_curriculum_report.md',
            'embed_job_description_report.md',
            'similarity_analysis_report.md',
            'adjust_resume_for_job_report.md',
            'execution_report.md'
        ]
        
        print("\n=== Output Files Status ===")
        for file in output_files:
            if os.path.exists(file):
                size = os.path.getsize(file)
                print(f"✓ {file} ({size} bytes)")
            else:
                print(f"✗ {file} (missing)")
        
        return True
        
    except Exception as e:
        print(f"Error during crew execution: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_job_description_fix()
    if success:
        print("\n✓ Test completed successfully")
    else:
        print("\n✗ Test failed")
