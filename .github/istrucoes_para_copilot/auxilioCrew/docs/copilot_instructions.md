# 🤖 Instruções para GitHub Copilot: Agente Especialista em CrewAI

Estas instruções são para o GitHub Copilot aprender como colaborar neste projeto de forma **especializada no framework CrewAI**.

## 📚 Sobre o CrewAI

CrewAI permite orquestrar **agentes autônomos de IA** que interagem entre si com objetivos definidos, realizando tarefas complexas em equipe.

Cada agente:
- Tem um **papel** (`role`)
- Um **objetivo claro** (`goal`)
- Um **backstory** (história para guiar comportamento)
- E é **designado para uma ou mais tarefas**.

---

## 📁 Estrutura do Projeto (Contexto para o Copilot)

O projeto segue o padrão de projetos gerados com `crewai create nome_do_projeto`.

```bash
src/nome_do_projeto/
│
├── config/
│   ├── agents.yaml      # Definição dos agentes
│   └── tasks.yaml       # Definição das tarefas
│
├── crew.py              # Monta a equipe e organiza a execução
├── main.py              # Executa a crew com inputs
└── tools/
    └── custom_tool.py   # Ferramentas personalizadas com @tool
```

---

## 🧠 Como funcionam os agentes (agents.yaml)

Cada agente é definido no arquivo YAML com 3 elementos fundamentais:

```yaml
nome_do_agente:
  role: >
    [Papel do agente]
  goal: >
    [Objetivo claro]
  backstory: >
    [História e personalidade do agente]
```

✅ Copilot deve sugerir papéis especializados, metas claras e histórias que justifiquem as decisões do agente.

### Exemplo de Agente

```yaml
curador_de_conteudo:
  role: Especialista em curadoria de conteúdo educacional
  goal: Selecionar materiais de alta qualidade sobre IA na educação
  backstory: Com experiência em pedagogia e tecnologia, você cria trilhas de aprendizado impactantes.
```

---

## 📝 Como funcionam as tarefas (tasks.yaml)

Cada tarefa deve ter:

```yaml
nome_da_tarefa:
  description: >
    [Instrução detalhada do que o agente deve fazer]
  expected_output: >
    [Resultado final esperado da tarefa — o agente deve seguir à risca]
  agent: nome_do_agente
```

✅ Copilot deve sugerir tarefas com escopo claro, linguagem objetiva e resultados bem definidos.

### Exemplo de Tarefa

```yaml
selecionar_materiais:
  description: >
    Pesquise e selecione 5 artigos de alta qualidade sobre o uso de IA na educação básica.
  expected_output: >
    Lista com título, link e um parágrafo explicando o valor de cada artigo.
  agent: curador_de_conteudo
```

---

## 🧰 Como funcionam ferramentas (tools/custom_tool.py)

Ferramentas são funções Python decoradas com `@tool`, que fazem ações externas (ex: buscar dados).

```python
from crewai_tools import tool

@tool
def buscar_tendencias(query: str) -> str:
    """Busca tendências de mercado com base em uma palavra-chave."""
    # Lógica customizada aqui
    return f"Tendências encontradas para: {query}"
```

✅ Copilot pode sugerir novas ferramentas úteis para agentes que precisam interagir com dados externos.

---

## ⚙️ Como funciona a crew (crew.py)

A função `crew.py` define a orquestração:

```python
crew = Crew(
  agents=[pesquisador, escritor],
  tasks=[tarefa_pesquisa, tarefa_escrita],
  process=Process.sequential
)
```

- `Process.sequential` = tarefas em sequência
- `Process.parallel` = tarefas em paralelo

✅ Copilot deve sugerir a ordem correta com base nas dependências das tarefas.

---

## 🚀 Como iniciar (main.py)

Executa a crew passando variáveis de entrada:

```python
if __name__ == '__main__':
  result = crew.kickoff(inputs={"tema": "inteligência artificial na educação"})
  print(result)
```

✅ Copilot pode sugerir entradas e testes para diferentes temas.

---

## 🚨 Troubleshooting para Copilot

### Problemas Comuns e Soluções

| Sintoma              | Causa Provável           | Solução                          |
|----------------------|--------------------------|----------------------------------|
| Sugestões genéricas  | Contexto insuficiente    | Adicionar mais exemplos no código|
| Erro em YAML         | Indentação incorreta     | Validar estrutura do YAML        |
| Ferramenta ausente   | Importação faltando      | Garantir que `@tool` esteja decorado|

---

## 🧠 Dica final para o Copilot

Sempre proponha:

- Papéis especializados e bem definidos para os agentes
- Tarefas com escopos objetivos e resultados claros
- Sugestões de ferramentas se perceber necessidade de busca, análise ou integração externa
- Respeitar o fluxo de orquestração via `crew.py` e `main.py`

✨ Estas instruções garantem que Copilot atue como um membro útil da equipe, colaborando com a lógica do CrewAI com precisão.