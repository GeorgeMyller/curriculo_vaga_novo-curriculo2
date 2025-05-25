"""
Tool for calculating semantic similarity between two text embeddings.
"""
from typing import List, Union, Any
import numpy as np
import ast
import re
from crewai.tools import BaseTool

class SimilarityTool(BaseTool):
    name: str = "Semantic Similarity Tool"
    description: str = "Calculates the cosine similarity between two semantic vector embeddings. Can extract embeddings from context or markdown text."

    def _extract_embedding_from_text(self, text: str) -> List[float]:
        """
        Extract embedding from text that might contain markdown or other formatting.
        """
        # Remove markdown formatting and extract the list
        text = text.strip()
        
        # If the text starts with [, it's already a proper list format
        if text.startswith('[') and text.endswith(']'):
            try:
                embedding = ast.literal_eval(text)
                return [float(x) for x in embedding]
            except (ValueError, SyntaxError) as e:
                print(f"Error parsing embedding list: {e}")
                return []
        
        # Handle case where text starts with [ but doesn't end with ]
        # This happens when the embedding was cut off during saving
        if text.startswith('[') and not text.endswith(']'):
            try:
                # Add closing bracket and try to parse up to the last complete number
                # Find the last comma and complete number
                last_comma = text.rfind(',')
                if last_comma > 0:
                    # Try to find the end of the last complete number
                    truncated_text = text[:last_comma] + ']'
                    embedding = ast.literal_eval(truncated_text)
                    print(f"Warning: Embedding appears truncated, using {len(embedding)} values")
                    return [float(x) for x in embedding]
            except (ValueError, SyntaxError) as e:
                print(f"Error parsing truncated embedding: {e}")
        
        # Look for a list pattern like [0.123, -0.456, ...]
        pattern = r'\[([0-9\-\.e\+,\s]+)\]'
        match = re.search(pattern, text)
        
        if match:
            try:
                # Parse the list string
                list_str = '[' + match.group(1) + ']'
                embedding = ast.literal_eval(list_str)
                return [float(x) for x in embedding]
            except (ValueError, SyntaxError) as e:
                print(f"Error parsing embedding from regex match: {e}")
                return []
        
        # If no brackets found, assume the entire text is comma-separated values
        # This handles cases where the embedding is saved without brackets
        if ',' in text and not text.startswith('#'):
            try:
                # Remove any markdown formatting
                clean_text = text.replace('```', '').replace('`', '').strip()
                # Split by comma and convert to floats
                values = [float(x.strip()) for x in clean_text.split(',') if x.strip()]
                return values
            except (ValueError, TypeError) as e:
                print(f"Error parsing comma-separated values: {e}")
                return []
        
        return []

    def _process_input(self, input_data: Any) -> List[float]:
        """
        Process various input formats to extract embedding vectors.
        """
        if isinstance(input_data, list) and all(isinstance(x, (int, float)) for x in input_data):
            # Already a proper embedding
            return input_data
        elif isinstance(input_data, str):
            # Check if it's a file path and try to read the file
            if input_data.endswith('.md') or input_data.endswith('.txt'):
                try:
                    import os
                    if os.path.exists(input_data):
                        with open(input_data, 'r', encoding='utf-8') as f:
                            file_content = f.read()
                        print(f"Read file {input_data}, extracting embedding...")
                        return self._extract_embedding_from_text(file_content)
                except Exception as e:
                    print(f"Error reading file {input_data}: {e}")
            
            # Try to extract embedding from string
            return self._extract_embedding_from_text(input_data)
        elif isinstance(input_data, dict):
            # Check if it's a dict with embedding data
            if 'embedding' in input_data:
                return self._process_input(input_data['embedding'])
            elif 'content' in input_data:
                return self._extract_embedding_from_text(str(input_data['content']))
            else:
                return self._extract_embedding_from_text(str(input_data))
        else:
            # Try to convert to string and extract
            return self._extract_embedding_from_text(str(input_data))

    def _run(self, embedding1: Any, embedding2: Any = None, context_data: Any = None) -> float:
        """
        Calculates cosine similarity between two embeddings.

        Args:
            embedding1: The first text embedding (can be various formats).
            embedding2: The second text embedding (can be various formats).
            context_data: Additional context data that might contain embeddings.

        Returns:
            The cosine similarity score (float between -1 and 1).
        """
        # If context_data is provided and embedding2 is None, try to extract both from context
        if context_data and embedding2 is None:
            if isinstance(context_data, list) and len(context_data) >= 2:
                # Try to extract two embeddings from context
                emb1 = self._process_input(context_data[0])
                emb2 = self._process_input(context_data[1])
            else:
                print("Error: Need two embeddings for similarity calculation.")
                return 0.0
        else:
            # Process the provided embeddings
            emb1 = self._process_input(embedding1)
            emb2 = self._process_input(embedding2) if embedding2 else []

        if not emb1 or not emb2:
            print("Error: One or both embeddings are empty or could not be extracted.")
            return 0.0 

        vec1 = np.array(emb1)
        vec2 = np.array(emb2)

        if vec1.shape != vec2.shape:
            # If dimensions don't match, truncate both to the smaller dimension
            min_dim = min(len(vec1), len(vec2))
            vec1 = vec1[:min_dim]
            vec2 = vec2[:min_dim]
            print(f"Warning: Embeddings had different dimensions, truncated both to {min_dim} dimensions")
        
        if np.linalg.norm(vec1) == 0 or np.linalg.norm(vec2) == 0:
            print("Error: One or both embeddings are zero vectors.")
            return 0.0

        cosine_similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
        return float(cosine_similarity)
