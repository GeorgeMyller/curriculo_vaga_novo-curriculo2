# Importa o decorador 'tool' do pacote crewai.tools para registrar a função como uma ferramenta utilizável pelos agentes
from crewai.tools import tool
# Importa o conversor de LaTeX para texto plano da biblioteca pylatexenc
from pylatexenc.latex2text import LatexNodes2Text
import os
from functools import lru_cache


# Registra esta função como uma ferramenta chamada "LatexReaderTool" que pode ser usada pelos agentes da CrewAI
@tool("LatexReaderTool")
def LatexReaderTool(inputs=None, file_path: str = None, encoding: str = 'utf-8', chunk_size: int = 8192) -> str:
    """
    Extrai texto limpo e estruturado de um arquivo .tex de currículo.

    Você pode passar o caminho do arquivo .tex diretamente como `file_path`.
    """
    # Verifica se o caminho do arquivo foi fornecido
    if not file_path:
        return "Erro: nenhum caminho de arquivo fornecido para LatexReaderTool."
    # Verifica se o arquivo existe
    if not os.path.isfile(file_path):
        return f"Erro: o arquivo '{file_path}' não existe."
    try:
        # Leitura em chunks para reduzir uso de memória
        content = ""
        with open(file_path, 'r', encoding=encoding) as file:
            for chunk in iter(lambda: file.read(chunk_size), ''):
                content += chunk
        # Converte o conteúdo LaTeX para texto plano com cache
        clean_text = convert_latex_to_text(content)
        return clean_text
    except FileNotFoundError:
        return f"Erro: arquivo não encontrado: {file_path}"
    except PermissionError:
        return f"Erro: sem permissão para acessar o arquivo: {file_path}"
    except UnicodeDecodeError:
        return "Erro: falha ao decodificar o arquivo. Tente especificar uma codificação diferente."
    except Exception as e:
        return f"Erro ao ler arquivo .tex: {str(e)}"


# Função auxiliar com cache para conversão LaTeX
@lru_cache(maxsize=32)
def convert_latex_to_text(content: str) -> str:
    """
    Converte conteúdo LaTeX para texto plano com cache para melhorar performance.
    
    Args:
        content: Conteúdo LaTeX a ser convertido
    
    Returns:
        Texto extraído do conteúdo LaTeX
    """
    return LatexNodes2Text().latex_to_text(content)
