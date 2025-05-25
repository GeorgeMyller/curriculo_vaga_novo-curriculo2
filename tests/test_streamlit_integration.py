#!/usr/bin/env python3
"""
Script de teste para diagnosticar problemas na integração Streamlit-CrewAI
"""

import os
import tempfile
import traceback
from pathlib import Path
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def test_basic_imports():
    """Testa as importações básicas"""
    print("=== Testando Importações ===")
    try:
        from src.streamlit_runner import run_with_streamlit_inputs
        print("✅ Importação do streamlit_runner bem-sucedida")
        
        from src.crew import create_crew, ResumeOptimizerCrew
        print("✅ Importação do crew bem-sucedida")
        
        import crewai
        print(f"✅ CrewAI versão: {crewai.__version__}")
        
        return True
    except Exception as e:
        print(f"❌ Erro nas importações: {e}")
        traceback.print_exc()
        return False

def test_crew_creation():
    """Testa a criação do crew"""
    print("\n=== Testando Criação do Crew ===")
    try:
        from src.crew import create_crew
        crew = create_crew()
        print("✅ Crew criado com sucesso")
        print(f"📊 Agentes: {len(crew.agents)}")
        print(f"📋 Tarefas: {len(crew.tasks)}")
        return True, crew
    except Exception as e:
        print(f"❌ Erro na criação do crew: {e}")
        traceback.print_exc()
        return False, None

def test_simple_crew_run():
    """Testa uma execução simples do crew"""
    print("\n=== Testando Execução Simples do Crew ===")
    try:
        from src.crew import create_crew
        
        # Criar arquivo de teste temporário
        with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False) as f:
            f.write("""
\\documentclass{article}
\\begin{document}
\\section{Dados Pessoais}
Nome: João Silva
Email: joao@email.com

\\section{Experiência}
Desenvolvedor Python - 2 anos

\\section{Habilidades}
Python, SQL, Git
\\end{document}
""")
            temp_resume_path = f.name
        
        crew = create_crew()
        
        # Inputs mínimos para teste
        inputs = {
            'resume_path': temp_resume_path,
            'file_path': temp_resume_path,
            'job_description': 'Vaga para Desenvolvedor Python com experiência em Django e PostgreSQL',
            'job_url': '',
            'job_text': 'Vaga para Desenvolvedor Python com experiência em Django e PostgreSQL',
            'query': 'Extract professional experiences and skills'
        }
        
        print("🚀 Iniciando execução do crew...")
        result = crew.kickoff(inputs=inputs)
        print("✅ Crew executado com sucesso!")
        print(f"📄 Resultado (primeiros 200 chars): {str(result)[:200]}...")
        
        # Limpeza
        os.unlink(temp_resume_path)
        return True, result
        
    except Exception as e:
        print(f"❌ Erro na execução do crew: {e}")
        traceback.print_exc()
        # Limpeza em caso de erro
        try:
            os.unlink(temp_resume_path)
        except:
            pass
        return False, None

def test_streamlit_runner():
    """Testa o módulo streamlit_runner"""
    print("\n=== Testando Streamlit Runner ===")
    try:
        from src.streamlit_runner import run_with_streamlit_inputs
        
        # Criar arquivo de teste temporário
        with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False) as f:
            f.write("""
\\documentclass{article}
\\begin{document}
\\section{Dados Pessoais}
Nome: Maria Santos
Email: maria@email.com

\\section{Experiência}
Analista de Dados - 3 anos
Conhecimento em Python, Pandas, SQL

\\section{Educação}
Bacharelado em Estatística
\\end{document}
""")
            temp_resume_path = f.name
        
        # Criar diretório de output temporário
        with tempfile.TemporaryDirectory() as temp_output_dir:
            print("🚀 Testando run_with_streamlit_inputs...")
            
            result, output_file_path = run_with_streamlit_inputs(
                resume_file_path=temp_resume_path,
                job_url=None,
                job_text="Analista de Dados com experiência em Python, SQL e visualização de dados",
                output_dir=temp_output_dir
            )
            
            print("✅ Streamlit runner executado com sucesso!")
            print(f"📄 Resultado (primeiros 200 chars): {result[:200]}...")
            print(f"📁 Arquivo de output: {output_file_path}")
            print(f"📁 Arquivo existe: {os.path.exists(output_file_path)}")
            
            # Verificar arquivos de relatório gerados
            report_files = [
                'extract_curriculum_data_report.md',
                'analyze_job_description_report.md',
                'adjust_resume_for_job_report.md',
                'execution_report.md'
            ]
            
            print("\n📋 Verificando arquivos de relatório:")
            for report_file in report_files:
                report_path = os.path.join(temp_output_dir, report_file)
                if os.path.exists(report_path):
                    print(f"✅ {report_file} - encontrado")
                else:
                    print(f"❌ {report_file} - não encontrado")
        
        # Limpeza
        os.unlink(temp_resume_path)
        return True
        
    except Exception as e:
        print(f"❌ Erro no streamlit runner: {e}")
        traceback.print_exc()
        # Limpeza em caso de erro
        try:
            os.unlink(temp_resume_path)
        except:
            pass
        return False

def main():
    """Função principal de teste"""
    print("🔍 Diagnóstico da Integração Streamlit-CrewAI")
    print("=" * 50)
    
    # Verificar variáveis de ambiente
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        print(f"✅ GEMINI_API_KEY encontrada (comprimento: {len(api_key)})")
    else:
        print("❌ GEMINI_API_KEY não encontrada")
        return
    
    # Executar testes
    tests = [
        ("Importações Básicas", test_basic_imports),
        ("Criação do Crew", test_crew_creation),
        ("Execução Simples do Crew", test_simple_crew_run),
        ("Streamlit Runner", test_streamlit_runner)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_name == "Criação do Crew":
                success, _ = test_func()
            elif test_name == "Execução Simples do Crew":
                success, _ = test_func()
            else:
                success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ Erro inesperado no teste {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumo dos resultados
    print(f"\n{'='*20} RESUMO DOS TESTES {'='*20}")
    for test_name, success in results:
        status = "✅ PASSOU" if success else "❌ FALHOU"
        print(f"{test_name}: {status}")
    
    total_tests = len(results)
    passed_tests = sum(1 for _, success in results if success)
    print(f"\n📊 Resultado final: {passed_tests}/{total_tests} testes passaram")
    
    if passed_tests == total_tests:
        print("🎉 Todos os testes passaram! A integração parece estar funcionando.")
    else:
        print("⚠️  Alguns testes falharam. Verifique os erros acima para diagnóstico.")

if __name__ == "__main__":
    main()
