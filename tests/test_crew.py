#!/usr/bin/env python
"""
Simple test script to verify crew functionality
"""
import os
from src.crew import ResumeOptimizerCrew

def test_crew():
    print("Testing ResumeOptimizerCrew initialization...")
    
    # Test inputs - using files that should exist
    inputs = {
        'resume_path': 'input/curriculum.tex',
        'file_path': 'input/curriculum.tex',
        'job_url': 'https://example.com/job',
        'job_description': 'Software Engineer position requiring Python skills',
        'query': 'Extract professional experiences and skills'
    }
    
    try:
        # Create crew instance
        crew_instance = ResumeOptimizerCrew()
        print("✓ Crew instance created successfully")
        
        # Get crew configuration
        crew = crew_instance.crew()
        print("✓ Crew configuration loaded successfully")
        
        print(f"✓ Crew has {len(crew.agents)} agents:")
        for agent in crew.agents:
            print(f"  - {agent.role}")
            
        print(f"✓ Crew has {len(crew.tasks)} tasks:")
        for task in crew.tasks:
            print(f"  - {task.description[:50]}...")
            
        print("\n✓ All basic checks passed!")
        print("The crew is properly configured.")
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_crew()
