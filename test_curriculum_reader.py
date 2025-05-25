#!/usr/bin/env python
"""
Script de teste para o agente curriculum_reader
"""
import os
from src.crew import ResumeOptimizerCrew

def test_curriculum_reader():
    print("=== Teste do Agente Curriculum Reader ===")
    
    # Criar instância do crew
    crew_instance = ResumeOptimizerCrew()
    
    # Configurar inputs para a tarefa
    inputs = {
        'resume_path': './input/curriculum.pdf',
        'file_path': './input/curriculum.pdf',
        'query': "Extract professional experiences and academic background"
    }
    
    print(f"Testando com arquivo: {inputs['resume_path']}")
    print(f"Arquivo existe: {os.path.exists(inputs['resume_path'])}")
    
    # Criar apenas a primeira tarefa para teste
    extract_task = crew_instance.extract_curriculum_data()
    agent = crew_instance.curriculum_reader()
    
    print(f"\nAgente: {agent.role}")
    print(f"Ferramentas disponíveis: {[tool.name if hasattr(tool, 'name') else str(type(tool)) for tool in agent.tools]}")
    
    try:
        # Executar apenas a primeira tarefa
        print("\n=== Executando tarefa extract_curriculum_data ===")
        result = agent.execute_task(extract_task, inputs)
        
        print(f"\nResultado:")
        print(result)
        
    except Exception as e:
        print(f"Erro durante execução: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_curriculum_reader()
