#!/bin/bash

echo "Instalando dependências..."
pip install -r requirements.txt

echo "Verificando banco de dados..."
python db_setup.py

echo "Configuração concluída!"
echo ""
echo "Para iniciar o bot, edite o arquivo .env com seu token do Telegram e execute:"
echo "python telegram_bot.py"
