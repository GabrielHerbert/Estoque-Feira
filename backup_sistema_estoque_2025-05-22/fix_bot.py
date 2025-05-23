#!/usr/bin/env python3
import os
import sys
import subprocess
import time

# Verificar se o bot está em execução
def check_bot_running():
    try:
        output = subprocess.check_output(["ps", "-ef"]).decode("utf-8")
        return "telegram_bot.py" in output and "grep" not in output
    except Exception as e:
        print(f"Erro ao verificar se o bot está em execução: {e}")
        return False

# Encerrar todas as instâncias do bot
def kill_bot():
    try:
        subprocess.run(["pkill", "-f", "telegram_bot.py"])
        time.sleep(2)
        return not check_bot_running()
    except Exception as e:
        print(f"Erro ao encerrar o bot: {e}")
        return False

# Corrigir o código do estoque_core.py
def fix_estoque_core():
    try:
        # Ler o arquivo
        with open("/home/ubuntu/estoque_core.py", "r") as f:
            content = f.read()
        
        # Verificar se já está corrigido
        if ":<8.1f}" in content or ":<10.1f}" in content:
            print("O arquivo já foi corrigido anteriormente.")
            return True
        
        # Fazer backup do arquivo original
        with open("/home/ubuntu/estoque_core.py.bak", "w") as f:
            f.write(content)
        
        # Substituir a formatação de 3 casas decimais por 1 casa decimal
        content = content.replace(":<8.3f}", ":<8.1f}")
        content = content.replace(":<10.3f}", ":<10.1f}")
        
        # Salvar o arquivo corrigido
        with open("/home/ubuntu/estoque_core.py", "w") as f:
            f.write(content)
        
        print("Arquivo estoque_core.py corrigido com sucesso.")
        return True
    except Exception as e:
        print(f"Erro ao corrigir o arquivo estoque_core.py: {e}")
        return False

# Iniciar o bot
def start_bot():
    try:
        os.chdir("/home/ubuntu")
        subprocess.Popen(["nohup", "python3", "-u", "telegram_bot.py", ">", "telegram_bot_debug.log", "2>&1", "&"], 
                         shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(3)
        return check_bot_running()
    except Exception as e:
        print(f"Erro ao iniciar o bot: {e}")
        return False

# Executar as etapas de correção
print("Verificando se o bot está em execução...")
if check_bot_running():
    print("Bot em execução. Encerrando...")
    if kill_bot():
        print("Bot encerrado com sucesso.")
    else:
        print("Falha ao encerrar o bot.")
else:
    print("Bot não está em execução.")

print("\nCorrigindo o arquivo estoque_core.py...")
if fix_estoque_core():
    print("Arquivo corrigido com sucesso.")
else:
    print("Falha ao corrigir o arquivo.")

print("\nIniciando o bot...")
if start_bot():
    print("Bot iniciado com sucesso.")
else:
    print("Falha ao iniciar o bot.")

print("\nProcesso de correção concluído.")
