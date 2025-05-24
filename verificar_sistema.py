#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de verificação final do sistema de estoque
"""

import os
import sys
import sqlite3

def verificar_arquivos():
    """Verifica se todos os arquivos necessários existem"""
    print("📁 Verificando arquivos do sistema...")
    
    arquivos_necessarios = [
        'estoque.db',
        'estoque_core.py',
        'text_processor.py',
        'telegram_bot.py',
        'db_setup.py',
        'criar_tabela_logs.py',
        'requirements.txt'
    ]
    
    todos_existem = True
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            print(f"✅ {arquivo}")
        else:
            print(f"❌ {arquivo} - FALTANDO!")
            todos_existem = False
    
    return todos_existem

def verificar_banco():
    """Verifica a estrutura do banco de dados"""
    print("\n🗄️ Verificando banco de dados...")
    
    if not os.path.exists('estoque.db'):
        print("❌ Banco de dados não encontrado!")
        print("Execute: python db_setup.py")
        return False
    
    try:
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()
        
        # Verificar tabelas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tabelas = [row[0] for row in cursor.fetchall()]
        
        tabelas_necessarias = ['produtos', 'estoque_lopes', 'estoque_herbert', 'logs_movimentacao']
        
        for tabela in tabelas_necessarias:
            if tabela in tabelas:
                print(f"✅ Tabela {tabela}")
            else:
                print(f"❌ Tabela {tabela} - FALTANDO!")
                if tabela == 'logs_movimentacao':
                    print("Execute: python criar_tabela_logs.py")
                else:
                    print("Execute: python db_setup.py")
                return False
        
        # Verificar se há produtos cadastrados
        cursor.execute("SELECT COUNT(*) FROM produtos")
        count_produtos = cursor.fetchone()[0]
        print(f"📦 Produtos cadastrados: {count_produtos}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar banco: {e}")
        return False

def verificar_dependencias():
    """Verifica se as dependências estão instaladas"""
    print("\n📦 Verificando dependências...")
    
    dependencias = [
        ('telegram', 'python-telegram-bot'),
        ('rapidfuzz', 'rapidfuzz')
    ]
    
    todas_instaladas = True
    for modulo, pacote in dependencias:
        try:
            __import__(modulo)
            print(f"✅ {pacote}")
        except ImportError:
            print(f"❌ {pacote} - NÃO INSTALADO!")
            print(f"Execute: pip install {pacote}")
            todas_instaladas = False
    
    return todas_instaladas

def verificar_token():
    """Verifica se o token do bot está configurado"""
    print("\n🤖 Verificando configuração do bot...")
    
    try:
        with open('telegram_bot.py', 'r', encoding='utf-8') as f:
            conteudo = f.read()
            
        if 'TOKEN = "7952211429:AAHP8UFrrmd_E96QIZQNwZigd5zjK8VN5QY"' in conteudo:
            print("⚠️ Token padrão detectado - CONFIGURE SEU PRÓPRIO TOKEN!")
            print("1. Crie um bot no @BotFather")
            print("2. Substitua o TOKEN no arquivo telegram_bot.py")
            return False
        elif 'TOKEN = ""' in conteudo or 'SEU_TOKEN_AQUI' in conteudo:
            print("❌ Token não configurado!")
            print("Configure o TOKEN no arquivo telegram_bot.py")
            return False
        else:
            print("✅ Token configurado")
            return True
            
    except Exception as e:
        print(f"❌ Erro ao verificar token: {e}")
        return False

def main():
    """Função principal de verificação"""
    print("🔍 VERIFICAÇÃO FINAL DO SISTEMA DE ESTOQUE")
    print("=" * 50)
    
    verificacoes = [
        ("Arquivos do sistema", verificar_arquivos),
        ("Banco de dados", verificar_banco),
        ("Dependências Python", verificar_dependencias),
        ("Token do bot", verificar_token)
    ]
    
    resultados = []
    
    for nome, funcao in verificacoes:
        print(f"\n{nome}")
        print("-" * 30)
        resultado = funcao()
        resultados.append((nome, resultado))
    
    print("\n" + "=" * 50)
    print("📊 RESULTADO DA VERIFICAÇÃO")
    print("=" * 50)
    
    tudo_ok = True
    for nome, resultado in resultados:
        status = "✅ OK" if resultado else "❌ PROBLEMA"
        print(f"{nome:<25} {status}")
        if not resultado:
            tudo_ok = False
    
    print("=" * 50)
    
    if tudo_ok:
        print("🎉 SISTEMA PRONTO PARA USO!")
        print("\nPara iniciar o bot:")
        print("python telegram_bot.py")
        print("\nPara testar o sistema:")
        print("python test_sistema_completo.py")
    else:
        print("⚠️ SISTEMA PRECISA DE AJUSTES!")
        print("\nSiga as instruções acima para corrigir os problemas.")
        print("\nApós corrigir, execute novamente:")
        print("python verificar_sistema.py")
    
    print("=" * 50)

if __name__ == "__main__":
    main()