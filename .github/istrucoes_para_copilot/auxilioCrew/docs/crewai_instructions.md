# 🤖 Manual de Instruções para Pair Programmers no Projeto CrewAI

Este manual foi projetado para guiar pair programmers no uso do framework CrewAI, fornecendo instruções detalhadas para criar, configurar e executar equipes de agentes de IA colaborativos. O objetivo é garantir que todos os membros da equipe possam contribuir de forma eficiente e consistente.

---

## 🧠 O que é o CrewAI?

O CrewAI permite que você crie **agentes com papéis e backstories**, que se comunicam e resolvem tarefas em conjunto. É ideal para simular equipes de trabalho automatizadas. Cada agente possui:

- **Role**: Especialização principal (ex.: Analista de Mercado)
- **Goal**: Objetivo claro e mensurável
- **Backstory**: Contexto que guia o comportamento do agente
- **Tools**: Ferramentas específicas para execução de tarefas
- **Memory**: Capacidade de reter contexto

---

## 📁 Estrutura do Projeto

```bash
.
├── README.md                  # Este arquivo
├── pyproject.toml             # Dependências e configuração do projeto
└── src/
    └── nome_do_projeto/
        ├── config/
        │   ├── agents.yaml    # Definição dos agentes
        │   └── tasks.yaml     # Definição das tarefas
        ├── crew.py            # Montagem da crew (orquestração)
        ├── main.py            # Execução principal do projeto
        └── tools/
            └── custom_tool.py # Ferramentas personalizadas (se necessário)
```

---

## ⚙️ Configurando Agentes (agents.yaml)

Os agentes são definidos no arquivo `agents.yaml`. Cada agente deve conter:

- **role**: Papel do agente
- **goal**: Objetivo principal
- **backstory**: Contexto e motivação

### Exemplo:

```yaml
pesquisador:
  role: >
    Especialista em Análise de Mercado
  goal: >
    Descobrir tendências emergentes no setor de energia renovável
  backstory: >
    Você é um analista renomado, com anos de experiência identificando oportunidades inovadoras e disruptivas em mercados sustentáveis.
```

---

## 📌 Configurando Tarefas (tasks.yaml)

As tarefas são definidas no arquivo `tasks.yaml`. Cada tarefa deve conter:

- **description**: Descrição detalhada do objetivo
- **expected_output**: Resultado esperado
- **agent**: Agente responsável pela tarefa

### Exemplo:

```yaml
pesquisar_tendencias_renovaveis:
  description: >
    Pesquise as 5 principais tendências emergentes no setor de energia renovável para os próximos 5 anos.
    Utilize fontes confiáveis e dados atualizados.

  expected_output: >
    Uma lista com 5 tendências, cada uma com descrição e fontes utilizadas.

  agent: pesquisador
```

---

## 🛠️ Criando Ferramentas Customizadas

Ferramentas são funções Python decoradas com `@tool`, que permitem que os agentes executem ações específicas, como buscar dados externos ou realizar análises.

### Exemplo:

```python
from crewai_tools import tool

@tool
def buscar_dados_startups(query: str) -> str:
    """Busca informações financeiras de startups baseado na query."""
    # Aqui você pode chamar uma API, banco de dados, etc.
    return "Resultados simulados para: " + query
```

---

## 🚀 Executando o Projeto

1. **Instale as dependências:**

```bash
pip install -e .
```

2. **Configure as variáveis de ambiente:**

```bash
export OPENAI_API_KEY="sua-chave"
export SERPER_API_KEY="sua-chave"  # se usar ferramentas de busca
```

3. **Execute o projeto:**

```bash
python src/nome_do_projeto/main.py
```

---

## 💡 Dicas para Pair Programmers

1. **Comente suas intenções:**
   - Use comentários claros para descrever o que cada trecho de código deve fazer.
   - Exemplo:
     ```python
     # Criar um novo agente com foco em análise financeira de startups
     ```

2. **Use YAML bem descritivo:**
   - Exemplo:
     ```yaml
     investidor:
       role: Analista de Investimentos
       goal: Avaliar startups com potencial de alto crescimento
       backstory: Você trabalha em um fundo de VC e busca os próximos unicórnios.
     ```

3. **Deixe TODOs para guiar o desenvolvimento:**
   - Exemplo:
     ```python
     # TODO: Criar função que extrai palavras-chave do resultado da pesquisa
     ```

---

## ✨ Futuras Expansões

- Integração com APIs externas (Crunchbase, PitchBook, etc.)
- Dashboards com Streamlit ou Gradio
- Exportação automática de relatórios

---

## 🛠️ Melhorias no Fluxo de Trabalho do CrewAI

### Estratégias de Otimização

1. **Gerenciamento de Memória:**
   - Configure a retenção de memória dos agentes para evitar perda de contexto.
   - Exemplo:
     ```python
     Agent(
         memory_retention=0.8,  # 0-1 (intensidade de memória)
         memory_window=3  # Número de interações retidas
     )
     ```

2. **Execução Paralela:**
   - Utilize `async_execution` para tarefas que podem ser realizadas simultaneamente.
   - Exemplo:
     ```python
     task1.async_execution = True
     task2.async_execution = True
     ```

3. **Hierarquia de Processos:**
   - Para fluxos complexos, use `Process.hierarchical`.
   - Exemplo:
     ```python
     Crew(
         process=Process.hierarchical,
         max_iterations=15  # Prevenir loops
     )
     ```

---

## 🧪 Exemplos Reais de Agentes e Tarefas

### Exemplo de Agente

```yaml
curador_de_conteudo:
  role: Especialista em curadoria de conteúdo educacional
  goal: Selecionar materiais de alta qualidade sobre IA na educação
  backstory: Com experiência em pedagogia e tecnologia, você cria trilhas de aprendizado impactantes.
```

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

## 🔧 Ferramentas Customizadas

### Template de Ferramenta

Ferramentas são funções Python decoradas com `@tool`, que fazem ações externas (ex: buscar dados).

```python
from crewai_tools import tool

@tool
def buscar_tendencias(query: str) -> str:
    """Busca tendências de mercado com base em uma palavra-chave."""
    # Lógica customizada aqui
    return f"Tendências encontradas para: {query}"
```

---

## 🚨 Troubleshooting

### Problemas Comuns e Soluções

| Sintoma              | Causa Provável           | Solução                          |
|----------------------|--------------------------|----------------------------------|
| Loop infinito        | Delegação circular       | `allow_delegation=False`        |
| Output inconsistente | Memória insuficiente     | Aumentar `memory_retention`     |
| Erro de delegação    | Hierarquia indefinida    | Definir `process=Process.hierarchical` |
| Perda de contexto    | Janela de memória pequena| Ajustar `memory_window`         |

---

Este manual foi projetado para garantir que pair programmers possam colaborar de forma eficiente e consistente no desenvolvimento do projeto CrewAI.
