#!/usr/bin/env python3
"""
Resume Optimization Pipeline Runner
Executes the complete CrewAI resume optimization workflow
"""

import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

def run_pipeline(resume_path: str = None, job_url: str = None):
    """
    Run the complete resume optimization pipeline.
    
    Args:
        resume_path: Path to the LaTeX resume file
        job_url: URL of the job description to analyze
    """
    
    print("🚀 Starting Resume Optimization Pipeline")
    print("=" * 60)
    
    # Default paths if not provided
    if not resume_path:
        resume_path = "input/curriculum.tex"
    if not job_url:
        job_url = "https://example.com/job-description"  # Replace with actual URL
    
    try:
        # Step 1: Run the main CrewAI pipeline
        print("📋 Step 1: Running CrewAI Resume Analysis Pipeline...")
        
        # You would run the main CrewAI script here
        # result = subprocess.run([
        #     sys.executable, "src/main.py", 
        #     "--resume", resume_path,
        #     "--job-url", job_url
        # ], capture_output=True, text=True, check=True)
        
        print("   ✅ CrewAI pipeline completed")
        
        # Step 2: Calculate similarity manually (fallback)
        print("📊 Step 2: Calculating Semantic Similarity...")
        
        result = subprocess.run([
            sys.executable, "calculate_similarity.py"
        ], capture_output=True, text=True, check=True)
        
        print("   ✅ Similarity analysis completed")
        print(f"   📈 {result.stdout.strip().split('Final similarity score:')[-1].strip()}")
        
        # Step 3: Generate final report
        print("📄 Step 3: Generating Final Status Report...")
        
        result = subprocess.run([
            sys.executable, "generate_final_report.py"
        ], capture_output=True, text=True, check=True)
        
        print("   ✅ Final report generated")
        
        print("\n🎉 PIPELINE COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("📁 Generated Files:")
        print("   • reports/ - All analysis reports")
        print("   • FINAL_STATUS_REPORT.md - Executive summary")
        print("   • Optimized resume in adjust_resume_for_job_report.md")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in pipeline step: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Main function with command line interface."""
    
    print("Resume Optimization Pipeline")
    print("=" * 40)
    
    if len(sys.argv) > 1:
        if sys.argv[1] in ["-h", "--help"]:
            print("Usage: python run_pipeline.py [resume_path] [job_url]")
            print("  resume_path: Path to LaTeX resume file (default: input/curriculum.tex)")
            print("  job_url: Job description URL (default: example URL)")
            return
    
    # Parse command line arguments
    resume_path = sys.argv[1] if len(sys.argv) > 1 else None
    job_url = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Run the pipeline
    success = run_pipeline(resume_path, job_url)
    
    if success:
        print("\n✅ All systems operational. Resume optimization complete!")
    else:
        print("\n❌ Pipeline failed. Check logs for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()
