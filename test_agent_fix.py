#!/usr/bin/env python3
"""
Test script to validate the agent configuration fixes
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.crew import ResumeOptimizerCrew

def test_agent_configuration():
    """Test if agents are properly configured with tools"""
    try:
        # Initialize the crew
        crew_instance = ResumeOptimizerCrew()
        
        # Test job_analyzer agent
        job_analyzer = crew_instance.job_analyzer()
        print(f"✅ job_analyzer agent created successfully")
        print(f"   Tools: {[tool.name if hasattr(tool, 'name') else str(tool) for tool in job_analyzer.tools]}")
        
        # Test if File Writer Tool is available
        file_write_tools = [tool for tool in job_analyzer.tools if hasattr(tool, 'name') and 'write' in tool.name.lower()]
        if file_write_tools:
            print(f"✅ File Writer Tool found in job_analyzer")
        else:
            print(f"❌ File Writer Tool NOT found in job_analyzer")
        
        # Test other agents
        curriculum_reader = crew_instance.curriculum_reader()
        print(f"✅ curriculum_reader agent created successfully")
        print(f"   Tools: {[tool.name if hasattr(tool, 'name') else str(tool) for tool in curriculum_reader.tools]}")
        
        alignment_analyzer = crew_instance.alignment_analyzer()
        print(f"✅ alignment_analyzer agent created successfully")
        print(f"   Tools: {[tool.name if hasattr(tool, 'name') else str(tool) for tool in alignment_analyzer.tools]}")
        
        print("\n🎉 All agents configured successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error configuring agents: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Testing agent configuration fixes...")
    success = test_agent_configuration()
    exit(0 if success else 1)
