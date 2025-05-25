"""
Job Description Reader Tool - Handles both URL and direct text inputs
"""
from crewai.tools import BaseTool, tool
from crewai_tools import ScrapeWebsiteTool
from typing import Optional
import requests
from bs4 import BeautifulSoup


class JobDescriptionTool(BaseTool):
    """Tool to read job descriptions from either URLs or direct text inputs"""

    name: str = "JobDescriptionTool"
    description: str = "Reads job descriptions from URLs or analyzes provided text."

    def _run(
        self,
        job_url: str
    ) -> str:
        """
        Processes job descriptions from a URL
        
        Args:
            job_url: URL of the job posting
            
        Returns:
            Job description text
        """
        if job_url:
            try:
                # First try with ScrapeWebsiteTool
                scraper = ScrapeWebsiteTool()
                result = scraper.run(website_url=job_url)
                if result and len(result.strip()) > 50:
                    return f"Job Description (from URL: {job_url}):\n\n{result}"
                
                # Fallback to simple requests + BeautifulSoup
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                response = requests.get(job_url, headers=headers, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Try common selectors for job descriptions
                selectors = [
                    '.job-description', '.job-desc', '.description',
                    '.job-content', '.content', '.posting-description',
                    '[data-testid="job-description"]', '.job-details'
                ]
                
                content = ""
                for selector in selectors:
                    elements = soup.select(selector)
                    if elements:
                        content = ' '.join([elem.get_text(strip=True) for elem in elements])
                        break
                
                # If no specific selector worked, get all text
                if not content:
                    content = soup.get_text(separator=' ', strip=True)
                
                # Clean up the content
                content = ' '.join(content.split())  # Remove extra whitespace
                
                if content:
                    return f"Job Description (from URL: {job_url}):\n\n{content}"
                else:
                    return f"Error: Could not extract content from {job_url}"
                    
            except Exception as e:
                # Return a sample job description for testing
                return f"""Job Description (sample - could not fetch from {job_url}):\n\n
Senior Operations Analyst Position

We are seeking a highly motivated Senior Operations Analyst to join our dynamic team. 

RESPONSIBILITIES:
- Analyze operational data and identify trends and opportunities for improvement
- Develop and maintain dashboards and reports for executive management
- Collaborate with cross-functional teams to optimize business processes
- Lead process improvement initiatives and change management projects
- Monitor KPIs and provide actionable insights to stakeholders

REQUIRED QUALIFICATIONS:
- Bachelor's degree in Business, Operations Management, or related field
- 5+ years of experience in operations analysis or business intelligence
- Proficiency in SQL, Python, and data visualization tools (Tableau, Power BI)
- Strong analytical and problem-solving skills
- Experience with process improvement methodologies (Lean, Six Sigma)
- Excellent communication and presentation skills

PREFERRED QUALIFICATIONS:
- Master's degree in related field
- Experience with cloud platforms (AWS, Azure)
- Knowledge of statistical analysis and machine learning
- Project management certification (PMP, Agile)
- Experience in e-commerce or technology industry

WHAT WE OFFER:
- Competitive salary and benefits package
- Remote work flexibility
- Professional development opportunities
- Collaborative and innovative work environment

Error details: {str(e)}"""
        
        # If URL is not provided
        else:
            return "Error: No job description URL provided."


@tool("job_description_tool")
def job_description_tool(job_url: str) -> str:
    """Read job descriptions from URLs"""
    tool_instance = JobDescriptionTool()
    return tool_instance._run(job_url=job_url)
