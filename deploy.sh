#!/bin/bash

# Script de implantau00e7u00e3o para o sistema de estoque
echo "=== Script de Implantau00e7u00e3o do Sistema de Estoque ==="

# Verificar se o Git estu00e1 instalado
if ! command -v git &> /dev/null; then
    echo "Git nu00e3o estu00e1 instalado. Instalando..."
    sudo apt-get update
    sudo apt-get install -y git
fi

# Verificar se o Python 3 estu00e1 instalado
if ! command -v python3 &> /dev/null; then
    echo "Python 3 nu00e3o estu00e1 instalado. Instalando..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip
fi

# Criar backup do banco de dados atual
echo "\nCriando backup do banco de dados atual..."
python3 backup_db.py

# Atualizar o cu00f3digo do repositu00f3rio
echo "\nAtualizando o cu00f3digo do repositu00f3rio..."
if [ -d ".git" ]; then
    git pull
    echo "Cu00f3digo atualizado com sucesso!"
else
    echo "Este diretório não é um repositório Git."
    echo "Para clonar o repositório, execute:"
    echo "git clone <URL_DO_SEU_REPOSITORIO> ."
    exit 1
fi

# Instalar dependências
echo "\nInstalando dependências..."
pip3 install -r requirements.txt

# Migrar o banco de dados
echo "\nMigrando o banco de dados..."
python3 migrate_db.py

# Verificar o sistema
echo "\nVerificando o sistema..."
python3 verificar_sistema.py

echo "\n=== Implantau00e7u00e3o concluu00edda! ==="
echo "Para iniciar o bot, execute: python3 telegram_bot.py"