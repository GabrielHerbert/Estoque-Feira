#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import datetime
import sqlite3

def backup_database(db_path="estoque.db"):
    """Cria um backup do banco de dados atual"""
    # Verificar se o banco de dados existe
    if not os.path.exists(db_path):
        print(f"Erro: Banco de dados {db_path} não encontrado!")
        return False
    
    # Criar pasta de backup se não existir
    backup_dir = "backups"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    # Gerar nome do arquivo de backup com timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"{backup_dir}/estoque_backup_{timestamp}.db"
    
    # Copiar o banco de dados
    try:
        # Fechar todas as conexões com o banco de dados
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA wal_checkpoint(FULL)")
        conn.close()
        
        # Copiar o arquivo
        shutil.copy2(db_path, backup_filename)
        print(f"Backup criado com sucesso: {backup_filename}")
        return True
    except Exception as e:
        print(f"Erro ao criar backup: {str(e)}")
        return False

if __name__ == "__main__":
    backup_database()