"""
Tool for generating text embeddings using Gemini API.
"""
import os
from typing import List, Optional, Any
import google.generativeai as genai
from crewai.tools import BaseTool
from pydantic import Field, ConfigDict

class EmbeddingTool(BaseTool):
    name: str = "Text Embedding Tool"
    description: str = "Generates a semantic vector embedding for a given text using Google's Gemini API."
    model_name: str = Field(default="models/text-embedding-004", description="The embedding model to use")
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._configure_api()

    def _configure_api(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")
        genai.configure(api_key=api_key)

    def _run(self, text: str) -> List[float]:
        """
        Generates an embedding for the given text.

        Args:
            text: The text to embed.

        Returns:
            A list of floats representing the semantic embedding of the text.
        """
        if not text or not isinstance(text, str):
            return [] # Or raise an error
        try:
            result = genai.embed_content(
                model=self.model_name,
                content=text,
                task_type="retrieval_document"  # or "semantic_similarity" depending on downstream use
            )
            return result['embedding']
        except Exception as e:
            # Consider more specific error handling
            print(f"Error generating embedding: {e}")
            return [] # Or re-raise
