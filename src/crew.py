"""
Este módulo define a orquestração do CrewAI para o processo de otimização de currículos.
Implementa um sistema multi-agente que lê currículos, analisa descrições de vagas,
analisa semanticamente a similaridade e produz conteúdo de currículo personalizado.
"""
import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task, tool
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

# Importação de ferramentas e configurações necessárias
from crewai_tools import PDFSearchTool, SeleniumScrapingTool, FileReadTool, FileWriterTool

from src.tools.latex_reader import LatexReaderTool
from src.tools.job_description_tool import JobDescriptionTool
from src.tools.pdf_reader import PDFReaderTool
from src.tools.embedding_tool import EmbeddingTool # Nova ferramenta
from src.tools.similarity_tool import SimilarityTool # Nova ferramenta
from dotenv import load_dotenv
import yaml # Para carregar configs YAML

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração do LLM (Usando LiteLLM format for CrewAI compatibility)
# For LiteLLM, Gemini models should be prefixed with 'gemini/'
llm = LLM(
    model="gemini/gemini-1.5-flash-latest",
    api_key=os.getenv("GEMINI_API_KEY"),
    # temperature=0.1 # Ajuste conforme necessário
)

# Carregar configurações de agentes e tarefas do YAML
# When using @CrewBase decorator, the YAML files are loaded automatically
# We only need to specify the paths in the class attributes


# Instanciação das Ferramentas
# Note: PDFSearchTool has issues with Google embeddings, so we'll use a simpler configuration
# or fall back to default embeddings. The embedder configuration seems to have compatibility issues.

def get_tools():
    """Create and return tool instances to avoid import-time issues"""
    pdf_tool = PDFSearchTool(
        # pdf='dummy.pdf', # O PDF real será passado pela tarefa
        config={
            "llm": {
                "provider": "google", # ou "openai", "ollama" etc.
                "config": {
                    "model": "gemini-1.5-flash-latest",
                    "api_key": os.getenv("GEMINI_API_KEY"), # API key necessária para PDFSearchTool
                },
            },
            # Commenting out embedder config due to GoogleAIEmbedderConfig compatibility issues
            # "embedder": {
            #     "provider": "google", # ou "openai", "ollama" etc.
            #     "config": {
            #         "model": "models/embedding-001",
            #         "api_key": os.getenv("GEMINI_API_KEY"), # API key necessária para embedder
            #         # "task_type": "retrieval_document" # Ajuste conforme a API do embedder
            #     },
            # },
        }
    )

    selenium_tool = SeleniumScrapingTool(
        # website_url será passado pela tarefa
        # css_selector=".job-description", # Pode ser definido na tarefa ou aqui se for padrão
        # wait_time=5
    )

    latex_tool = LatexReaderTool()
    file_write_tool = FileWriterTool()
    embedding_tool = EmbeddingTool() # Usa GEMINI_API_KEY do .env internamente
    file_read_tool = FileReadTool() # Para ler o conteúdo do currículo e da vaga para embedding
    similarity_tool = SimilarityTool() # Nova ferramenta - Moved instantiation before CrewBase
    
    return {
        'pdf_tool': pdf_tool,
        'selenium_tool': selenium_tool,
        'latex_tool': latex_tool,
        'file_write_tool': file_write_tool,
        'embedding_tool': embedding_tool,
        'file_read_tool': file_read_tool,
        'similarity_tool': similarity_tool
    }


@CrewBase
class ResumeOptimizerCrew():
    """Equipe de Otimização de Currículo - Orquestra agentes para otimizar um currículo com base em descrições de emprego e análise semântica"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        # Initialize tools when the crew is created
        self.tools = get_tools()
        super().__init__()
    
    # Tool methods for YAML tool references
    @tool
    def text_embedding_tool(self):
        """Text embedding tool for generating semantic embeddings"""
        return self.tools['embedding_tool']
    
    @tool
    def semantic_similarity_tool(self):
        """Semantic similarity tool for comparing embeddings"""
        return self.tools['similarity_tool']
    
    @tool
    def latex_reader_tool(self):
        """LaTeX reader tool for reading .tex files"""
        return self.tools['latex_tool']
    
    @tool
    def pdf_search_tool(self):
        """PDF search tool for reading and searching PDF files"""
        return self.tools['pdf_tool']
    
    @tool
    def file_writer_tool(self):
        """File writer tool for writing output files"""
        return self.tools['file_write_tool']

    @agent
    def curriculum_reader(self) -> Agent:
        return Agent(
            **self.agents_config['curriculum_reader'],
            tools=[
                self.tools['pdf_tool'],
                self.tools['latex_tool'],
                self.tools['file_write_tool'], # Added back file_write_tool
                self.tools['file_read_tool'] # Para ler o arquivo antes de passar para embedding
            ],
            verbose=True,
            llm=llm,
            allow_delegation=False
            # output_file foi removido, a escrita de arquivos é responsabilidade de uma Tarefa/Ferramenta
        )

    @agent
    def job_analyzer(self) -> Agent:
        job_tool = JobDescriptionTool() # Esta ferramenta lida com URL ou texto
        return Agent(
            **self.agents_config['job_analyzer'],
            tools=[job_tool, self.tools['file_read_tool']], # Adicionado file_read_tool se a vaga for local
            verbose=True,
            allow_delegation=False,
            llm=llm,
        )

    @agent
    def alignment_analyzer(self) -> Agent:
        return Agent(
            **self.agents_config['alignment_analyzer'],
            tools=[self.tools['embedding_tool'], self.tools['similarity_tool']],
            verbose=True,
            llm=llm, # Usar um LLM mais potente se a análise for complexa
            allow_delegation=False
        )

    @agent
    def resume_editor(self) -> Agent:
        return Agent(
            **self.agents_config['resume_editor'],
            tools=[self.tools['file_write_tool']], # Para salvar o .tex final
            verbose=True,
            llm=llm,
            allow_delegation=False
        )

    @agent
    def reporting_agent(self) -> Agent:
        return Agent(
            **self.agents_config['reporting_agent'],
            tools=[self.tools['file_write_tool']], # Para salvar o relatório final
            verbose=True,
            llm=llm,
            allow_delegation=False
        )

    # --- Definição das Tarefas ---
    @task
    def extract_curriculum_data_task(self) -> Task:
        return Task(
            **self.tasks_config['extract_curriculum_data'],
            agent=self.curriculum_reader(),
            # O output_file é definido no YAML da tarefa ou gerenciado pela ferramenta
        )

    @task
    def analyze_job_description_task(self) -> Task:
        return Task(
            **self.tasks_config['analyze_job_description'],
            agent=self.job_analyzer(),
        )

    @task
    def embed_curriculum_task(self) -> Task:
        return Task(
            **self.tasks_config['embed_curriculum'],
            agent=self.alignment_analyzer(),
            context=[self.extract_curriculum_data_task()],
            # O output da tarefa anterior (texto do currículo) será o input desta
        )

    @task
    def embed_job_description_task(self) -> Task:
        return Task(
            **self.tasks_config['embed_job_description'],
            agent=self.alignment_analyzer(),
            context=[self.analyze_job_description_task()],
        )

    @task
    def analyze_similarity_task(self) -> Task:
        return Task(
            **self.tasks_config['analyze_similarity'],
            agent=self.alignment_analyzer(),
            context=[self.embed_curriculum_task(), self.embed_job_description_task()],
        )

    @task
    def adjust_resume_for_job_task(self) -> Task:
        return Task(
            **self.tasks_config['adjust_resume_for_job'],
            agent=self.resume_editor(),
            context=[
                self.extract_curriculum_data_task(),
                self.analyze_job_description_task(),
                self.analyze_similarity_task()
            ],
        )

    @task
    def generate_report_task(self) -> Task:
        return Task(
            **self.tasks_config['generate_report'],
            agent=self.reporting_agent(),
            context=[
                self.extract_curriculum_data_task(),
                self.analyze_job_description_task(),
                self.embed_curriculum_task(),
                self.embed_job_description_task(),
                self.analyze_similarity_task(),
                self.adjust_resume_for_job_task()
            ],
        )

    @task
    def explain_curriculum_learning_task(self) -> Task:
        return Task(
            **self.tasks_config['explain_curriculum_learning'],
            agent=self.curriculum_reader(),
            context=[self.extract_curriculum_data_task()],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.curriculum_reader(),
                self.job_analyzer(),
                self.alignment_analyzer(),
                self.resume_editor(),
                self.reporting_agent()
            ],
            tasks=[
                self.extract_curriculum_data_task(),
                self.explain_curriculum_learning_task(),
                self.analyze_job_description_task(),
                self.embed_curriculum_task(),
                self.embed_job_description_task(),
                self.analyze_similarity_task(),
                self.adjust_resume_for_job_task(),
                self.generate_report_task()
            ],
            process=Process.sequential,
            verbose=True, # Changed from 2 to True
            # memory=True # Ativar memória se os agentes precisarem lembrar de interações passadas
            # manager_llm=llm # Para processo hierárquico
        )

# Function to create and return a configured crew (for Streamlit integration)
def create_crew():
    """
    Creates and returns a configured ResumeOptimizerCrew instance.
    This function is used by the Streamlit runner.
    """
    return ResumeOptimizerCrew().crew()

# Ponto de entrada para depuração ou execução direta
if __name__ == "__main__":
    print("## Bem-vindo à Equipe de Otimização de Currículos! ##")
    # Aqui você pode adicionar lógica para pegar inputs do usuário
    resume_path_input = "input/curriculo.tex" # Exemplo
    job_description_input = "https://www.linkedin.com/jobs/view/some-job-id" # Exemplo de URL
    # job_description_input = "Analista de Dados Pleno com experiência em Python, SQL e PowerBI." # Exemplo de texto

    inputs = {
        "resume_path": resume_path_input,
        "job_description": job_description_input, # A tarefa analyze_job_description espera este input
        # Adicione outros inputs que suas tarefas esperam, ex:
        # "job_url": job_description_input if job_description_input.startswith("http") else None,
        # "job_text": job_description_input if not job_description_input.startswith("http") else None,
    }

    resume_optimizer_crew = ResumeOptimizerCrew().crew()
    result = resume_optimizer_crew.kickoff(inputs=inputs)

    print("\n\n########################")
    print("## Resultado Final da Equipe:")
    print(result)
    print("########################")
    # O resultado final (currículo otimizado) estará no arquivo definido pela tarefa `adjust_resume_for_job`
    # e o relatório de similaridade em `similarity_analysis_report.md` (se configurado).
