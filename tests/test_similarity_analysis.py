#!/usr/bin/env python3
"""
Test script for the similarity analysis functionality
"""
import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from tools.similarity_tool import SimilarityTool

def test_similarity_analysis():
    """Test the similarity analysis with the current embedding files"""
    
    print("Testing Similarity Analysis")
    print("=" * 50)
    
    # Initialize the tool
    similarity_tool = SimilarityTool()
    
    # Test with the existing embedding files
    curriculum_file = 'embed_curriculum_report.md'
    job_file = 'embed_job_description_report.md'
    
    # Check if files exist
    if not os.path.exists(curriculum_file):
        print(f"❌ File not found: {curriculum_file}")
        return
    
    if not os.path.exists(job_file):
        print(f"❌ File not found: {job_file}")
        return
    
    print(f"📄 Reading embeddings from:")
    print(f"   - Curriculum: {curriculum_file}")
    print(f"   - Job: {job_file}")
    print()
    
    # Calculate similarity
    try:
        result = similarity_tool._run(curriculum_file, job_file)
        print(f"🔍 Similarity Score: {result:.4f}")
        
        # Interpret the score
        if result >= 0.8:
            interpretation = 'Alto Alinhamento'
            emoji = '🟢'
        elif result >= 0.6:
            interpretation = 'Alinhamento Moderado-Alto'
            emoji = '🟡'
        elif result >= 0.4:
            interpretation = 'Alinhamento Moderado'
            emoji = '🟠'
        elif result >= 0.2:
            interpretation = 'Alinhamento Baixo-Moderado'
            emoji = '🔴'
        else:
            interpretation = 'Baixo Alinhamento'
            emoji = '⚫'
        
        print(f"{emoji} Interpretação: {interpretation}")
        print()
        
        # Provide recommendations based on score
        print("📋 Recomendações:")
        if result >= 0.7:
            print("   ✅ Excelente alinhamento! O currículo está bem adequado à vaga.")
            print("   💡 Foque em destacar ainda mais as competências principais.")
        elif result >= 0.5:
            print("   ⚠️  Alinhamento moderado. Há espaço para melhorias.")
            print("   💡 Identifique e ajuste os pontos de menor correspondência.")
        else:
            print("   🔧 Baixo alinhamento. Adaptações significativas são recomendadas.")
            print("   💡 Revise completamente o currículo para melhor adequação à vaga.")
        
        return result
        
    except Exception as e:
        print(f"❌ Error calculating similarity: {e}")
        return None

if __name__ == "__main__":
    test_similarity_analysis()
