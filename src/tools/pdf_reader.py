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
            if file_path.endswith('.pdf'):
                # Try to import PDF processing libraries (prefer pypdf over deprecated PyPDF2)
                try:
                    from pypdf import PdfReader
                    
                    with open(file_path, 'rb') as file:
                        pdf_reader = PdfReader(file)
                        text = ""
                        for page in pdf_reader.pages:
                            text += page.extract_text() + "\n"
                    
                    if text.strip():
                        return f"PDF Content Extracted:\n\n{text}"
                    else:
                        return "Error: No text could be extracted from the PDF file."
                        
                except ImportError:
                    # Fallback to PyPDF2 if pypdf is not available
                    try:
                        import PyPDF2
                        
                        with open(file_path, 'rb') as file:
                            pdf_reader = PyPDF2.PdfReader(file)
                            text = ""
                            for page in pdf_reader.pages:
                                text += page.extract_text() + "\n"
                        
                        if text.strip():
                            return f"PDF Content Extracted:\n\n{text}"
                        else:
                            return "Error: No text could be extracted from the PDF file."
                            
                    except ImportError:
                        # Final fallback to pdfplumber
                        try:
                            import pdfplumber
                            
                            with pdfplumber.open(file_path) as pdf:
                                text = ""
                                for page in pdf.pages:
                                    page_text = page.extract_text()
                                    if page_text:
                                        text += page_text + "\n"
                            
                            if text.strip():
                                return f"PDF Content Extracted:\n\n{text}"
                            else:
                                return "Error: No text could be extracted from the PDF file."
                                
                        except ImportError:
                            return "Error: PDF processing libraries (pypdf, PyPDF2 or pdfplumber) are not installed. Please install one of them: 'uv add pypdf' or 'uv add pdfplumber'"
                
            else:
                return f"Error: File '{file_path}' is not a PDF file."
                
        except Exception as e:
            return f"Error reading PDF file: {str(e)}"


@tool("pdf_reader_tool")
def pdf_reader_tool(file_path: str) -> str:
    """Extract text content from PDF files"""
    tool_instance = PDFReaderTool()
    return tool_instance._run(file_path)
