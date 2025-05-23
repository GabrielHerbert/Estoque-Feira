
import sqlite3
from typing import List, Dict, Any, Optional, Tuple, Union

def get_connection():
    """Retorna uma conexão com o banco de dados"""
    return sqlite3.connect('estoque.db')

def add_produto_catalogo(nome: str) -> int:
    """
    Adiciona um novo produto ao catálogo
    
    Args:
        nome: Nome do produto
        
    Returns:
        ID do produto adicionado ou -1 em caso de erro
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Verificar se o produto já existe
        cursor.execute("SELECT id FROM produtos WHERE nome = ?", (nome,))
        resultado = cursor.fetchone()
        
        if resultado:
            return resultado[0]  # Retorna o ID se o produto já existir
        
        # Inserir o novo produto
        cursor.execute("INSERT INTO produtos (nome) VALUES (?)", (nome,))
        produto_id = cursor.lastrowid
        
        # Inicializar o produto nos dois estoques com quantidade zero
        cursor.execute("INSERT INTO estoque_lopes (produto_id, quantidade) VALUES (?, 0)", (produto_id,))
        cursor.execute("INSERT INTO estoque_herbert (produto_id, quantidade) VALUES (?, 0)", (produto_id,))
        
        conn.commit()
        return produto_id
    except Exception as e:
        print(f"Erro ao adicionar produto: {e}")
        return -1
    finally:
        conn.close()

def add_to_stock(produto_id: int, quantidade: float, filial: str) -> bool:
    """
    Adiciona uma quantidade de produto ao estoque
    
    Args:
        produto_id: ID do produto
        quantidade: Quantidade a ser adicionada (em kg)
        filial: Nome da filial ('lopes' ou 'herbert')
        
    Returns:
        True se a operação foi bem-sucedida, False caso contrário
    """
    if filial.lower() not in ['lopes', 'herbert']:
        raise ValueError("Filial deve ser 'lopes' ou 'herbert'")
    
    tabela = f"estoque_{filial.lower()}"
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Verificar se o produto existe
        cursor.execute("SELECT id FROM produtos WHERE id = ?", (produto_id,))
        if not cursor.fetchone():
            print(f"Produto com ID {produto_id} não encontrado")
            return False
        
        # Obter quantidade atual
        cursor.execute(f"SELECT quantidade FROM {tabela} WHERE produto_id = ?", (produto_id,))
        resultado = cursor.fetchone()
        
        if resultado:
            # Atualizar quantidade
            nova_quantidade = resultado[0] + quantidade
            cursor.execute(f"UPDATE {tabela} SET quantidade = ? WHERE produto_id = ?", 
                          (nova_quantidade, produto_id))
        else:
            # Inserir novo registro
            cursor.execute(f"INSERT INTO {tabela} (produto_id, quantidade) VALUES (?, ?)", 
                          (produto_id, quantidade))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao adicionar ao estoque: {e}")
        return False
    finally:
        conn.close()

def remove_from_stock(produto_id: int, quantidade: float, filial: str) -> bool:
    """
    Remove uma quantidade de produto do estoque
    
    Args:
        produto_id: ID do produto
        quantidade: Quantidade a ser removida (em kg)
        filial: Nome da filial ('lopes' ou 'herbert')
        
    Returns:
        True se a operação foi bem-sucedida, False caso contrário
    """
    if filial.lower() not in ['lopes', 'herbert']:
        raise ValueError("Filial deve ser 'lopes' ou 'herbert'")
    
    tabela = f"estoque_{filial.lower()}"
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Verificar se o produto existe
        cursor.execute("SELECT id FROM produtos WHERE id = ?", (produto_id,))
        if not cursor.fetchone():
            print(f"Produto com ID {produto_id} não encontrado")
            return False
        
        # Obter quantidade atual
        cursor.execute(f"SELECT quantidade FROM {tabela} WHERE produto_id = ?", (produto_id,))
        resultado = cursor.fetchone()
        
        if not resultado:
            print(f"Produto não encontrado no estoque {filial}")
            return False
        
        quantidade_atual = resultado[0]
        
        # Verificar se há quantidade suficiente
        if quantidade_atual < quantidade:
            print(f"Quantidade insuficiente no estoque. Disponível: {quantidade_atual}, Solicitado: {quantidade}")
            return False
        
        # Atualizar quantidade
        nova_quantidade = quantidade_atual - quantidade
        cursor.execute(f"UPDATE {tabela} SET quantidade = ? WHERE produto_id = ?", 
                      (nova_quantidade, produto_id))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao remover do estoque: {e}")
        return False
    finally:
        conn.close()

def get_stock(filial: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Obtém informações de estoque
    
    Args:
        filial: Nome da filial ('lopes', 'herbert' ou None para ambos)
        
    Returns:
        Lista de dicionários com informações de estoque
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        resultados = []
        
        if filial is None or filial.lower() == 'lopes':
            query = """
            SELECT p.id, p.nome, el.quantidade 
            FROM produtos p
            LEFT JOIN estoque_lopes el ON p.id = el.produto_id
            ORDER BY p.nome
            """
            
            cursor.execute(query)
            for row in cursor.fetchall():
                resultados.append({
                    'id': row[0],
                    'nome': row[1],
                    'estoque': 'Lopes',
                    'quantidade': row[2] or 0
                })
        
        if filial is None or filial.lower() == 'herbert':
            query = """
            SELECT p.id, p.nome, eh.quantidade 
            FROM produtos p
            LEFT JOIN estoque_herbert eh ON p.id = eh.produto_id
            ORDER BY p.nome
            """
            
            cursor.execute(query)
            for row in cursor.fetchall():
                resultados.append({
                    'id': row[0],
                    'nome': row[1],
                    'estoque': 'Herbert',
                    'quantidade': row[2] or 0
                })
        
        return resultados
    finally:
        conn.close()

def get_stock_combined() -> List[Dict[str, Any]]:
    """
    Obtém informações de estoque combinadas (Lopes + Herbert)
    
    Returns:
        Lista de dicionários com informações de estoque combinadas
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        query = """
        SELECT p.id, p.nome, 
               COALESCE(el.quantidade, 0) as qtd_lopes, 
               COALESCE(eh.quantidade, 0) as qtd_herbert,
               COALESCE(el.quantidade, 0) + COALESCE(eh.quantidade, 0) as qtd_total
        FROM produtos p
        LEFT JOIN estoque_lopes el ON p.id = el.produto_id
        LEFT JOIN estoque_herbert eh ON p.id = eh.produto_id
        ORDER BY p.nome
        """
        
        cursor.execute(query)
        resultados = []
        
        for row in cursor.fetchall():
            resultados.append({
                'id': row[0],
                'nome': row[1],
                'qtd_lopes': row[2],
                'qtd_herbert': row[3],
                'qtd_total': row[4]
            })
        
        return resultados
    finally:
        conn.close()

def list_products() -> List[Tuple[int, str]]:
    """
    Lista todos os produtos cadastrados
    
    Returns:
        Lista de tuplas (id, nome) dos produtos
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id, nome FROM produtos ORDER BY nome")
        return cursor.fetchall()
    finally:
        conn.close()

def get_product_by_id(produto_id: int) -> Optional[Tuple[int, str]]:
    """
    Obtém um produto pelo ID
    
    Args:
        produto_id: ID do produto
        
    Returns:
        Tupla (id, nome) do produto ou None se não encontrado
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id, nome FROM produtos WHERE id = ?", (produto_id,))
        return cursor.fetchone()
    finally:
        conn.close()

def get_product_by_name(nome: str) -> Optional[Tuple[int, str]]:
    """
    Obtém um produto pelo nome (busca parcial)
    
    Args:
        nome: Nome ou parte do nome do produto
        
    Returns:
        Tupla (id, nome) do produto ou None se não encontrado
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id, nome FROM produtos WHERE nome LIKE ? ORDER BY nome", (f"%{nome}%",))
        return cursor.fetchone()
    finally:
        conn.close()

def search_products(termo: str) -> List[Tuple[int, str]]:
    """
    Busca produtos pelo nome
    
    Args:
        termo: Termo de busca
        
    Returns:
        Lista de tuplas (id, nome) dos produtos encontrados
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id, nome FROM produtos WHERE nome LIKE ? ORDER BY nome", (f"%{termo}%",))
        return cursor.fetchall()
    finally:
        conn.close()

# Função para formatar o estoque para exibição no Telegram
def format_stock_message(estoque_data: List[Dict[str, Any]], titulo: str = "Estoque Atual") -> str:
    """
    Formata os dados de estoque para exibição no Telegram
    
    Args:
        estoque_data: Lista de dicionários com informações de estoque
        titulo: Título da mensagem
        
    Returns:
        Mensagem formatada
    """
    mensagem = f"*{titulo}*\n\n"
    
    if 'qtd_lopes' in estoque_data[0]:  # Estoque combinado
        mensagem += "```\n"
        mensagem += f"{'ID':<3} {'Produto':<25} {'Lopes':<8} {'Herbert':<8} {'Total':<8}\n"
        mensagem += "-" * 55 + "\n"
        
        for item in estoque_data:
            mensagem += f"{item['id']:<3} {item['nome'][:25]:<25} {item['qtd_lopes']:<8.3f} {item['qtd_herbert']:<8.3f} {item['qtd_total']:<8.3f}\n"
        
        mensagem += "```"
    else:  # Estoque individual
        estoque_atual = estoque_data[0]['estoque'] if estoque_data else ""
        mensagem += f"*Filial: {estoque_atual}*\n\n"
        mensagem += "```\n"
        mensagem += f"{'ID':<3} {'Produto':<25} {'Quantidade':<10}\n"
        mensagem += "-" * 40 + "\n"
        
        for item in estoque_data:
            mensagem += f"{item['id']:<3} {item['nome'][:25]:<25} {item['quantidade']:<10.3f}\n"
        
        mensagem += "```"
    
    return mensagem

# Teste simples para verificar se o módulo está funcionando
if __name__ == "__main__":
    print("Testando módulo de estoque...")
    produtos = list_products()
    print(f"Total de produtos: {len(produtos)}")
    
    estoque = get_stock_combined()
    print("Estoque combinado:")
    for item in estoque:
        print(f"{item['nome']}: Lopes={item['qtd_lopes']}, Herbert={item['qtd_herbert']}, Total={item['qtd_total']}")
