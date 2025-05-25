#!/usr/bin/env python3
"""
Script para testar se todos os reports estão sendo direcionados corretamente para a pasta reports/
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.crew import ResumeOptimizerCrew

def test_output_paths():
    """Testa se todos os output paths estão direcionados para a pasta reports"""
    print("🔍 Testando caminhos de output dos reports...\n")
    
    try:
        crew_instance = ResumeOptimizerCrew()
        
        # Lista todas as tarefas e seus output paths
        tasks = [
            ('extract_curriculum_data', crew_instance.extract_curriculum_data()),
            ('analyze_job_description', crew_instance.analyze_job_description()),
            ('embed_curriculum', crew_instance.embed_curriculum()),
            ('embed_job_description', crew_instance.embed_job_description()),
            ('analyze_similarity', crew_instance.analyze_similarity()),
            ('adjust_resume_for_job', crew_instance.adjust_resume_for_job()),
            ('generate_report', crew_instance.generate_report()),
            ('explain_curriculum_learning', crew_instance.explain_curriculum_learning()),
        ]
        
        all_correct = True
        
        for task_name, task in tasks:
            output_path = task.output_file
            points_to_reports = 'reports/' in output_path
            is_absolute = os.path.isabs(output_path)
            
            status = "✅" if points_to_reports else "❌"
            print(f"{status} {task_name}")
            print(f"   Path: {output_path}")
            print(f"   Points to reports/: {points_to_reports}")
            print(f"   Is absolute: {is_absolute}")
            print()
            
            if not points_to_reports:
                all_correct = False
        
        if all_correct:
            print("🎉 Todos os reports estão configurados para serem salvos na pasta reports/")
            print("\n📝 Próximos passos:")
            print("   1. Execute o crew para testar na prática")
            print("   2. Verifique se os arquivos são criados em reports/")
            print("   3. Os reports não devem mais aparecer no diretório raiz")
        else:
            print("⚠️  Alguns reports ainda não estão direcionados corretamente!")
            
    except Exception as e:
        print(f"❌ Erro ao testar: {e}")
        return False
        
    return all_correct

if __name__ == "__main__":
    test_output_paths()
