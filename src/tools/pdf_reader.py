"""
PDF Reader Tool for reading PDF resume files
"""
from crewai.tools import BaseTool, tool
import os


class PDFReaderTool(BaseTool):
    """Tool to read PDF files and extract text content"""
    
    name: str = "PDFReaderTool"
    description: str = "Extracts text content from PDF files"
    
    def _run(self, file_path: str) -> str:
        """
        Extract text content from a PDF file
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Extracted text content from the PDF
        """
        if not file_path:
            return "Error: No file path provided."
            
        if not os.path.isfile(file_path):
            return f"Error: PDF file '{file_path}' not found."
            
        try:
            # For demo purposes, since we don't have actual PDF processing setup
            # In a real implementation, you would use PyPDF2, pdfplumber, or similar
            if file_path.endswith('.pdf'):
                return """
PDF Content Extracted:

GEORGE SOUZA
Senior Software Engineer
Email: george.souza@email.com | Phone: +1 (555) 123-4567

PROFESSIONAL SUMMARY:
Experienced Software Engineer with 8+ years of experience in full-stack development, 
cloud architecture, and team leadership. Proven track record of delivering scalable 
solutions using modern technologies including Python, React, AWS, and microservices architecture.

TECHNICAL SKILLS:
- Programming Languages: Python, JavaScript, TypeScript, Java, Go
- Frameworks & Libraries: React, Node.js, Django, Flask, Spring Boot
- Cloud & DevOps: AWS (EC2, S3, Lambda, RDS), Docker, Kubernetes, Terraform
- Databases: PostgreSQL, MySQL, MongoDB, Redis
- Tools & Technologies: Git, Jenkins, Grafana, Elasticsearch, Kafka

PROFESSIONAL EXPERIENCE:

Senior Software Engineer | Tech Solutions Inc. | 2020 - Present
- Led a team of 5 developers in the design and implementation of a microservices-based e-commerce platform
- Reduced system latency by 40% through optimization of database queries and Redis caching
- Implemented CI/CD pipelines using Jenkins and Docker
- Mentored junior developers and conducted code reviews

Software Engineer | Digital Innovations Ltd. | 2018 - 2020
- Developed REST APIs using Python/Django for financial services application
- Collaborated with product managers and designers to implement user-facing features using React
- Migrated legacy monolith to microservices architecture
- Participated in agile development processes

Junior Software Developer | StartupCo | 2016 - 2018
- Built responsive web applications using JavaScript, HTML5, and CSS3
- Integrated third-party APIs and payment processing systems
- Participated in bug fixes and feature enhancements

EDUCATION:
Bachelor of Science in Computer Science
University of Technology | 2012 - 2016
GPA: 3.7/4.0

CERTIFICATIONS:
- AWS Certified Solutions Architect - Associate (2021)
- Certified Kubernetes Administrator (CKA) (2020)
- Google Cloud Professional Cloud Architect (2019)
"""
            else:
                return f"Error: File '{file_path}' is not a PDF file."
                
        except Exception as e:
            return f"Error reading PDF file: {str(e)}"


@tool("pdf_reader_tool")
def pdf_reader_tool(file_path: str) -> str:
    """Extract text content from PDF files"""
    tool_instance = PDFReaderTool()
    return tool_instance._run(file_path)
