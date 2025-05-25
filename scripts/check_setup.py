#!/usr/bin/env python3
"""
Script de verificação rápida da organização do projeto.
Verifica se todos os imports e dependências estão funcionando corretamente.
"""

import sys
import os
from pathlib import Path

def check_project_structure():
    """Verifica se a estrutura do projeto está correta."""
    print("🔍 Verificando estrutura do projeto...")
    
    project_root = Path.cwd()
    required_dirs = [
        'src', 'input', 'output', 'reports', 
        'examples', 'tests', 'scripts', 'docs', 'temp'
    ]
    
    missing_dirs = []
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        if not dir_path.exists():
            missing_dirs.append(dir_name)
        else:
            print(f"✅ {dir_name}/")
    
    if missing_dirs:
        print(f"❌ Diretórios ausentes: {', '.join(missing_dirs)}")
        return False
    
    print("✅ Estrutura de diretórios OK")
    return True

def check_config_files():
    """Verifica se os arquivos de configuração existem."""
    print("\n🔍 Verificando arquivos de configuração...")
    
    project_root = Path.cwd()
    config_files = [
        'src/config/agents.yaml',
        'src/config/tasks.yaml',
        '.env.example',
        'pyproject.toml',
        'requirements.txt'
    ]
    
    missing_files = []
    for file_path in config_files:
        full_path = project_root / file_path
        if not full_path.exists():
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print(f"❌ Arquivos ausentes: {', '.join(missing_files)}")
        return False
    
    print("✅ Arquivos de configuração OK")
    return True

def check_imports():
    """Verifica se os imports principais funcionam."""
    print("\n🔍 Verificando imports...")
    
    try:
        # Adicionar src ao path para imports
        src_path = Path.cwd() / 'src'
        sys.path.insert(0, str(src_path))
        
        from crew import ResumeOptimizerCrew
        print("✅ crew.ResumeOptimizerCrew")
        
        # Verificar se consegue instanciar
        crew_instance = ResumeOptimizerCrew()
        print("✅ Instanciação do ResumeOptimizerCrew")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erro de import: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return False

def check_dependencies():
    """Verifica se as dependências estão instaladas."""
    print("\n🔍 Verificando dependências principais...")
    
    dependencies = [
        ('crewai', 'crewai'),
        ('crewai_tools', 'crewai_tools'), 
        ('python-dotenv', 'dotenv'),
        ('streamlit', 'streamlit'),
        ('pylatexenc', 'pylatexenc')
    ]
    
    missing_deps = []
    for dep_name, import_name in dependencies:
        try:
            __import__(import_name)
            print(f"✅ {dep_name}")
        except ImportError:
            missing_deps.append(dep_name)
            print(f"❌ {dep_name}")
    
    if missing_deps:
        print(f"\n💡 Para instalar dependências ausentes:")
        print(f"   uv sync")
        return False
    
    print("✅ Dependências OK")
    return True

def main():
    """Executa todas as verificações."""
    print("🚀 Verificação da organização do projeto Resume Optimizer Crew\n")
    
    checks = [
        check_project_structure,
        check_config_files,
        check_dependencies,
        check_imports
    ]
    
    all_passed = True
    for check in checks:
        if not check():
            all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("🎉 Todas as verificações passaram!")
        print("💡 O projeto está bem organizado e pronto para uso.")
        print("\n📝 Próximos passos:")
        print("   1. Configure suas chaves API no arquivo .env")
        print("   2. Execute: make run")
        print("   3. Ou use a interface: make streamlit")
    else:
        print("⚠️  Algumas verificações falharam.")
        print("💡 Resolva os problemas acima antes de usar o projeto.")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
