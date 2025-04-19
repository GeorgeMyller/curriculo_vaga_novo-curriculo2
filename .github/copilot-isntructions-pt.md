# GitHub Copilot Instructions

Este arquivo consolida instruções para o GitHub Copilot sobre o projeto **Resume Optimize Crew**.

---
## 🤖 Instruções: Projeto `resume_optimizer_crew` (Atualizado)
---

**Resumo:** Este projeto usa o framework CrewAI para otimizar um currículo `.tex` com base na descrição de uma vaga obtida de uma URL. Ele lê o currículo, analisa a vaga e adapta o texto para destacar a relevância para a oportunidade.

### 📁 Estrutura do Projeto

*   **`src/main.py`**: Ponto de entrada. Carrega configurações, inicia a `Crew` e salva o resultado em `output/`.
*   **`src/crew.py`**: Define a `Crew`, agentes e tarefas (processo sequencial).
*   **`src/config/agents.yaml`**: Define os agentes (Leitor, Analista, Editor).
*   **`src/config/tasks.yaml`**: Define as tarefas (Extrair, Analisar, Ajustar).
*   **`src/tools/latex_reader.py`**: Ferramenta `LatexReaderTool` para ler `.tex`.
*   **`src/tools/scraping_tool.py`**: Ferramenta `WebScraperTool` para extrair conteúdo de URLs.
*   **`input/curriculo.tex`**: Local do currículo `.tex` original (exemplo).
*   **`output/`**: Diretório para salvar o currículo otimizado (`.tex`).
*   **`.env`**: Arquivo para variáveis de ambiente (ex: chaves de API).
*   **`pyproject.toml`**: Metadados do projeto e dependências (gerenciado por `uv`).
*   **`requirements.txt`**: Dependências (pode estar desatualizado; `pyproject.toml` é a fonte principal).

### 🧠 Agentes (`src/config/agents.yaml`)

1.  **Leitor de Currículo (`curriculum_reader`)**
    *   **`role`**: Leitor de Currículo
    *   **`goal`**: Entender o conteúdo completo do currículo `.tex`.
    *   **`backstory`**: Especialista em análise de currículos e LaTeX.
    *   **`tools`**: `LatexReaderTool`

2.  **Analista de Vaga (`job_analyzer`)**
    *   **`role`**: Analista de Vaga
    *   **`goal`**: Extrair os requisitos principais da vaga (via URL).
    *   **`backstory`**: Profissional de RH experiente em identificar necessidades de vagas.
    *   **`tools`**: `WebScraperTool` (usado pela tarefa `analyze_job_description`)

3.  **Editor de Currículo (`resume_editor`)**
    *   **`role`**: Editor de Currículo
    *   **`goal`**: Adaptar o currículo para destacar aderência à vaga.
    *   **`backstory`**: Experiente em currículos personalizados, focado em evidenciar o relevante sem inventar informações.

### 📝 Tarefas (`src/config/tasks.yaml`)

1.  **Extrair Dados do Currículo (`extract_curriculum_data`)**
    *   **`description`**: Ler o `.tex` e extrair experiências, habilidades, formação.
    *   **`expected_output`**: Dicionário estruturado com os dados extraídos.
    *   **`agent`**: `curriculum_reader`

2.  **Analisar Descrição da Vaga (`analyze_job_description`)**
    *   **`description`**: Ler a descrição da vaga (URL) e extrair requisitos técnicos, experiências e palavras-chave.
    *   **`expected_output`**: Resumo em bullet points do que destacar no currículo.
    *   **`agent`**: `job_analyzer`

3.  **Ajustar Currículo para Vaga (`adjust_resume_for_job`)**
    *   **`description`**: Reorganizar e reescrever partes do `.tex` com base nos dados do currículo e análise da vaga. Não adicionar novas experiências.
    *   **`expected_output`**: Novo arquivo `.tex` com as modificações.
    *   **`agent`**: `resume_editor`
    *   **`context`**: Tarefas `extract_curriculum_data` e `analyze_job_description`.

### 🧰 Ferramentas (`src/tools/`)

*   **`LatexReaderTool` (`latex_reader.py`)**:
    *   **`@tool("LatexReaderTool")`**
    *   **`description`**: Extrai texto limpo e estruturado de um arquivo `.tex`.
    *   **Funcionamento**: Recebe `file_path`, lê o `.tex` e usa `pylatexenc` para converter em texto.
*   **`WebScraperTool` (`scraping_tool.py`)**:
    *   **`@tool("WebScraperTool")`**
    *   **`description`**: Lê a descrição da vaga de uma URL.
    *   **Funcionamento**: Usa `ScrapeWebsiteTool` da `crewai-tools` para buscar conteúdo da URL.

### ⚙️ Fluxo da Crew (`src/crew.py`, `src/main.py`)

1.  **Configuração (`crew.py`)**: A `Crew` é instanciada com agentes e tarefas dos arquivos YAML. O processo é `Process.sequential`.
2.  **Execução (`main.py`)**:
    *   Carrega variáveis de ambiente (`.env`).
    *   Configura a API do LLM (OpenAI/Gemini).
    *   Inicia a `Crew` com `crew.kickoff(inputs={...})`.
        *   *Nota:* Os inputs (caminho do currículo, URL da vaga) devem ser passados dinamicamente para `kickoff`. Ex: `inputs={'resume_path': 'input/curriculo.tex', 'job_url': 'https://...'}`. Ajustar `main.py` e possivelmente as tarefas para receberem esses inputs.
    *   Imprime o resultado (conteúdo `.tex` modificado).
    *   Gera nome de arquivo com timestamp.
    *   Salva o resultado em `output/`.
        *   *Nota:* O conteúdo salvo deve ser a variável `result` retornada por `kickoff`, não um placeholder. Ajustar `main.py` para salvar `result`.

### 🧩 Dependências (`pyproject.toml`)

Principais: `crewai`, `crewai-tools`, `python-dotenv`, `pylatexenc`, `beautifulsoup4`, `requests`. Gerenciadas com `uv`.

### ⚙️ Configuração (`.env`)

Requer chaves de API para o LLM (ex: `GEMINI_API_KEY`) e opcionalmente `GEMINI_API_BASE`, `GEMINI_MODEL_NAME`.

---
## 🤖 Instruções Gerais e para Copilot: Framework CrewAI
---

**Resumo:** CrewAI ([Documentação Oficial](https://docs.crewai.com/)) orquestra agentes autônomos de IA que colaboram em tarefas. Este guia cobre os conceitos principais e como o Copilot deve auxiliar no desenvolvimento.

### 📚 Conceitos Fundamentais do CrewAI

*   **Agentes:** Entidades com `role` (papel), `goal` (objetivo), `backstory` (contexto), `tools` (ferramentas) e `memory` (memória).
*   **Tarefas (`Tasks`):** Ações que os agentes executam, definidas por `description` (descrição) e `expected_output` (resultado esperado). Cada tarefa é atribuída a um `agent`.
*   **Ferramentas (`Tools`):** Funções Python com decorador `@tool` que permitem aos agentes interagir com o mundo externo (APIs, arquivos, etc.).
*   **Crew:** Orquestra a colaboração entre agentes para completar as tarefas. Define o `process` (sequencial, paralelo ou hierárquico).

### 📁 Estrutura Padrão de Projeto CrewAI

```bash
src/nome_do_projeto/
├── config/
│   ├── agents.yaml      # Definição dos agentes
│   └── tasks.yaml       # Definição das tarefas
├── crew.py              # Monta a Crew e organiza a execução
├── main.py              # Ponto de entrada para executar a Crew
└── tools/
    └── custom_tool.py   # Ferramentas personalizadas
```
*(Nota: A estrutura pode variar, mas os conceitos são os mesmos).*

### 💡 Como o Copilot Deve Ajudar

*   **Agentes:** Sugerir `role`s especializados, `goal`s claros e `backstory` consistentes.
*   **Tarefas:** Propor `description`s objetivas e `expected_output` bem definidos.
*   **Ferramentas:** Sugerir `tool`s úteis para interações externas e auxiliar na implementação.
*   **Crew:** Sugerir a ordem correta das tarefas (`Process.sequential`) ou configurações para `Process.parallel` / `Process.hierarchical` quando apropriado.
*   **Execução (`main.py`):** Auxiliar na definição dos `inputs` para `kickoff` e na escrita de testes básicos.
*   **YAML:** Validar a indentação e estrutura dos arquivos `agents.yaml` e `tasks.yaml`.
*   **Troubleshooting:**
    *   Se as sugestões forem genéricas, pedir mais contexto ou exemplos.
    *   Verificar importações e uso correto do decorador `@tool` se uma ferramenta não for encontrada.
    *   Para loops infinitos, sugerir `allow_delegation=False` ou revisar a lógica da tarefa/agente.
    *   Para outputs inconsistentes, sugerir ajustes na memória do agente.
    *   Para erros de delegação, verificar se `process=Process.hierarchical` está configurado na Crew.

### ✨ Melhores Práticas e Recursos Avançados

*   **Gerenciamento de Memória:** Configurar `memory=True` no Agente para habilitar memória de curto prazo.
*   **Execução Paralela:** Usar `async_execution=True` nas Tarefas para execução assíncrona (requer `Process.parallel` na Crew).
*   **Hierarquia:** Usar `manager_llm` e `process=Process.hierarchical` na Crew para fluxos complexos com um agente gerente.

---
## ⚡ Instruções: Gerenciador de Pacotes `uv`
---

**Resumo:** `uv` ([Documentação Oficial](https://astral.sh/uv)) é um gerenciador de pacotes e projetos Python extremamente rápido, escrito em Rust. Ele substitui `pip`, `pip-tools`, `venv`, `pipx` e mais.

### Destaques

*   **Velocidade:** 10-100x mais rápido que `pip` e `pip-tools`.
*   **Tudo-em-um:** Substitui `pip`, `pip-tools`, `venv`, `virtualenv`, `pipx`.
*   **Resolução Avançada:** Suporte a lockfiles (`uv.lock`), workspaces.
*   **Gerenciamento Python:** Instala e gerencia versões do Python.

### Instalação

**Standalone (macOS/Linux):**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
**Standalone (Windows):**
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
**Via PyPI (requer pip/pipx):**
```bash
pip install uv
# ou
pipx install uv
```
**Atualizar:**
```bash
uv self update
```

### Comandos Principais

*   **Gerenciamento de Projetos (`pyproject.toml`):**
    ```bash
    uv init          # Cria pyproject.toml (se não existir)
    uv add <pacote>  # Adiciona dependência ao pyproject.toml e instala
    uv remove <pacote> # Remove dependência do pyproject.toml e desinstala
    uv sync          # Instala dependências do uv.lock (ou pyproject.toml)
    uv lock          # Gera/atualiza uv.lock a partir de pyproject.toml
    uv run <comando> # Executa comando no ambiente virtual do projeto
    ```
*   **Ambientes Virtuais:**
    ```bash
    uv venv          # Cria ou reutiliza .venv no diretório atual
    # Para ativar: source .venv/bin/activate (Linux/macOS) ou .venv\Scripts\activate (Windows)
    ```
*   **Gerenciamento de Python:**
    ```bash
    uv python install <versao> # Instala versão específica do Python (ex: 3.11)
    uv python pin <versao>    # Fixa a versão do Python para o diretório atual
    ```
*   **Interface `pip` (Compatibilidade):**
    ```bash
    uv pip install <pacote> [-r requirements.txt] [-e .]
    uv pip uninstall <pacote>
    uv pip freeze > requirements.txt
    uv pip compile requirements.in -o requirements.txt
    uv pip sync requirements.txt # Instala exatamente as versões do requirements.txt
    ```
*   **Ferramentas CLI Globais (Isoladas):**
    ```bash
    uv tool install <ferramenta> # Instala ferramenta CLI (como pipx)
    uv tool uninstall <ferramenta>
    uv tool list                 # Lista ferramentas instaladas
    uvx <comando> [args...]     # Executa comando em ambiente temporário com pacotes
                                # Ex: uvx black --check .
    ```

---
# 🤖 Instruções para Atualização da Documentação Interna do Copilot
---

**Objetivo:** Manter este arquivo (`.github/copilot-instructions.md`) atualizado com as versões e práticas mais recentes das tecnologias usadas no projeto (CrewAI, `uv`, etc.).

**Prioridade:** **Verificar e atualizar estas instruções deve ser a primeira tarefa ao iniciar o trabalho neste workspace.**

## 🔄 Processo de Atualização (Workflow para Copilot)

1.  **Ler Instruções Atuais:** Carregue o conteúdo de `.github/copilot-instructions.md`.
2.  **Identificar Tecnologias:** Liste as bibliotecas, frameworks e ferramentas mencionadas (ex: `crewai`, `uv`, `pylatexenc`, `crewai-tools`).
3.  **Pesquisar Documentação Recente:** Para cada tecnologia, use a busca na web para encontrar a documentação oficial, notas de lançamento ou changelogs mais recentes.
    *   Consultas: `"documentação oficial [nome] python"`, `"latest release notes [nome]"`, `"changelog [nome]"`.
4.  **Comparar e Identificar Mudanças:** Compare a documentação encontrada com as instruções atuais. Foque em:
    *   Mudanças na API (funções, classes, parâmetros).
    *   Funcionalidades obsoletas (deprecated).
    *   Novas funcionalidades ou abordagens recomendadas.
    *   Validade dos exemplos de código.
    *   Comandos de instalação ou configuração.
5.  **Aplicar Atualizações:** Se houver discrepâncias:
    *   Modifique as seções relevantes usando `insert_edit_into_file`.
    *   Atualize textos e exemplos de código.
    *   Indique claramente as mudanças (ex: "Atualizado para usar `nova_funcao()` da vX.Y").
    *   Mantenha a estrutura e o propósito originais.
6.  **Documentar Atualizações (Opcional):** Adicione uma nota no final do arquivo sobre a data e versões verificadas.

## 🛠️ Ferramentas a Utilizar

*   `read_file`: Ler o arquivo `.md`.
*   `vscode-websearchforcopilot_webSearch`: Pesquisar documentação.
*   `insert_edit_into_file`: Aplicar as atualizações.

## 💡 Considerações

*   **Precisão:** Baseie as atualizações na documentação oficial.
*   **Clareza:** Mantenha as instruções fáceis de entender.
*   **Contexto:** Não adicione informações irrelevantes.
*   **Frequência:** Execute periodicamente ou quando houver suspeita de atualizações importantes.

---
## 🔄 Instruções: Commits Automáticos (Sugestão)
---

**Objetivo:** Manter um histórico claro das alterações, especialmente aquelas relacionadas aos agentes de IA.

**Quando Sugerir Commit:** O Copilot deve *sugerir* um commit (não fazer automaticamente sem confirmação) após aplicar alterações significativas no código, especialmente nos arquivos relacionados ao CrewAI (`agents.yaml`, `tasks.yaml`, `crew.py`, `tools/`, `main.py`).

### 📝 Formato Sugerido para Mensagem de Commit

1.  **Prefixo:** Use um prefixo indicando o escopo principal:
    *   `[CrewAI]` para mudanças nos agentes, tarefas ou fluxo.
    *   `[Tool]` para adição ou modificação de ferramentas.
    *   `[Config]` para `.yaml`, `.env`.
    *   `[Docs]` para arquivos `.md`.
    *   `[Refactor]` para refatorações.
    *   `[Fix]` para correções de bugs.
    *   `[Feat]` para novas funcionalidades.
2.  **Descrição:** Mensagem clara e objetiva sobre a mudança.
    *   Ex: `[CrewAI] Adiciona agente EditorDeCurriculo`
    *   Ex: `[Tool] Implementa LatexReaderTool para ler arquivos .tex`
    *   Ex: `[Fix] Corrige passagem de inputs para crew.kickoff em main.py`
    *   Ex: `[Docs] Atualiza instruções do Copilot sobre UV`
3.  **Corpo (Opcional):** Detalhes adicionais, motivação ou impacto.
    ```
    [CrewAI] Ajusta tarefa analyze_job_description

    - Melhora a extração de palavras-chave da descrição da vaga.
    - Adiciona tratamento para URLs inválidas na WebScraperTool.
    ```
4.  **Boas Práticas:**
    *   Mensagens no imperativo (Ex: "Adiciona", "Corrige", "Atualiza").
    *   Evitar mensagens genéricas ("update", "changes").
    *   Um commit por mudança lógica.

### 🚀 Processo de Sugestão

1.  **Após Aplicação:** Depois que uma sugestão do Copilot for aceita e aplicada ao código.
2.  **Análise:** Identificar os arquivos modificados e a natureza da mudança.
3.  **Sugestão:** Apresentar uma sugestão de mensagem de commit no formato acima para o usuário revisar e confirmar (via interface do Git/SCM).

### 🔎 Considerações Adicionais

*   **Agrupamento:** Se múltiplas sugestões relacionadas forem aceitas em sequência, sugerir um único commit abrangente.
*   **Revisão:** O usuário sempre terá a oportunidade de revisar/editar a mensagem antes de commitar.