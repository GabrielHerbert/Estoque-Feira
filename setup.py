#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de Setup Completo - Sistema de Estoque Telegram
Instala e configura tudo necessário para o bot funcionar no servidor
"""

import os
import sys
import subprocess
import sqlite3
from datetime import datetime

def print_header():
    """Imprime cabeçalho do setup"""
    print("=" * 60)
    print("🚀 SETUP - SISTEMA DE ESTOQUE TELEGRAM")
    print("=" * 60)
    print("Versão: 2.1.0")
    print("Data:", datetime.now().strftime("%d/%m/%Y %H:%M"))
    print("=" * 60)

def verificar_python():
    """Verifica se a versão do Python é compatível"""
    print("\n🔍 Verificando versão do Python...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} não é compatível")
        print("✅ Versão mínima requerida: Python 3.8")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatível")
    return True

def instalar_dependencias():
    """Instala as dependências do projeto"""
    print("\n📦 Instalando dependências...")
    
    # Criar requirements.txt se não existir
    requirements = [
        "python-telegram-bot==20.7",
        "sqlite3"  # Já vem com Python, mas listamos para documentação
    ]
    
    if not os.path.exists('requirements.txt'):
        with open('requirements.txt', 'w') as f:
            f.write('\n'.join(requirements))
        print("✅ Arquivo requirements.txt criado")
    
    try:
        # Instalar dependências
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas com sucesso")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def criar_banco_dados():
    """Cria o banco de dados com todas as tabelas necessárias"""
    print("\n🗄️ Configurando banco de dados...")
    
    try:
        # Conectar ao banco (cria se não existir)
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()
        
        # Criar tabela de produtos
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE
        )
        ''')
        print("✅ Tabela 'produtos' criada/verificada")
        
        # Criar tabela para o Estoque Lopes
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS estoque_lopes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER NOT NULL,
            quantidade INTEGER DEFAULT 0,
            FOREIGN KEY (produto_id) REFERENCES produtos (id)
        )
        ''')
        print("✅ Tabela 'estoque_lopes' criada/verificada")
        
        # Criar tabela para o Estoque Herbert
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS estoque_herbert (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER NOT NULL,
            quantidade INTEGER DEFAULT 0,
            FOREIGN KEY (produto_id) REFERENCES produtos (id)
        )
        ''')
        print("✅ Tabela 'estoque_herbert' criada/verificada")
        
        # Criar tabela para logs de operações (NOVA)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS operacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filial TEXT NOT NULL,
            operacao TEXT NOT NULL,
            mensagem TEXT NOT NULL,
            data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            observacao TEXT
        )
        ''')
        print("✅ Tabela 'operacoes' criada/verificada")
        
        # Criar tabela de logs antiga para compatibilidade
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs_movimentacao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER NOT NULL,
            filial TEXT NOT NULL,
            operacao TEXT NOT NULL,
            quantidade_anterior INTEGER NOT NULL,
            quantidade_nova INTEGER NOT NULL,
            data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            observacao TEXT,
            FOREIGN KEY (produto_id) REFERENCES produtos (id)
        )
        ''')
        print("✅ Tabela 'logs_movimentacao' criada/verificada (compatibilidade)")
        
        conn.commit()
        conn.close()
        
        print("✅ Banco de dados configurado com sucesso")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar banco de dados: {e}")
        return False

def inserir_produtos_exemplo():
    """Insere alguns produtos de exemplo se o banco estiver vazio"""
    print("\n🐟 Verificando produtos de exemplo...")
    
    try:
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()
        
        # Verificar se já existem produtos
        cursor.execute("SELECT COUNT(*) FROM produtos")
        count = cursor.fetchone()[0]
        
        if count == 0:
            produtos_exemplo = [
                "tilápia",
                "camarão limpo g",
                "pescada amarela",
                "salmão",
                "robalo",
                "dourado",
                "camarão médio",
                "lula limpa"
            ]
            
            for produto in produtos_exemplo:
                cursor.execute("INSERT INTO produtos (nome) VALUES (?)", (produto,))
            
            conn.commit()
            print(f"✅ {len(produtos_exemplo)} produtos de exemplo inseridos")
        else:
            print(f"✅ Banco já possui {count} produtos cadastrados")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro ao inserir produtos de exemplo: {e}")
        return False

def verificar_arquivos_necessarios():
    """Verifica se todos os arquivos necessários estão presentes"""
    print("\n📁 Verificando arquivos do sistema...")
    
    arquivos_necessarios = [
        'telegram_bot.py',
        'estoque_core.py',
        'estoque_db.py',
        'text_processor.py',
        'db_setup.py',
        'backup_db.py'
    ]
    
    todos_presentes = True
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            print(f"✅ {arquivo}")
        else:
            print(f"❌ {arquivo} - FALTANDO")
            todos_presentes = False
    
    return todos_presentes

def testar_importacoes():
    """Testa se todos os módulos podem ser importados"""
    print("\n🔍 Testando importações dos módulos...")
    
    modulos = [
        ('estoque_core', 'Funções principais'),
        ('estoque_db', 'Banco de dados'),
        ('text_processor', 'Processamento de texto')
    ]
    
    todos_ok = True
    for modulo, descricao in modulos:
        try:
            __import__(modulo)
            print(f"✅ {modulo} - {descricao}")
        except ImportError as e:
            print(f"❌ {modulo} - Erro: {e}")
            todos_ok = False
    
    return todos_ok

def testar_funcoes_basicas():
    """Testa funções básicas do sistema"""
    print("\n🧪 Testando funções básicas...")
    
    try:
        import estoque_core
        
        # Testar conexão com banco
        estoque_lopes = estoque_core.get_stock("lopes")
        print("✅ Conexão com banco - OK")
        
        # Testar formatação
        mensagem = estoque_core.format_stock_message(estoque_lopes, "Teste")
        print("✅ Formatação de mensagens - OK")
        
        # Testar operações
        operacoes = estoque_core.get_operacoes(limite=1)
        print("✅ Sistema de operações - OK")
        
        # Testar relatórios
        relatorio = estoque_core.gerar_relatorio_estoque("lopes")
        print("✅ Geração de relatórios - OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro nos testes: {e}")
        return False

def configurar_token():
    """Orienta sobre configuração do token"""
    print("\n🔑 CONFIGURAÇÃO DO TOKEN DO BOT")
    print("-" * 40)
    print("⚠️  IMPORTANTE: Configure o token do bot antes de usar!")
    print()
    print("1. Abra o arquivo 'telegram_bot.py'")
    print("2. Localize a linha: TOKEN = \"7952211429:AAHP8UFrrmd_E96QIZQNwZigd5zjK8VN5QY\"")
    print("3. Substitua pelo seu token obtido do @BotFather")
    print()
    print("💡 Como obter um token:")
    print("   - Converse com @BotFather no Telegram")
    print("   - Use o comando /newbot")
    print("   - Siga as instruções")
    print("   - Copie o token fornecido")

def mostrar_instrucoes_uso():
    """Mostra instruções de uso do sistema"""
    print("\n📱 COMO USAR O SISTEMA")
    print("-" * 40)
    print("1. Configure o token do bot (veja instruções acima)")
    print("2. Execute: python telegram_bot.py")
    print("3. No Telegram, inicie conversa com seu bot")
    print("4. Use /start para ver o menu principal")
    print()
    print("📊 FUNCIONALIDADES DISPONÍVEIS:")
    print("   • Gestão de estoque por filial (Lopes/Herbert)")
    print("   • Relatórios (individual e conjunto)")
    print("   • Adição/remoção de produtos")
    print("   • Sistema de logs completo")
    print("   • Processamento inteligente de texto")

def main():
    """Função principal do setup"""
    print_header()
    
    # Lista de verificações
    verificacoes = [
        ("Versão do Python", verificar_python),
        ("Arquivos necessários", verificar_arquivos_necessarios),
        ("Dependências", instalar_dependencias),
        ("Banco de dados", criar_banco_dados),
        ("Produtos de exemplo", inserir_produtos_exemplo),
        ("Importações", testar_importacoes),
        ("Funções básicas", testar_funcoes_basicas)
    ]
    
    sucessos = 0
    total = len(verificacoes)
    
    for nome, funcao in verificacoes:
        print(f"\n{'='*20} {nome.upper()} {'='*20}")
        try:
            if funcao():
                sucessos += 1
            else:
                print(f"❌ Falha em: {nome}")
        except Exception as e:
            print(f"❌ Erro inesperado em {nome}: {e}")
    
    # Resultado final
    print("\n" + "=" * 60)
    print("📊 RESULTADO DO SETUP")
    print("=" * 60)
    print(f"✅ Sucessos: {sucessos}/{total}")
    
    if sucessos == total:
        print("🎉 SETUP CONCLUÍDO COM SUCESSO!")
        print("\n✅ Sistema pronto para uso!")
        configurar_token()
        mostrar_instrucoes_uso()
        
        print("\n🚀 PRÓXIMOS PASSOS:")
        print("1. Configure o token do bot")
        print("2. Execute: python telegram_bot.py")
        print("3. Teste o bot no Telegram")
        
    else:
        print("⚠️ SETUP INCOMPLETO")
        print(f"❌ {total - sucessos} verificações falharam")
        print("\n🔧 Verifique os erros acima e execute novamente:")
        print("python setup.py")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()