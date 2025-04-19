# GitHub Copilot Instructions

This file consolidates instructions for GitHub Copilot regarding the **Resume Optimize Crew** project.

---
## 🤖 Instructions: `resume_optimizer_crew` Project (Updated)
---

**Summary:** This project uses the CrewAI framework to optimize a `.tex` resume based on a job description obtained from a URL. It reads the original resume, analyzes the job description, and adapts the text to highlight relevance for the opportunity.

### 📁 Project Structure

*   **`src/main.py`**: Entry point. Loads configurations, starts the `Crew`, and saves the result in `output/`.
*   **`src/crew.py`**: Defines the `Crew`, agents, and tasks (sequential process).
*   **`src/config/agents.yaml`**: Defines the agents (Reader, Analyzer, Editor).
*   **`src/config/tasks.yaml`**: Defines the tasks (Extract, Analyze, Adjust).
*   **`src/tools/latex_reader.py`**: `LatexReaderTool` tool for reading `.tex` files.
*   **`src/tools/scraping_tool.py`**: `WebScraperTool` tool for extracting content from URLs.
*   **`input/curriculo.tex`**: Location of the original `.tex` resume (example).
*   **`output/`**: Directory to save the optimized resume (`.tex`).
*   **`.env`**: File for environment variables (e.g., API keys).
*   **`pyproject.toml`**: Project metadata and dependencies (managed by `uv`).
*   **`requirements.txt`**: Dependencies (may be outdated; `pyproject.toml` is the primary source).

### 🧠 Agents (`src/config/agents.yaml`)

1.  **Resume Reader (`curriculum_reader`)**
    *   **`role`**: Resume Reader
    *   **`goal`**: Understand the full content of the `.tex` resume.
    *   **`backstory`**: Specialist in resume analysis and LaTeX.
    *   **`tool`**: `LatexReaderTool`

2.  **Job Analyzer (`job_analyzer`)**
    *   **`role`**: Job Analyzer
    *   **`goal`**: Extract the main requirements from the job description (via URL).
    *   **`backstory`**: Senior HR professional experienced in identifying job needs.
    *   **`tool`**: `WebScraperTool` (used by the `analyze_job_description` task)

3.  **Resume Editor (`resume_editor`)**
    *   **`role`**: Resume Editor
    *   **`goal`**: Adapt the resume to highlight alignment with the job.
    *   **`backstory`**: Experienced in custom resumes, focused on highlighting relevance without inventing information.

### 📝 Tasks (`src/config/tasks.yaml`)

1.  **Extract Resume Data (`extract_curriculum_data`)**
    *   **`description`**: Read the `.tex` file and extract experiences, skills, education.
    *   **`expected_output`**: Structured dictionary with the extracted data.
    *   **`agent`**: `curriculum_reader`

2.  **Analyze Job Description (`analyze_job_description`)**
    *   **`description`**: Read the job description (URL) and extract technical requirements, valued experiences, and keywords.
    *   **`expected_output`**: Bullet-point summary of what to emphasize in the resume.
    *   **`agent`**: `job_analyzer`

3.  **Adjust Resume for Job (`adjust_resume_for_job`)**
    *   **`description`**: Reorganize and rewrite parts of the `.tex` based on the resume data and job analysis. Do not add new experiences.
    *   **`expected_output`**: New `.tex` file with the modifications.
    *   **`agent`**: `resume_editor`
    *   **`context`**: Tasks `extract_curriculum_data` and `analyze_job_description`.

### 🧰 Tools (`src/tools/`)

*   **`LatexReaderTool` (`latex_reader.py`)**:
    *   **`@tool("LatexReaderTool")`**
    *   **`description`**: Extracts clean and structured text from a `.tex` file.
    *   **How it works**: Receives `file_path`, reads the `.tex` file, and uses `pylatexenc` to convert to text.
*   **`WebScraperTool` (`scraping_tool.py`)**:
    *   **`@tool("WebScraperTool")`**
    *   **`description`**: Reads the job description from a URL.
    *   **How it works**: Uses `ScrapeWebsiteTool` from `crewai-tools` to fetch content from the URL.

### ⚙️ Crew Flow (`src/crew.py`, `src/main.py`)

1.  **Configuration (`crew.py`)**: The `Crew` is instantiated with agents and tasks from the YAML files. The process is `Process.sequential`.
2.  **Execution (`main.py`)**:
    *   Loads environment variables (`.env`).
    *   Configures the LLM API (OpenAI/Gemini).
    *   Starts the `Crew` with `crew.kickoff(inputs={...})`.
        *   *Note:* Inputs (resume path, job URL) must be passed dynamically to `kickoff`. Ex: `inputs={'resume_path': 'input/curriculo.tex', 'job_url': 'https://...'}`. Adjust `main.py` and possibly tasks to receive these inputs.
    *   Prints the result (modified `.tex` content).
    *   Generates a filename with a timestamp.
    *   Saves the result in `output/`.
        *   *Note:* The saved content should be the `result` variable returned by `kickoff`, not a placeholder. Adjust `main.py` to save `result`.

### 🧩 Dependencies (`pyproject.toml`)

Main ones: `crewai`, `crewai-tools`, `python-dotenv`, `pylatexenc`, `beautifulsoup4`, `requests`. Managed with `uv`.

### ⚙️ Configuration (`.env`)

Requires API keys for the LLM (e.g., `GEMINI_API_KEY`) and optionally `GEMINI_API_BASE`, `GEMINI_MODEL_NAME`.

---
## 🤖 General and Copilot Instructions: CrewAI Framework
---

**Summary:** CrewAI ([Official Documentation](https://docs.crewai.com/)) orchestrates autonomous AI agents collaborating on tasks. This guide covers the main concepts and how Copilot should assist in development.

### 📚 Core CrewAI Concepts

*   **Agents:** Entities with `role`, `goal`, `backstory`, `tools`, and `memory`.
*   **Tasks:** Actions agents perform, defined by `description` and `expected_output`. Each task is assigned to an `agent`.
*   **Tools:** Python functions with the `@tool` decorator allowing agents to interact with the external world (APIs, files, etc.).
*   **Crew:** Orchestrates collaboration between agents to complete tasks. Defines the `process` (sequential, parallel, or hierarchical).

### 📁 Standard CrewAI Project Structure

```bash
src/project_name/
├── config/
│   ├── agents.yaml      # Agent definitions
│   └── tasks.yaml       # Task definitions
├── crew.py              # Assembles the Crew and organizes execution
├── main.py              # Entry point to run the Crew
└── tools/
    └── custom_tool.py   # Custom tools
```
*(Note: Structure may vary, but concepts remain the same).*

### 💡 How Copilot Should Help

*   **Agents:** Suggest specialized `role`s, clear `goal`s, and consistent `backstory`.
*   **Tasks:** Propose objective `description`s and well-defined `expected_output`.
*   **Tools:** Suggest useful `tool`s for external interactions and assist in implementation.
*   **Crew:** Suggest the correct task order (`Process.sequential`) or configurations for `Process.parallel` / `Process.hierarchical` when appropriate.
*   **Execution (`main.py`):** Assist in defining `inputs` for `kickoff` and writing basic tests.
*   **YAML:** Validate indentation and structure of `agents.yaml` and `tasks.yaml` files.
*   **Troubleshooting:**
    *   If suggestions are generic, ask for more context or examples.
    *   Check imports and correct usage of the `@tool` decorator if a tool is not found.
    *   For infinite loops, suggest `allow_delegation=False` or review task/agent logic.
    *   For inconsistent outputs, suggest adjustments to agent memory.
    *   For delegation errors, check if `process=Process.hierarchical` is configured in the Crew.

### ✨ Best Practices and Advanced Features

*   **Memory Management:** Set `memory=True` on the Agent to enable short-term memory.
*   **Parallel Execution:** Use `async_execution=True` in Tasks for asynchronous execution (requires `Process.parallel` in the Crew).
*   **Hierarchy:** Use `manager_llm` and `process=Process.hierarchical` in the Crew for complex flows with a manager agent.

---
## ⚡ Instructions: `uv` Package Manager
---

**Summary:** `uv` ([Official Documentation](https://astral.sh/uv)) is an extremely fast Python package and project manager, written in Rust. It replaces `pip`, `pip-tools`, `venv`, `pipx`, and more.

### Highlights

*   **Speed:** 10-100x faster than `pip` and `pip-tools`.
*   **All-in-one:** Replaces `pip`, `pip-tools`, `venv`, `virtualenv`, `pipx`.
*   **Advanced Resolution:** Supports lockfiles (`uv.lock`), workspaces.
*   **Python Management:** Installs and manages Python versions.

### Installation

**Standalone (macOS/Linux):**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
**Standalone (Windows):**
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
**Via PyPI (requires pip/pipx):**
```bash
pip install uv
# or
pipx install uv
```
**Update:**
```bash
uv self update
```

### Key Commands

*   **Project Management (`pyproject.toml`):**
    ```bash
    uv init          # Creates pyproject.toml (if it doesn't exist)
    uv add <package> # Adds dependency to pyproject.toml and installs
    uv remove <package> # Removes dependency from pyproject.toml and uninstalls
    uv sync          # Installs dependencies from uv.lock (or pyproject.toml)
    uv lock          # Generates/updates uv.lock from pyproject.toml
    uv run <command> # Runs command in the project's virtual environment
    ```
*   **Virtual Environments:**
    ```bash
    uv venv          # Creates or reuses .venv in the current directory
    # To activate: source .venv/bin/activate (Linux/macOS) or .venv\Scripts\activate (Windows)
    ```
*   **Python Management:**
    ```bash
    uv python install <version> # Installs specific Python version (e.g., 3.11)
    uv python pin <version>    # Pins the Python version for the current directory
    ```
*   **`pip` Interface (Compatibility):**
    ```bash
    uv pip install <package> [-r requirements.txt] [-e .]
    uv pip uninstall <package>
    uv pip freeze > requirements.txt
    uv pip compile requirements.in -o requirements.txt
    uv pip sync requirements.txt # Installs exact versions from requirements.txt
    ```
*   **Global CLI Tools (Isolated):**
    ```bash
    uv tool install <tool> # Installs CLI tool (like pipx)
    uv tool uninstall <tool>
    uv tool list           # Lists installed tools
    uvx <command> [args...] # Executes command in a temporary environment with packages
                            # Ex: uvx black --check .
    ```

---
# 🤖 Instructions for Updating Copilot's Internal Documentation
---

**Objective:** Keep this file (`.github/copilot-instructions.md`) updated with the latest versions and best practices of the technologies used in the project (CrewAI, `uv`, etc.).

**Priority:** **Checking and updating these instructions should be the first task when starting work in this workspace.**

## 🔄 Update Process (Workflow for Copilot)

1.  **Read Current Instructions:** Load the content of `.github/copilot-instructions.md`.
2.  **Identify Technologies:** List the libraries, frameworks, and tools mentioned (e.g., `crewai`, `uv`, `pylatexenc`, `crewai-tools`).
3.  **Search for Recent Documentation:** For each technology, use web search to find the official documentation, release notes, or latest changelogs.
    *   Queries: `"official documentation [name] python"`, `"latest release notes [name]"`, `"changelog [name]"`.
4.  **Compare and Identify Changes:** Compare the found documentation with the current instructions. Focus on:
    *   API changes (functions, classes, parameters).
    *   Deprecated features.
    *   New features or recommended approaches.
    *   Validity of code examples.
    *   Installation or configuration commands.
5.  **Apply Updates:** If discrepancies exist:
    *   Modify the relevant sections using `insert_edit_into_file`.
    *   Update text and code examples.
    *   Clearly indicate changes (e.g., "Updated to use `new_function()` from vX.Y").
    *   Maintain the original structure and purpose.
6.  **Document Updates (Optional):** Add a note at the end of the file about the date and versions checked.

## 🛠️ Tools to Use

*   `read_file`: Read the `.md` file.
*   `vscode-websearchforcopilot_webSearch`: Search for documentation.
*   `insert_edit_into_file`: Apply updates.

## 💡 Considerations

*   **Accuracy:** Base updates on official documentation.
*   **Clarity:** Keep instructions easy to understand.
*   **Context:** Do not add irrelevant information.
*   **Frequency:** Run periodically or when major updates are suspected.

---
## 🔄 Instructions: Automatic Commits (Suggestion)
---

**Objective:** Maintain a clear history of changes, especially those related to AI agents.

**When to Suggest Commit:** Copilot should *suggest* a commit (not make one automatically without confirmation) after applying significant code changes, especially to files related to CrewAI (`agents.yaml`, `tasks.yaml`, `crew.py`, `tools/`, `main.py`).

### 📝 Suggested Commit Message Format

1.  **Prefix:** Use a prefix indicating the main scope:
    *   `[CrewAI]` for changes in agents, tasks, or flow.
    *   `[Tool]` for adding or modifying tools.
    *   `[Config]` for `.yaml`, `.env`.
    *   `[Docs]` for `.md` files.
    *   `[Refactor]` for refactoring.
    *   `[Fix]` for bug fixes.
    *   `[Feat]` for new features.
2.  **Description:** Clear and concise message about the change.
    *   Ex: `[CrewAI] Add ResumeEditor agent`
    *   Ex: `[Tool] Implement LatexReaderTool to read .tex files`
    *   Ex: `[Fix] Correct input passing to crew.kickoff in main.py`
    *   Ex: `[Docs] Update Copilot instructions regarding UV`
3.  **Body (Optional):** Additional details, motivation, or impact.
    ```
    [CrewAI] Adjust analyze_job_description task

    - Improves keyword extraction from the job description.
    - Adds handling for invalid URLs in WebScraperTool.
    ```
4.  **Best Practices:**
    *   Use imperative mood (Ex: "Add", "Fix", "Update").
    *   Avoid generic messages ("update", "changes").
    *   One commit per logical change.

### 🚀 Suggestion Process

1.  **After Application:** After a Copilot suggestion is accepted and applied to the code.
2.  **Analysis:** Identify modified files and the nature of the change.
3.  **Suggestion:** Present a commit message suggestion in the format above for the user to review and confirm (via Git/SCM interface).

### 🔎 Additional Considerations

*   **Grouping:** If multiple related suggestions are accepted in sequence, suggest a single comprehensive commit.
*   **Review:** The user will always have the opportunity to review/edit the message before committing.

### Documenteatios of APIs
* **Linkedin** https://github.com/linkedin-developers/linkedin-api-python-client 
* **Linkedin** https://learn.microsoft.com/en-us/linkedin/
