#!/usr/bin/env python3
"""
Test script to verify the similarity calculation works with existing embeddings.
"""
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from tools.similarity_tool import SimilarityTool

def test_similarity():
    """Test similarity calculation with the existing embedding files."""
    
    # Read the embedding files
    try:
        with open('embed_curriculum_report.md', 'r') as f:
            curriculum_embedding_text = f.read()
        
        with open('embed_job_description_report.md', 'r') as f:
            job_embedding_text = f.read()
        
        print("✓ Successfully read embedding files")
        
        # Initialize similarity tool
        similarity_tool = SimilarityTool()
        
        print("📝 Curriculum embedding preview:", curriculum_embedding_text[:100] + "...")
        print("📝 Job embedding preview:", job_embedding_text[:100] + "...")
        
        # Test individual extraction
        curriculum_emb = similarity_tool._extract_embedding_from_text(curriculum_embedding_text)
        job_emb = similarity_tool._extract_embedding_from_text(job_embedding_text)
        
        print(f"📊 Extracted curriculum embedding length: {len(curriculum_emb)}")
        print(f"📊 Extracted job embedding length: {len(job_emb)}")
        
        if curriculum_emb:
            print(f"📊 First 5 values of curriculum embedding: {curriculum_emb[:5]}")
        if job_emb:
            print(f"📊 First 5 values of job embedding: {job_emb[:5]}")
        
        # Calculate similarity
        similarity_score = similarity_tool._run(curriculum_embedding_text, job_embedding_text)
        
        print(f"✓ Similarity calculation completed!")
        print(f"📊 Similarity Score: {similarity_score:.4f}")
        
        # Interpret the score
        if similarity_score >= 0.8:
            interpretation = "Alto Alinhamento"
        elif similarity_score >= 0.6:
            interpretation = "Alinhamento Moderado-Alto"
        elif similarity_score >= 0.4:
            interpretation = "Alinhamento Moderado"
        elif similarity_score >= 0.2:
            interpretation = "Alinhamento Baixo-Moderado"
        else:
            interpretation = "Baixo Alinhamento"
        
        print(f"📈 Interpretação: {interpretation}")
        
        # Create a proper similarity report
        report = f"""# Relatório de Análise de Similaridade

## Score de Similaridade
**Valor:** {similarity_score:.4f}
**Interpretação:** {interpretation}

## Análise
O score de similaridade de {similarity_score:.4f} indica que existe um {interpretation.lower()} entre o currículo analisado e a descrição da vaga para Analista de Dados.

## Recomendações
{"Este é um excelente alinhamento! Continue destacando as competências técnicas relevantes." if similarity_score >= 0.6 else "Há espaço para melhorar o alinhamento. Considere enfatizar mais as habilidades técnicas mencionadas na vaga."}

## Detalhes Técnicos
- Método: Similaridade de Cosseno
- Modelo de Embedding: Gemini text-embedding-004
- Data da Análise: {os.path.basename(__file__)} execution
"""
        
        # Save the report
        with open('similarity_analysis_report.md', 'w') as f:
            f.write(report)
        
        print("✓ Similarity report saved to similarity_analysis_report.md")
        
    except FileNotFoundError as e:
        print(f"❌ Error: Could not find embedding file: {e}")
        return False
    except Exception as e:
        print(f"❌ Error during similarity calculation: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🧪 Testing Similarity Analysis...")
    success = test_similarity()
    if success:
        print("✅ Similarity test completed successfully!")
    else:
        print("❌ Similarity test failed!")
    sys.exit(0 if success else 1)
