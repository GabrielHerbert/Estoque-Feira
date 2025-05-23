#!/usr/bin/env python3
import requests
import json
import time

# Token do bot
TOKEN = "7952211429:AAHP8UFrrmd_E96QIZQNwZigd5zjK8VN5QY"
# ID do chat (substitua pelo seu ID de chat)
CHAT_ID = "123456789"

def send_message(text):
    """Envia uma mensagem para o bot"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text
    }
    response = requests.post(url, data=data)
    return response.json()

def get_updates():
    """Obtém as atualizações do bot"""
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    response = requests.get(url)
    return response.json()

# Teste de envio de mensagem
print("Enviando mensagem para o bot...")
result = send_message("Teste de formatação com 3 casas decimais")
print(f"Resultado: {json.dumps(result, indent=2)}")

# Aguardar um pouco para o bot processar
time.sleep(2)

# Obter atualizações
print("\nObtendo atualizações...")
updates = get_updates()
print(f"Atualizações: {json.dumps(updates, indent=2)}")
