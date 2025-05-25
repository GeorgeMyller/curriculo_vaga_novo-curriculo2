#!/usr/bin/env python3
"""
Test script to verify and fix the Semantic Similarity Tool validation issues.
"""
import sys
import os

# Add src to path
sys.path.insert(0, 'src')

def test_similarity_calculation():
    """Test the similarity calculation logic directly."""
    
    print("🧪 Testing Semantic Similarity Calculation...")
    print("=" * 50)
    
    # Import the actual calculation functions
    from tools.similarity_tool import _process_input, _extract_embedding_from_text
    import numpy as np
    
    # Test Case 1: Check if embedding files exist and can be read
    print("\n📋 Test Case 1: Check embedding files")
    
    curriculum_file = "reports/embed_curriculum_report.md"
    job_file = "reports/embed_job_description_report.md"
    
    if os.path.exists(curriculum_file):
        print(f"✅ {curriculum_file} exists")
        with open(curriculum_file, 'r') as f:
            curriculum_content = f.read()
        curriculum_emb = _extract_embedding_from_text(curriculum_content)
        print(f"   📊 Curriculum embedding: {len(curriculum_emb)} dimensions")
    else:
        print(f"❌ {curriculum_file} not found")
        return
    
    if os.path.exists(job_file):
        print(f"✅ {job_file} exists")
        with open(job_file, 'r') as f:
            job_content = f.read()
        job_emb = _extract_embedding_from_text(job_content)
        print(f"   📊 Job embedding: {len(job_emb)} dimensions")
    else:
        print(f"❌ {job_file} not found")
        return
    
    # Test Case 2: Calculate similarity directly
    print("\n📋 Test Case 2: Direct similarity calculation")
    
    if curriculum_emb and job_emb:
        vec1 = np.array(curriculum_emb)
        vec2 = np.array(job_emb)
        
        if vec1.shape != vec2.shape:
            min_dim = min(len(vec1), len(vec2))
            vec1 = vec1[:min_dim]
            vec2 = vec2[:min_dim]
            print(f"⚠️  Embeddings had different dimensions, truncated both to {min_dim}")
        
        if np.linalg.norm(vec1) == 0 or np.linalg.norm(vec2) == 0:
            print("❌ One or both embeddings are zero vectors")
            return
        
        cosine_similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
        print(f"✅ Similarity Score: {cosine_similarity:.4f}")
        
        # Interpret the score
        if cosine_similarity >= 0.8:
            interpretation = "Alto Alinhamento"
        elif cosine_similarity >= 0.6:
            interpretation = "Alinhamento Moderado-Alto"
        elif cosine_similarity >= 0.4:
            interpretation = "Alinhamento Moderado"
        elif cosine_similarity >= 0.2:
            interpretation = "Alinhamento Baixo-Moderado"
        else:
            interpretation = "Baixo Alinhamento"
        
        print(f"📈 Interpretation: {interpretation}")
        
        return cosine_similarity
    else:
        print("❌ Could not extract embeddings from files")
        return None

def test_tool_callable():
    """Test if we can create a working tool version."""
    
    print("\n� Testing Tool Implementation...")
    print("=" * 50)
    
    # Create a simplified version that should work
    def calculate_similarity_simple(file1: str, file2: str) -> float:
        """Simplified similarity calculation."""
        from tools.similarity_tool import _extract_embedding_from_text
        import numpy as np
        
        try:
            # Read files
            with open(file1, 'r') as f:
                content1 = f.read()
            with open(file2, 'r') as f:
                content2 = f.read()
            
            # Extract embeddings
            emb1 = _extract_embedding_from_text(content1)
            emb2 = _extract_embedding_from_text(content2)
            
            if not emb1 or not emb2:
                return 0.0
            
            # Calculate similarity
            vec1 = np.array(emb1)
            vec2 = np.array(emb2)
            
            if vec1.shape != vec2.shape:
                min_dim = min(len(vec1), len(vec2))
                vec1 = vec1[:min_dim]
                vec2 = vec2[:min_dim]
            
            if np.linalg.norm(vec1) == 0 or np.linalg.norm(vec2) == 0:
                return 0.0
            
            return float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
        
        except Exception as e:
            print(f"Error in calculation: {e}")
            return 0.0
    
    # Test the simplified version
    try:
        result = calculate_similarity_simple(
            "reports/embed_curriculum_report.md",
            "reports/embed_job_description_report.md"
        )
        print(f"✅ Simplified tool result: {result:.4f}")
        return result
    except Exception as e:
        print(f"❌ Simplified tool error: {e}")
        return None

if __name__ == "__main__":
    score1 = test_similarity_calculation()
    score2 = test_tool_callable()
    
    if score1 and score2:
        print(f"\n🎯 SUMMARY:")
        print(f"   Direct calculation: {score1:.4f}")
        print(f"   Tool calculation: {score2:.4f}")
        print(f"   Match: {'✅' if abs(score1 - score2) < 0.001 else '❌'}")
