# Makefile para Resume Optimizer Crew

.PHONY: help install dev clean test run streamlit

help: ## Mostra esta mensagem de ajuda
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Instala as dependências do projeto
	uv sync

dev: ## Configura ambiente de desenvolvimento
	uv sync --dev
	cp .env.example .env
	@echo "⚠️  Configure suas chaves de API no arquivo .env"

clean-reports:
	@echo "🧹 Movendo reports do diretório raiz para reports/"
	@find . -maxdepth 1 -name "*_report.md" -exec mv {} reports/ \; 2>/dev/null || true
	@find . -maxdepth 1 -name "*_report.tex" -exec mv {} reports/ \; 2>/dev/null || true
	@find . -maxdepth 1 -name "execution_report*" -exec mv {} reports/ \; 2>/dev/null || true
	@find . -maxdepth 1 -name "generate_report*" -exec mv {} reports/ \; 2>/dev/null || true
	@echo "✅ Reports organizados!"

clean: clean-reports ## Remove arquivos temporários e cache
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf temp/*
	rm -rf .cache*/
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete

test: ## Executa os testes
	uv run python -m pytest tests/ -v

run: ## Executa o otimizador de currículo
	uv run python src/main.py

streamlit: ## Inicia a interface Streamlit
	uv run streamlit run scripts/streamlit_app.py

debug: ## Executa o debug do crew
	uv run python tests/debug_crew_execution.py

format: ## Formata o código com black
	uv run black src/ tests/ scripts/

lint: ## Verifica o código com flake8
	uv run flake8 src/ tests/ scripts/

check: format lint test ## Executa formatação, lint e testes

build: ## Prepara o projeto para distribuição
	uv build

docs: ## Gera documentação (se aplicável)
	@echo "Documentação disponível em docs/"

update: ## Atualiza dependências
	uv sync --upgrade

reset-db: ## Reseta o banco de dados de embeddings
	rm -rf db/
	mkdir -p db/

reset-output: ## Limpa arquivos de saída
	rm -rf output/*
	rm -rf reports/*

setup: dev ## Alias para dev
	@echo "✅ Ambiente configurado!"

check-organization: ## Verifica se o projeto está bem organizado
	uv run python scripts/check_setup.py

status: ## Mostra status geral do projeto
	@echo "📊 Status do Resume Optimizer Crew:"
	@echo ""
	@echo "📁 Estrutura de diretórios:"
	@ls -la | grep ^d | wc -l | xargs -I {} echo "   {} diretórios principais"
	@echo ""
	@echo "🐍 Arquivos Python:"
	@find . -name "*.py" -not -path "./.venv/*" | wc -l | xargs -I {} echo "   {} arquivos Python"
	@echo ""
	@echo "📄 Configurações:"
	@ls -la src/config/ 2>/dev/null | grep ".yaml" | wc -l | xargs -I {} echo "   {} arquivos YAML de configuração"
	@echo ""
	@echo "🔧 Para verificação completa, execute: make check-organization"
