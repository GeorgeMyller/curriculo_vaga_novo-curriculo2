"""
Tool for calculating semantic similarity between two text embeddings.
"""
from typing import List
import numpy as np
from crewai.tools import BaseTool

class SimilarityTool(BaseTool):
    name: str = "Semantic Similarity Tool"
    description: str = "Calculates the cosine similarity between two semantic vector embeddings."

    def _run(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Calculates cosine similarity between two embeddings.

        Args:
            embedding1: The first text embedding (list of floats).
            embedding2: The second text embedding (list of floats).

        Returns:
            The cosine similarity score (float between -1 and 1).
        """
        if not embedding1 or not embedding2:
            # Or raise an error, or return a specific value like -1 or 0
            print("Error: One or both embeddings are empty.")
            return 0.0 

        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)

        if vec1.shape != vec2.shape:
            # Or raise an error
            print("Error: Embeddings have different dimensions.")
            return 0.0
        
        if np.linalg.norm(vec1) == 0 or np.linalg.norm(vec2) == 0:
            # Handle zero vectors to avoid division by zero
            print("Error: One or both embeddings are zero vectors.")
            return 0.0

        cosine_similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
        return float(cosine_similarity)
