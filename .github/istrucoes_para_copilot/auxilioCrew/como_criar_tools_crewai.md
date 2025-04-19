# Guia Prático: Como Criar e Integrar Tools Customizadas no CrewAI

Este guia apresenta um passo a passo para criar, melhorar e integrar ferramentas (tools) customizadas no padrão CrewAI, facilitando a automação de tarefas especializadas por agentes.

---

## 1. Estrutura Recomendada

```
src/
  tools/
    minha_tool.py
  config/
    agents.yaml
    tasks.yaml
  crew.py
  main.py
```

---

## 2. Criando uma Tool Customizada

1. **Crie o arquivo da tool:**
   - Exemplo: `src/tools/minha_tool.py`

2. **Implemente a função da tool:**
   - Use o decorador `@tool("NomeDaTool")` do CrewAI.
   - Defina uma descrição clara.
   - Receba parâmetros via argumentos da função.

```python
from crewai_tools import tool

@tool("MinhaTool")
def minha_tool(file_path: str) -> str:
    """Lê um arquivo e retorna seu conteúdo."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()
```

3. **(Opcional) Crie uma classe Tool:**
   - Para lógica mais complexa, use classes e métodos.

---

## 3. Registrando a Tool

- Certifique-se de importar sua tool no arquivo `src/crew.py`:

```python
from tools.minha_tool import MinhaTool
```

- Isso garante que o CrewAI reconheça e registre a tool.

---

## 4. Integrando a Tool ao Agente

1. **No arquivo de configuração do agente (`agents.yaml`):**
   - Adicione o nome da tool na lista de tools do agente.

```yaml
curriculum_reader:
  role: Resume Reader
  goal: Ler e entender o currículo em .tex
  tools:
    - MinhaTool
```

2. **No código do agente (`crew.py`):**
   - Adicione a tool na lista de tools do agente:

```python
from tools.minha_tool import MinhaTool
# ...
Agent(
    # ...
    tools=[MinhaTool()],
    # ...
)
```

---

## 5. Testando a Tool

- Execute o fluxo principal (`main.py`) e verifique se o agente utiliza a tool corretamente.
- Adicione prints ou logs para depuração.

---

## 6. Dicas e Boas Práticas

- Use nomes descritivos para suas tools.
- Documente a função e os parâmetros.
- Prefira funções puras e sem efeitos colaterais.
- Importe todas as tools customizadas em `crew.py` para evitar erros de registro.
- Consulte a [documentação oficial CrewAI](https://docs.crewai.com/) para exemplos avançados.

---

## 7. Exemplo de Tool Completa

```python
from crewai_tools import tool

@tool("LatexReaderTool")
def latex_reader_tool(file_path: str) -> str:
    """Extrai texto limpo de um arquivo .tex usando pylatexenc."""
    from pylatexenc.latex2text import LatexNodes2Text
    with open(file_path, 'r', encoding='utf-8') as f:
        tex = f.read()
    return LatexNodes2Text().latex_to_text(tex)
```

---

## 8. Integração Final

- Certifique-se de que o nome da tool no decorador `@tool` e no `agents.yaml` seja idêntico.
- Importe todas as tools customizadas no início de `crew.py`.
- Teste o fluxo completo para garantir que os agentes utilizam as tools corretamente.

---

Pronto! Agora você pode criar, registrar e integrar tools customizadas no CrewAI de forma robusta e escalável.
