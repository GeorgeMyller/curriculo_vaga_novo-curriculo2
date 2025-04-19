#!/usr/bin/env python
"""
Script principal para executar o otimizador de currículo com CrewAI.
"""

import os
import sys
import argparse
from pathlib import Path
from crew import ResumeOptimizerCrew

def main():
    # Configurar o parser de argumentos
    parser = argparse.ArgumentParser(description='Otimizador de Currículo com CrewAI')
    parser.add_argument('--input-dir', type=str, default='./input', 
                        help='Diretório contendo os arquivos de currículo (PDF e LaTeX)')
    parser.add_argument('--job-url', type=str, required=True,
                        help='URL da descrição da vaga')
    parser.add_argument('--output-dir', type=str, default='./output',
                        help='Diretório para salvar os resultados')
    
    args = parser.parse_args()
    
    # Criar diretórios se não existirem
    input_dir = Path(args.input_dir).absolute()
    output_dir = Path(args.output_dir).absolute()
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    # Verificar se existem arquivos no diretório de entrada
    pdf_files = list(input_dir.glob('*.pdf'))
    latex_files = list(input_dir.glob('*.tex'))
    
    if not pdf_files and not latex_files:
        print(f"Erro: Nenhum arquivo PDF ou LaTeX encontrado em {input_dir}")
        sys.exit(1)
    

    inputs = {
        'resume_path': str(input_dir / 'curriculum.tex'),
        'file_path': str(input_dir / 'curriculum.pdf'),
        'job_url': args.job_url
    }
    # Executar a equipe com os inputs necessários
    crew_output = ResumeOptimizerCrew().crew().kickoff(inputs=inputs)

    # Print the result of the Crew execution
    print(crew_output)
    
    print("\n=== Processo concluído ===")
    print(f"Resultados salvos em: {output_dir}")
    print("\nRelatório final:")
    print(crew_output)

if __name__ == "__main__":
    main()
