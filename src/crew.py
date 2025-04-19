"""
Este módulo define a orquestração do CrewAI para o processo de otimização de currículos.
Implementa um sistema multi-agente que lê currículos, analisa descrições de vagas,
e produz conteúdo de currículo personalizado com base nos requisitos da vaga.
"""
import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
# Importação de ferramentas e configurações necessárias
from crewai_tools import PDFSearchTool, SeleniumScrapingTool
from tools.latex_reader import LatexReaderTool 
from dotenv import load_dotenv


# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

pdf_tool = PDFSearchTool(
config={
    "embedder": {
        "provider": "google",
        "config": {
            "model": "models/embedding-001",
            "task_type": "retrieval_document"
        }
    }
}
)


selenium_tool = SeleniumScrapingTool(
website_url="https://jobs.foundever.com/job/Porto-Data-Analyst-Porto%2C-Portugal-Port/1278591600/?utm_source=LINKEDIN&utm_medium=referrer",
css_element=".job-description",  # Seletor CSS para a descrição da vaga
wait_time=5  # Tempo de espera para carregamento da página
) 

latex_tool = LatexReaderTool


agents_config = "config/agents.yaml"
tasks_config = "config/tasks.yaml"

@CrewBase
class ResumeOptimizerCrew():
    """Equipe de Otimização de Currículo - Orquestra agentes para otimizar um currículo com base em descrições de emprego"""

    @agent
    def curriculum_reader(self) -> Agent:
            return Agent(
            config=self.agents_config['curriculum_reader'],
            tools=[
                pdf_tool,
                latex_tool 
            ],            
            verbose=True,  # Ativa logs detalhados para acompanhamento
            # Utiliza o modelo Gemini 1.5 Flash como LLM para processamento de linguagem
            llm=LLM("gemini/gemini-1.5-flash", credentials=os.getenv('GOOGLE_API_KEY')),
            output_file='output/curriculum_reader.md'  # Armazena os dados processados neste arquivo
        )

    @agent
    def css_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['css_analyzer'],
            tools=[selenium_tool],
            llm=LLM("gemini/gemini-1.5-flash", credentials=os.getenv('GOOGLE_API_KEY')),
            output_file='output/css_analyzer.md'

        )
    @agent
    def job_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['job_analyzer'],
            tools=[selenium_tool],  # Utiliza selenium para navegar e extrair dados de sites de vagas
            verbose=True,
            allow_delegation=False,  # Desativa delegação para manter o controle do fluxo de trabalho
            llm=LLM("gemini/gemini-1.5-flash", credentials=os.getenv('GOOGLE_API_KEY')),
            output_file='output/job_analyzer.md'
        )

    @agent
    def resume_editor(self) -> Agent:
        return Agent(
            config=self.agents_config['resume_editor'],
            tools=[],  # Opera sem ferramentas externas, utilizando apenas capacidades do LLM
            verbose=True,
            llm=LLM("gemini/gemini-1.5-flash", credentials=os.getenv('GOOGLE_API_KEY')),
            output_file='output/resume_editor.md'
        )

    @agent
    def reporting_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_agent'],
            verbose=True,
            llm=LLM("gemini/gemini-2.0-flash", credentials=os.getenv('GOOGLE_API_KEY')),
            output_file='output/reporting_agent.md'  # Armazena os dados processados neste arquivo

        )

    @task
    def extract_curriculum_data(self) -> Task:
        # Tarefa responsável pela extração estruturada de informações do currículo original
        return Task(
            config=self.tasks_config['extract_curriculum_data'],
            agent=self.curriculum_reader()  # Designada ao agente especializado em leitura de currículos
        )

    @task
    def css_analysis(self) -> Task:
        # Tarefa responsável por analisar o css do site. 
        return Task(
            config=self.tasks_config['css_analysis'],
            agent=self.css_analyzer() # Desiguina ao agente esppeciliasta em CSS
        )   

    @task
    def analyze_job_description(self) -> Task:
        # Tarefa para identificação de requisitos, habilidades e palavras-chave da vaga
        return Task(
            config=self.tasks_config['analyze_job_description'],
            agent=self.job_analyzer()  # Atribuída ao agente especializado em análise de vagas
        )

    @task
    def adjust_resume_for_job(self) -> Task:
        # Tarefa que adapta o currículo para maximizar compatibilidade com a vaga específica
        return Task(
            config=self.tasks_config['adjust_resume_for_job'],
            agent=self.resume_editor(),  # Executada pelo agente editor de currículos

        )


    @task
    def explain_curriculum_learning(self) -> Task:
        # Tarefa que documenta as alterações realizadas e justifica a estratégia de otimização
        return Task(
            config=self.tasks_config['explain_curriculum_learning'],
            agent=self.curriculum_reader()  # Utiliza o mesmo agente da leitura para explicações
        )

    @task
    def generate_report(self) -> Task:
        # Tarefa para gerar o relatório final da execução
        return Task(
            config=self.tasks_config['generate_report'],
            agent=self.reporting_agent() # Designada ao agente de relatórios
        )


    @crew
    def crew(self) -> Crew:
        # Define a equipe completa e seu fluxo de trabalho
        return Crew(
            agents=self.agents,  # Inclui todos os agentes especializados
            tasks=self.tasks,    # Incorpora todas as tarefas do processo
            process=Process.sequential,  # Estabelece execução sequencial para garantir dependência entre etapas
            verbose=True,  # Ativa logs completos para monitoramento e depuração
        )

# Expose a helper to create and return the configured crew for external use
def create_crew() -> Crew:
    return ResumeOptimizerCrew().crew()
