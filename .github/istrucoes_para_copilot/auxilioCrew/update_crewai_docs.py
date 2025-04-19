import subprocess
import sys
import requests
import os
from difflib import unified_diff

def get_installed_version():
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'show', 'crewAI'], capture_output=True, text=True, check=True)
        for line in result.stdout.splitlines():
            if line.startswith('Version:'):
                return line.split(':')[1].strip()
    except subprocess.CalledProcessError:
        return None

def get_latest_version():
    try:
        response = requests.get('https://pypi.org/pypi/crewAI/json')
        response.raise_for_status()
        return response.json()['info']['version']
    except requests.RequestException:
        return None

def fetch_remote_file(url, local_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(local_path, 'w') as file:
            file.write(response.text)
        return response.text
    except requests.RequestException as e:
        print(f"Erro ao buscar {url}: {e}")
        return None

def compare_files(local_path, remote_content):
    if not os.path.exists(local_path):
        print(f"Arquivo local {local_path} não encontrado. Salvando o arquivo remoto.")
        return None

    with open(local_path, 'r') as file:
        local_content = file.read()

    diff = list(unified_diff(local_content.splitlines(), remote_content.splitlines(), lineterm='',
                             fromfile='local', tofile='remote'))
    if diff:
        print(f"Diferenças encontradas no arquivo {local_path}:")
        print('\n'.join(diff))
    else:
        print(f"Nenhuma diferença encontrada no arquivo {local_path}.")

def handle_docs_update():
    os.makedirs('docs', exist_ok=True)

    files_to_fetch = {
        'README.md': 'https://raw.githubusercontent.com/joaomdmoura/crewai/main/README.md',
        'CHANGELOG.md': 'https://raw.githubusercontent.com/joaomdmoura/crewai/main/CHANGELOG.md'
    }

    for filename, url in files_to_fetch.items():
        local_path = os.path.join('docs', f'crewai_{filename}_remote.md')
        print(f"Buscando {filename} do repositório oficial...")
        remote_content = fetch_remote_file(url, local_path)
        if remote_content:
            compare_files(local_path, remote_content)

def main():
    installed_version = get_installed_version()
    if not installed_version:
        print("CrewAI não está instalado localmente.")
        return

    latest_version = get_latest_version()
    if not latest_version:
        print("Não foi possível verificar a última versão do CrewAI no PyPI.")
        return

    print(f"Versão instalada do CrewAI: {installed_version}")
    print(f"Última versão disponível no PyPI: {latest_version}")

    if installed_version != latest_version:
        print("Você está desatualizado. Considere atualizar o CrewAI executando:")
        print(f"pip install --upgrade crewAI")
        handle_docs_update()
    else:
        print("Você já está usando a versão mais recente do CrewAI.")

if __name__ == "__main__":
    main()