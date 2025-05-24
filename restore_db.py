#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import sqlite3
import glob

def list_backups():
    """Lista todos os backups disponu00edveis"""
    backup_dir = "backups"
    if not os.path.exists(backup_dir):
        print("Nenhum backup encontrado!")
        return []
    
    backups = glob.glob(f"{backup_dir}/estoque_backup_*.db")
    backups.sort(reverse=True)  # Mais recentes primeiro
    
    if not backups:
        print("Nenhum backup encontrado!")
        return []
    
    print("Backups disponu00edveis:")
    for i, backup in enumerate(backups):
        # Extrair a data e hora do nome do arquivo
        filename = os.path.basename(backup)
        timestamp = filename.replace("estoque_backup_", "").replace(".db", "")
        date_part = timestamp[:8]
        time_part = timestamp[9:]
        formatted_date = f"{date_part[:4]}-{date_part[4:6]}-{date_part[6:8]}"
        formatted_time = f"{time_part[:2]}:{time_part[2:4]}:{time_part[4:6]}"
        print(f"{i+1}. {formatted_date} {formatted_time} - {backup}")
    
    return backups

def restore_database(backup_path, target_path="estoque.db"):
    """Restaura um backup para o banco de dados principal"""
    if not os.path.exists(backup_path):
        print(f"Erro: Arquivo de backup {backup_path} nu00e3o encontrado!")
        return False
    
    # Fazer backup do banco atual antes de substituir
    if os.path.exists(target_path):
        import backup_db
        backup_db.backup_database(target_path)
        
        # Fechar todas as conexu00f5es com o banco de dados
        try:
            conn = sqlite3.connect(target_path)
            conn.execute("PRAGMA wal_checkpoint(FULL)")
            conn.close()
        except Exception as e:
            print(f"Aviso: Nu00e3o foi possu00edvel fechar conexu00f5es com o banco: {str(e)}")
    
    # Copiar o backup para o local do banco de dados principal
    try:
        shutil.copy2(backup_path, target_path)
        print(f"Banco de dados restaurado com sucesso a partir de: {backup_path}")
        return True
    except Exception as e:
        print(f"Erro ao restaurar banco de dados: {str(e)}")
        return False

def interactive_restore():
    """Interface interativa para restaurar um backup"""
    backups = list_backups()
    if not backups:
        return
    
    try:
        choice = int(input("\nDigite o nu00famero do backup que deseja restaurar (0 para cancelar): "))
        if choice == 0:
            print("Operau00e7u00e3o cancelada.")
            return
        
        if 1 <= choice <= len(backups):
            selected_backup = backups[choice-1]
            confirm = input(f"Tem certeza que deseja restaurar {selected_backup}? (s/n): ")
            if confirm.lower() == 's':
                restore_database(selected_backup)
            else:
                print("Operau00e7u00e3o cancelada.")
        else:
            print("Opu00e7u00e3o invu00e1lida!")
    except ValueError:
        print("Por favor, digite um nu00famero vu00e1lido.")

if __name__ == "__main__":
    interactive_restore()