# Resume Optimizer Crew

**Resumo**
O `Resume Optimizer Crew` é uma aplicação Python que utiliza o framework CrewAI para analisar e otimizar currículos em formato LaTeX (.tex) com base em uma descrição de vaga obtida via URL. O fluxo envolve três agentes (Leitor, Analista e Editor) orquestrados sequencialmente para ler o currículo original, extrair requisitos da vaga e reescrever o `.tex` destacando a relevância.

## Estrutura do Projeto

```
├── input/                   # Currículo original (.tex e arquivos auxiliares)
├── output/                  # Diretório para armazenar o currículo otimizado
├── src/
│   ├── main.py              # Ponto de entrada CLI
│   ├── crew.py              # Definição do Crew e tarefas
│   ├── config/
│   │   ├── agents.yaml      # Definição dos agentes
│   │   └── tasks.yaml       # Definição das tarefas
│   └── tools/
│       ├── latex_reader.py  # Ferramenta para ler e converter .tex
│       └── scraping_tool.py # Ferramenta para extrair descrição de vaga via URL
├── streamlit_app.py         # Interface web interativa (Streamlit)
├── .env                     # Variáveis de ambiente (chaves de API)
├── pyproject.toml           # Metadados e dependências (gerenciado por `uv`)
└── uv.lock                  # Lockfile de dependências
```

## Tecnologias e Dependências
- Python >= 3.12
- CrewAI (`crewai`, `crewai-tools`)
- `pylatexenc`, `beautifulsoup4`, `requests`
- Gerenciador de pacotes: `uv` (uv.lock)
- Streamlit para UI opcional

## Instalação

1. Clone este repositório:
   ```bash
   git clone <repo-url>
   cd resume-optimizer-crew
   ```
2. Instale e ative o ambiente:
   ```bash
   uv venv
   source .venv/bin/activate
   ```
3. Instale as dependências:
   ```bash
   uv sync
   ```
4. Crie um arquivo `.env` na raiz com suas chaves de API (por exemplo `GEMINI_API_KEY`).

## Uso

### Linha de Comando (CLI)
```bash
python src/main.py --job-url <URL_DA_VAGA> --input-dir input --output-dir output
```
- `--job-url`: URL da descrição da vaga.
- `--input-dir`: Diretório com o currículo `.tex` original.
- `--output-dir`: Diretório para salvar o currículo otimizado.

### Interface Web (Streamlit)
```bash
streamlit run streamlit_app.py
```
- Faça upload do seu `.tex` e informe a URL da vaga.
- Baixe o arquivo otimizado diretamente na web.

## Contribuição
Sinta-se à vontade para sugerir melhorias via issues ou pull requests.

## Licença
Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.
