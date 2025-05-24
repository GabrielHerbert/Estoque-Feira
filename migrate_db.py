#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sqlite3
import backup_db

def check_logs_table(db_path="estoque.db"):
    """Verifica se a tabela de logs existe no banco de dados"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='logs_movimentacao'")
    table_exists = cursor.fetchone() is not None
    
    conn.close()
    return table_exists

def create_logs_table(db_path="estoque.db"):
    """Cria a tabela de logs se ela nu00e3o existir"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Criar tabela de logs
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS logs_movimentacao (
        id INTEGER PRIMARY KEY,
        produto_id INTEGER,
        filial TEXT,
        operacao TEXT,
        quantidade INTEGER,
        quantidade_anterior INTEGER,
        quantidade_nova INTEGER,
        data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        observacao TEXT,
        FOREIGN KEY (produto_id) REFERENCES produtos(id)
    )
    ''')
    
    conn.commit()
    conn.close()
    print("Tabela de logs criada com sucesso!")
    return True

def migrate_database(db_path="estoque.db"):
    """Migra o banco de dados, preservando os dados existentes"""
    # Verificar se o banco de dados existe
    if not os.path.exists(db_path):
        print(f"Erro: Banco de dados {db_path} nu00e3o encontrado!")
        return False
    
    # Fazer backup antes de qualquer alterau00e7u00e3o
    print("Criando backup do banco de dados atual...")
    if not backup_db.backup_database(db_path):
        print("Erro ao criar backup. Abortando migrau00e7u00e3o.")
        return False
    
    # Verificar se a tabela de logs ju00e1 existe
    has_logs_table = check_logs_table(db_path)
    
    if has_logs_table:
        print("A tabela de logs ju00e1 existe no banco de dados. Nenhuma migrau00e7u00e3o necessu00e1ria.")
    else:
        print("A tabela de logs nu00e3o existe. Criando...")
        if not create_logs_table(db_path):
            print("Erro ao criar tabela de logs. Abortando migrau00e7u00e3o.")
            return False
    
    print("Migrau00e7u00e3o concluu00edda com sucesso!")
    return True

if __name__ == "__main__":
    migrate_database()