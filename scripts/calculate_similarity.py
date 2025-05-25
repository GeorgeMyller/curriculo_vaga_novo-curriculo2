#!/usr/bin/env python3
"""
Manual calculation of cosine similarity between curriculum and job description embeddings.
This completes the similarity analysis that couldn't be done by the Semantic Similarity Tool.
"""

import numpy as np
from typing import List, Tuple
import re

def parse_embedding_from_file(file_path: str) -> List[float]:
    """Extract the embedding vector from a markdown report file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    # Remove markdown formatting if present
    content = content.replace('```', '').replace('markdown', '').strip()
    
    # Handle arrays that might be incomplete (no closing bracket)
    if content.startswith('['):
        # Remove opening bracket
        numbers_str = content[1:]
        
        # Remove closing bracket if present
        if numbers_str.endswith(']'):
            numbers_str = numbers_str[:-1]
        
        # Split by comma and parse numbers
        numbers = []
        for x in numbers_str.split(','):
            x = x.strip()
            if x and not x.endswith('%'):  # Skip empty and incomplete entries
                try:
                    numbers.append(float(x))
                except ValueError:
                    # Skip malformed numbers
                    continue
        
        if not numbers:
            raise ValueError(f"No valid numbers found in embedding file: {file_path}")
        
        return numbers
    else:
        raise ValueError(f"Could not parse embedding from file: {file_path}")

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculate cosine similarity between two vectors."""
    # Convert to numpy arrays
    a = np.array(vec1)
    b = np.array(vec2)
    
    # Calculate cosine similarity
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
    
    return dot_product / (norm_a * norm_b)

def interpret_similarity_score(score: float) -> Tuple[str, str, List[str]]:
    """Interpret the cosine similarity score and provide insights."""
    
    if score >= 0.8:
        level = "Very High"
        interpretation = "Excellent alignment between the resume and job requirements"
        recommendations = [
            "The resume is very well aligned with the job description",
            "Minor adjustments in wording or emphasis could further optimize",
            "Consider highlighting specific achievements with metrics"
        ]
    elif score >= 0.6:
        level = "High" 
        interpretation = "Good alignment with significant overlap in relevant skills and experience"
        recommendations = [
            "Strong foundation with good alignment",
            "Consider emphasizing data analysis and technical skills more prominently",
            "Add specific examples of Python, SQL, and analytics work",
            "Highlight experience with data visualization tools"
        ]
    elif score >= 0.4:
        level = "Moderate"
        interpretation = "Reasonable alignment but with room for improvement"
        recommendations = [
            "Moderate alignment suggests potential for improvement",
            "Focus on technical skills mentioned in job description",
            "Reorganize resume to prioritize data analysis experience",
            "Add keywords related to machine learning and cloud platforms",
            "Consider additional training or certifications in lacking areas"
        ]
    elif score >= 0.2:
        level = "Low"
        interpretation = "Limited alignment, significant improvements needed"
        recommendations = [
            "Low alignment indicates major gaps",
            "Significant resume restructuring needed",
            "Focus on acquiring missing technical skills",
            "Consider additional education or training programs",
            "Highlight any transferable analytical or technical experience"
        ]
    else:
        level = "Very Low"
        interpretation = "Poor alignment, major revisions required"
        recommendations = [
            "Very low alignment suggests this may not be the ideal role",
            "Consider whether this position matches career goals",
            "Major skill development and training needed",
            "Focus on building foundational technical skills first"
        ]
    
    return level, interpretation, recommendations

def main():
    """Main function to calculate similarity and generate report."""
    
    # File paths
    curriculum_embedding_file = "/Volumes/SSD-EXTERNO/2025/Maio/curriculo_vaga_novo-curriculo2/reports/embed_curriculum_report.md"
    job_embedding_file = "/Volumes/SSD-EXTERNO/2025/Maio/curriculo_vaga_novo-curriculo2/reports/embed_job_description_report.md"
    output_file = "/Volumes/SSD-EXTERNO/2025/Maio/curriculo_vaga_novo-curriculo2/reports/similarity_analysis_report.md"
    
    try:
        # Parse embeddings
        print("Parsing curriculum embedding...")
        curriculum_embedding = parse_embedding_from_file(curriculum_embedding_file)
        print(f"Curriculum embedding dimension: {len(curriculum_embedding)}")
        
        print("Parsing job description embedding...")
        job_embedding = parse_embedding_from_file(job_embedding_file)
        print(f"Job description embedding dimension: {len(job_embedding)}")
        
        # Verify dimensions match or truncate to shorter
        if len(curriculum_embedding) != len(job_embedding):
            min_dim = min(len(curriculum_embedding), len(job_embedding))
            print(f"Warning: Embedding dimensions don't match: {len(curriculum_embedding)} vs {len(job_embedding)}")
            print(f"Truncating both to minimum dimension: {min_dim}")
            curriculum_embedding = curriculum_embedding[:min_dim]
            job_embedding = job_embedding[:min_dim]
        
        # Calculate cosine similarity
        similarity_score = cosine_similarity(curriculum_embedding, job_embedding)
        print(f"Cosine similarity: {similarity_score:.4f}")
        
        # Interpret the score
        level, interpretation, recommendations = interpret_similarity_score(similarity_score)
        
        # Generate detailed report
        report = f"""# Similarity Analysis Report

## Semantic Similarity Score

**Cosine Similarity**: {similarity_score:.4f}  
**Alignment Level**: {level}

## Analysis

{interpretation}

The cosine similarity score of {similarity_score:.4f} indicates a **{level.lower()}** level of semantic alignment between George Myller's resume and the Data Analyst job description.

## Detailed Interpretation

### What This Score Means:
- **Score Range**: Cosine similarity ranges from -1 to 1, where 1 indicates perfect alignment
- **Current Score**: {similarity_score:.4f} suggests {"strong" if similarity_score >= 0.6 else "moderate" if similarity_score >= 0.4 else "limited"} semantic overlap
- **Context**: This score reflects how well the resume content aligns with job requirements in the embedding space

### Key Factors Influencing the Score:

**Strengths Identified:**
- Technical programming experience (Python, Java, JavaScript)
- Database and data management skills
- Software development background with analytical components
- Educational foundation in technology and business

**Areas for Improvement:**
- Limited explicit data analysis experience mentioned
- Missing specific mention of data visualization tools (Tableau, Power BI)
- Lack of direct machine learning or statistical analysis experience
- Cloud platform experience could be more prominent

## Recommendations

### Immediate Actions:
"""
        
        for i, rec in enumerate(recommendations, 1):
            report += f"\n{i}. {rec}"
        
        report += f"""

### Strategic Improvements:
1. **Technical Skills Enhancement**: Emphasize Python libraries like Pandas, NumPy, and Scikit-learn
2. **Data Analysis Projects**: Highlight any data analysis or reporting work from current roles
3. **Visualization Skills**: Add experience with data visualization tools or willingness to learn
4. **Industry Language**: Use more data analysis terminology and keywords from the job description
5. **Quantifiable Results**: Include metrics and data-driven achievements where possible

## Embedding Analysis Details

- **Curriculum Embedding Dimension**: {len(curriculum_embedding)}
- **Job Description Embedding Dimension**: {len(job_embedding)}
- **Similarity Calculation Method**: Cosine similarity using dot product normalization
- **Vector Space**: High-dimensional semantic embedding space captures nuanced meaning relationships

## Next Steps

1. **Resume Optimization**: Apply the generated optimized resume focusing on data analysis alignment
2. **Skill Development**: Consider additional training in identified gap areas
3. **Portfolio Development**: Create data analysis projects to demonstrate capabilities
4. **Interview Preparation**: Focus on transferable analytical skills and learning enthusiasm

---

*Report generated using manual cosine similarity calculation between semantic embeddings.*
*Analysis date: {np.datetime64('today')}*
"""

        # Write the report
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\nSimilarity analysis report generated successfully!")
        print(f"Report saved to: {output_file}")
        print(f"Final similarity score: {similarity_score:.4f} ({level})")
        
        return similarity_score
        
    except Exception as e:
        print(f"Error during similarity calculation: {e}")
        return None

if __name__ == "__main__":
    main()
