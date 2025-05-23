"""
Job Description Reader Tool - Handles both URL and direct text inputs
"""
from crewai_tools import BaseTool
from crewai_tools import SeleniumScrapingTool
from typing import Optional


class JobDescriptionTool(BaseTool):
    """Tool to read job descriptions from either URLs or direct text inputs"""

    name: str = "JobDescriptionTool"
    description: str = "Reads job descriptions from URLs or analyzes provided text."

    def _run(
        self,
        job_url: Optional[str] = None,
        job_text: Optional[str] = None,
        css_selector: str = ".job-description",
        wait_time: int = 5
    ) -> str:
        """
        Processes job descriptions from either a URL or direct text
        
        Args:
            job_url: URL of the job posting (optional)
            job_text: Raw text of the job description (optional)
            css_selector: CSS selector to find job description in webpage (defaults to .job-description)
            wait_time: Seconds to wait for page to load
            
        Returns:
            Job description text
        """
        # If we have direct text, just return it
        if job_text:
            return f"Job Description (provided directly):\n\n{job_text}"
        
        # If we have a URL, use SeleniumScrapingTool to get the content
        elif job_url:
            try:
                scraper = SeleniumScrapingTool(
                    website_url=job_url,
                    css_element=css_selector,
                    wait_time=wait_time
                )
                result = scraper.run()
                return f"Job Description (from URL: {job_url}):\n\n{result}"
            except Exception as e:
                return f"Error scraping job URL {job_url}: {str(e)}"
        
        # If neither is provided
        else:
            return "Error: No job description URL or text provided."
