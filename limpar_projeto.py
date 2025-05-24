#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil

# Lista de arquivos necessários para o projeto
arquivos_necessarios = [
    'setup.sh',
    'db_setup.py',
    'estoque_core.py',
    'estoque_db.py',
    'README.md',
    'requirements.txt',
    'telegram_bot.py',
    'text_processor.py',
    'verificar_sistema.py',
    'estoque.db',  # Banco de dados
    'limpar_projeto.py',  # Este script
    '.git'  # Pasta git
]

# Obter lista de todos os arquivos e pastas no diretório atual
conteudo = os.listdir('.')

# Arquivos e pastas a serem removidos
remover = []
for item in conteudo:
    if item not in arquivos_necessarios and not item.startswith('__'):
        remover.append(item)

# Remover arquivos e pastas desnecessários
for item in remover:
    caminho = os.path.join('.', item)
    if os.path.isfile(caminho):
        print(f"Removendo arquivo: {item}")
        os.remove(caminho)
    elif os.path.isdir(caminho):
        print(f"Removendo pasta: {item}")
        shutil.rmtree(caminho)

print("\nLimpeza concluída! Arquivos mantidos:")
for item in sorted(os.listdir('.')):
    if not item.startswith('__'):
        print(f"- {item}")