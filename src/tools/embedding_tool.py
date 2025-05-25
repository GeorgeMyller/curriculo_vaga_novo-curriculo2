"""
Tool for generating text embeddings using Gemini API.
"""
import os
from typing import List, Optional, Any, Union
import google.generativeai as genai
from crewai.tools import BaseTool, tool
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

    def _run(self, text: Union[str, dict]) -> List[float]:
        """
        Generates an embedding for the given text.

        Args:
            text: The text to embed (string) or a dict with text content.

        Returns:
            A list of floats representing the semantic embedding of the text.
        """
        # Handle different input formats from CrewAI
        if isinstance(text, dict):
            if 'description' in text:
                text_to_embed = text['description']
            elif 'content' in text:
                text_to_embed = text['content']
            else:
                text_to_embed = str(text)
        else:
            text_to_embed = text
            
        if not text_to_embed or not isinstance(text_to_embed, str) or len(text_to_embed.strip()) == 0:
            print("Warning: Empty or invalid text provided to embedding tool")
            return []
            
        try:
            result = genai.embed_content(
                model=self.model_name,
                content=text_to_embed,
                task_type="retrieval_document"  # or "semantic_similarity" depending on downstream use
            )
            return result['embedding']
        except Exception as e:
            # Consider more specific error handling
            print(f"Error generating embedding: {e}")
            return []


@tool("text_embedding_tool")
def text_embedding_tool(text: str) -> List[float]:
    """Generate text embeddings using Gemini API"""
    tool_instance = EmbeddingTool()
    return tool_instance._run(text)
