# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

## [2025-05-25] - Reorganização do Projeto

### 🔄 Reestruturação
- **BREAKING**: Reorganizada estrutura completa do projeto
- Movido scripts de upscaling para repositório próprio
- Criada estrutura padrão de diretórios

### 📁 Nova Estrutura de Diretórios
```
├── src/                    # Código fonte principal
├── input/                  # Arquivos de entrada
├── output/                 # Arquivos de saída
├── reports/                # Relatórios gerados
├── examples/               # Exemplos e casos de uso
├── tests/                  # Testes e debug
├── scripts/                # Scripts utilitários
├── docs/                   # Documentação
├── temp/                   # Arquivos temporários
└── db/                     # Banco de dados
```

### ➕ Adicionado
- `README.md` atualizado com documentação completa
- `Makefile` para automatização de tarefas
- `.env.example` com configurações de exemplo
- `docs/TECHNICAL.md` com documentação técnica
- `.gitignore` reorganizado e expandido

### 🗂️ Organização de Arquivos
- Movidos relatórios para `reports/`
- Movidos testes para `tests/`
- Movidos exemplos para `examples/`
- Movidos scripts para `scripts/`
- Movida documentação para `docs/`
- Movidos arquivos temporários para `temp/`

### 🧹 Limpeza
- Removidos arquivos de cache do diretório raiz
- Removido diretório `scripts_upscaling_realce` (movido para repo próprio)
- Organizados arquivos soltos no diretório raiz

### 🔧 Melhorias de Desenvolvimento
- Adicionado suporte completo ao `uv` como gerenciador de pacotes
- Criados comandos `make` para tarefas comuns
- Configuração de ambiente simplificada

## Versões Anteriores

### [Antes de 2025-05-25] - Estado Original
- Estrutura de projeto desorganizada
- Arquivos misturados no diretório raiz
- Documentação limitada
- Scripts de upscaling incluídos
