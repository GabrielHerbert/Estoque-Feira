
import sqlite3
import os

# Verificar se o banco de dados já existe
db_exists = os.path.exists('estoque.db')

# Conectar ao banco de dados (cria se não existir)
conn = sqlite3.connect('estoque.db')
cursor = conn.cursor()

# Criar tabela de produtos se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE
)
''')

# Criar tabela para o Estoque Lopes
cursor.execute('''
CREATE TABLE IF NOT EXISTS estoque_lopes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER DEFAULT 0,
    FOREIGN KEY (produto_id) REFERENCES produtos (id)
)
''')

# Criar tabela para o Estoque Herbert
cursor.execute('''
CREATE TABLE IF NOT EXISTS estoque_herbert (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER DEFAULT 0,
    FOREIGN KEY (produto_id) REFERENCES produtos (id)
)
''')

# Criar tabela para logs de operações
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

# Lista inicial de produtos
produtos_iniciais = [
    "Tilápia",
    "Camarão Inteiro GG",
    "Surubim",
    "Piramutaba",
    "Bacalhau",
    "Pescada Amarela",
    "Camarão Limpo G",
    "Camarão P/ Molho",
    "Camarão Eviscerado",
    "Camarão Eviscerado XG"
]

# Inserir produtos iniciais apenas se o banco de dados acabou de ser criado
if not db_exists:
    for produto in produtos_iniciais:
        # Verificar se o produto já existe
        cursor.execute("SELECT id FROM produtos WHERE nome = ?", (produto,))
        resultado = cursor.fetchone()
        
        if not resultado:
            # Inserir o produto
            cursor.execute("INSERT INTO produtos (nome) VALUES (?)", (produto,))
            produto_id = cursor.lastrowid
            
            # Inicializar o produto nos dois estoques com quantidade zero
            cursor.execute("INSERT INTO estoque_lopes (produto_id, quantidade) VALUES (?, 0)", (produto_id,))
            cursor.execute("INSERT INTO estoque_herbert (produto_id, quantidade) VALUES (?, 0)", (produto_id,))
            
            print(f"Produto '{produto}' adicionado com ID {produto_id}")

# Commit das alterações e fechar conexão
conn.commit()
conn.close()

print("Configuração do banco de dados concluída com sucesso!")
print("Nova tabela 'logs_movimentacao' criada para registrar todas as movimentações de estoque.")
