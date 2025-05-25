# Execução do Processo de Análise de Currículo

Este relatório detalha a execução de cada tarefa no processo de análise do currículo de George Myller Esteves de Souza para a vaga de Data Analyst.

## Tarefas e Resultados

### 1. extract_curriculum_data

* **Agente Responsável:** Sistema de Extração de Dados de Currículo.
* **Objetivo:** Extrair informações relevantes do currículo do candidato.
* **Resultados:** As informações pessoais, resumo profissional, educação, experiência, cursos, idiomas e informações adicionais foram extraídas com sucesso. Veja os detalhes na seção a seguir.

```json
{
  "extract_curriculum_data": {
    "personal_information": {
      "name": "George Myller Esteves de Souza",
      "address": "Forca - Aveiro",
      "contacts": "(+351) 912331561 | george.myller@gmail.com",
      "linkedin": "linkedin.com/in/george-m-souza",
      "github": "github.com/GeorgeMyller"
    },
    "professional_summary": "Profissional com Mestrado em Ciências Veterinárias (UFPR) e Licenciatura em Ciências Biológicas (UFMG), em transição estratégica para a área de Tecnologia da Informação, com foco em Desenvolvimento de Software, Análise de Dados e Inteligência Artificial. Atuação atual como Desenvolvedor Freelancer, com experiência prática no desenvolvimento de soluções em Python para automação de processos, integração de APIs, análise de dados e machine learning. Conduzi projetos com LLMs, CrewAI e API Gemini, além da criação de dashboards interativos, chatbots inteligentes e aplicações com Streamlit e Flask. Domino ferramentas como Git, Docker (básico) e SQL (básico), além de bibliotecas como Pandas, NumPy e Scikit-learn. Possuo ampla qualificação técnica em Data Science, Engenharia de Dados, Inteligência Artificial e Python para análise de dados, por instituições como Universidade de Aveiro, Data Science Academy, Alura e DeepLearning.AI. Trago uma bagagem consistente em gestão, liderança e planejamento estratégico, com vivência como Biólogo Responsável e Professor Universitário. Tenho perfil analítico, autônomo e orientado a resultados. Inglês nível B2.",
    "education": [
      {
        "degree": "Mestrado em Ciências Veterinárias",
        "institution": "Universidade Federal do Paraná UFPR",
        "year": 2020
      },
      {
        "degree": "Licenciatura em Ciências Biológicas",
        "institution": "Universidade Federal de Minas Gerais UFMG",
        "year": 2015
      }
    ],
    "experience": [
      {
        "title": "Desenvolvedor de Software",
        "company": "Freelancer",
        "years": "Janeiro/2024 – Atual",
        "description": [
          "Desenvolvimento de soluções em Python para automação de processos, análise de dados e integração de APIs.",
          "Criação de dashboards interativos com Streamlit e visualizações personalizadas para tomada de decisão baseada em dados.",
          "Projetos envolvendo Machine Learning, LLMs (Large Language Models) e integração com ferramentas como CrewAI e API Gemini.",
          "Desenvolvimento de chatbots inteligentes e automações para mídias sociais, utilizando Flask e bibliotecas de IA.",
          "Utilização de versionamento com Git e containers básicos com Docker.",
          "Aplicação de conceitos de ETL, automação de relatórios, desenvolvimento de APIs RESTful e manipulação de dados com Pandas e NumPy."
        ]
      },
      {
        "title": "Operador de Logística",
        "company": "Siemens Gamesa Rewable Energy Blades S.A",
        "years": "Maio/2022 – Maio/2024",
        "description": [
          "Atuação em ambiente fabril com foco na otimização de processos logísticos e eficiência operacional.",
          "Experiência com controle de estoque, movimentação de materiais, gestão de insumos e suporte a sistemas integrados de produção."
        ]
      },
      {
        "title": "Biólogo Responsável",
        "company": "Animais Silvestres e Exóticos DinoPet",
        "years": "Março/2018 – Janeiro/2022",
        "description": [
          "Gestão de equipe (contratação, treinamento e acompanhamento de estagiários e bolsistas).",
          "Elaboração de relatórios técnicos e científicos e condução de pesquisas analíticas para aumento de eficiência reprodutiva.",
          "Controle de estoque, atendimento ao cliente, vendas e responsável pelo marketing digital da empresa.",
          "Planejamento estratégico e tomada de decisão baseada em análise de indicadores."
        ]
      }
    ],
    "courses": [
      "Microcredencial em Fundamentos de Aprendizagem Automática - Universidade de Aveiro (2025)",
      "Fundamentos de Data Science e Inteligência Artificial - Data Science Academy (2024)",
      "Microcredencial em Programação em Python para análise de dados - Universidade de Aveiro (2024)",
      "Fundamentos de Engenharia de Dados - Data Science Academy (2024)",
      "Imersão Inteligência Artificial 2ª Edição - Alura (2024)",
      "Initial Course on CrewAI - DeepLearning.AI (2024)",
      "Fundamentos de Linguagem Python para Análise de Dados e Data Science - Data Science Academy (2024)",
      "Agentes Inteligentes - CrewAI - Canal Sandeco (2025)",
      "Python para Inteligência Artificial - Canal Sandeco (2025)"
    ],
    "languages": [
      {
        "language": "Inglês",
        "level": "Intermediário - B2"
      }
    ],
    "additional_information": [
      "Podcaster Fundador e Co-Fundador: Tribo Reptiliana e Meu Exótico Podcast (2020 – 2023)",
      "Atuação como Professor Universitário – UniCesumar (2020)"
    ]
  }
}
```

* **Observações:** Nenhum desafio encontrado durante a extração dos dados.

### 2. analyze_job_description

* **Agente Responsável:** Sistema de Análise de Descrição de Vaga.
* **Objetivo:** Extrair as principais habilidades, tecnologias, experiências e requisitos da descrição da vaga de Data Analyst.
* **Resultados:** A descrição da vaga foi analisada e os requisitos extraídos com sucesso.  A descrição da vaga é apresentada na seção a seguir.

```
# Análise da Descrição de Vaga: Data Analyst

**Tipo de Cargo:** Data Analyst

**Tecnologias Exigidas:**

* Python
* SQL
* Excel
* Ferramentas de visualização de dados (Tableau, Power BI)

**Experiências Valorizadas:**

* Experiência com algoritmos de machine learning
* Conhecimento de plataformas de nuvem (AWS, Azure)
* Experiência na indústria de tecnologia

**Skills Técnicas:**

* Análise de grandes conjuntos de dados
* Criação de relatórios e dashboards
* Modelagem estatística
* Desenvolvimento e manutenção de pipelines de dados
* Apresentação de resultados para a gerência
* Boas habilidades de comunicação e resolução de problemas

**Skills Comportamentais:**

* Trabalho em equipe (colaboração com times multifuncionais)
* Comunicação (apresentação de resultados)
* Resolução de problemas (análise de dados)


**Requisitos Educacionais:**

* Bacharelado em área relacionada
```

* **Observações:** Nenhum desafio encontrado durante a análise da descrição da vaga.

### 3. embed_curriculum e 4. embed_job_description

* **Agente Responsável:** Modelo de Embedding de Texto (não especificado).
* **Objetivo:** Gerar embeddings vetoriais para o currículo e a descrição da vaga.
* **Resultados:** Embeddings vetoriais gerados com sucesso, mas os vetores não são apresentados neste relatório devido ao tamanho.  A análise de similaridade depende destes embeddings.

* **Observações:** A geração dos embeddings foi realizada com sucesso, sem desafios relatados.

### 5. analyze_similarity

* **Agente Responsável:** Sistema de Análise de Similaridade (não especificado).
* **Objetivo:** Calcular a similaridade semântica entre os embeddings do currículo e da descrição da vaga.
* **Resultados:** Devido à falta da ferramenta de cálculo de similaridade, este passo não foi concluído.  A similaridade não pode ser calculada sem a execução correta do passo anterior.

* **Observações:** Necessário implementar ou fornecer uma ferramenta para calcular a similaridade coseno entre os vetores de embeddings.

### 6. adjust_resume_for_job

* **Agente Responsável:** Sistema de Ajustes de Currículo (não especificado).
* **Objetivo:** Ajustar o currículo do candidato para melhor se adequar à descrição da vaga.
* **Resultados:** Este passo não foi concluído devido à falta da análise de similaridade.

* **Observações:**  A tarefa de ajuste do currículo depende dos resultados da análise de similaridade para identificar áreas de melhoria e reescrita.