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
        print(f"Por favor, coloque um arquivo .pdf ou .tex no diretório {input_dir}")
        sys.exit(1)
    
    # Determinar o arquivo de currículo principal - Priorizar LaTeX sobre PDF
    resume_file = latex_files[0] if latex_files else (pdf_files[0] if pdf_files else None)
    print(f"Usando arquivo de currículo: {resume_file}")

    inputs = {
        'resume_path': str(resume_file),
        'file_path': str(resume_file),  # Use the same file for both
        'job_url': args.job_url,
        'job_description': """Data Analyst Position

Company: Tech Solutions Inc.

JOB DESCRIPTION:
We are seeking a skilled Data Analyst to join our growing team. The ideal candidate will have experience in data analysis, statistical modeling, and business intelligence.

KEY RESPONSIBILITIES:
- Analyze large datasets to identify trends and insights
- Create reports and dashboards for stakeholders
- Collaborate with cross-functional teams
- Develop and maintain data pipelines
- Present findings to management

REQUIRED SKILLS:
- Proficiency in Python, SQL, and Excel
- Experience with data visualization tools (Tableau, Power BI)
- Knowledge of statistical analysis methods
- Strong communication and problem-solving skills
- Bachelor's degree in related field

PREFERRED QUALIFICATIONS:
- Experience with machine learning algorithms
- Knowledge of cloud platforms (AWS, Azure)
- Experience in technology industry""",  # Use the embedded job description
        'query': "Extract professional experiences, skills, and academic background from the curriculum"
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
