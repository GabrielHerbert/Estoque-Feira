
import sqlite3
from typing import List, Tuple, Optional, Dict, Any

class EstoqueDB:
    def __init__(self, db_path='estoque.db'):
        self.db_path = db_path
        
    def _get_connection(self):
        """Retorna uma conexão com o banco de dados"""
        return sqlite3.connect(self.db_path)
    
    def add_product(self, nome: str) -> int:
        """
        Adiciona um novo produto ao banco de dados
        
        Args:
            nome: Nome do produto
            
        Returns:
            ID do produto adicionado
        """
        conn = self._get_connection()
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
        finally:
            conn.close()
    
    def update_stock(self, produto_id: int, estoque: str, quantidade: float) -> bool:
        """
        Atualiza a quantidade de um produto em um estoque específico
        
        Args:
            produto_id: ID do produto
            estoque: Nome do estoque ('lopes' ou 'herbert')
            quantidade: Nova quantidade em Kg
            
        Returns:
            True se a atualização foi bem-sucedida, False caso contrário
        """
        if estoque.lower() not in ['lopes', 'herbert']:
            raise ValueError("Estoque deve ser 'lopes' ou 'herbert'")
        
        tabela = f"estoque_{estoque.lower()}"
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            # Verificar se o produto existe no estoque
            cursor.execute(f"SELECT id FROM {tabela} WHERE produto_id = ?", (produto_id,))
            resultado = cursor.fetchone()
            
            if resultado:
                # Atualizar quantidade
                cursor.execute(f"UPDATE {tabela} SET quantidade = ? WHERE produto_id = ?", 
                              (quantidade, produto_id))
            else:
                # Inserir novo registro
                cursor.execute(f"INSERT INTO {tabela} (produto_id, quantidade) VALUES (?, ?)", 
                              (produto_id, quantidade))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao atualizar estoque: {e}")
            return False
        finally:
            conn.close()
    
    def get_stock(self, produto_id: Optional[int] = None, estoque: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Obtém informações de estoque
        
        Args:
            produto_id: ID do produto (opcional, se None retorna todos os produtos)
            estoque: Nome do estoque ('lopes' ou 'herbert', opcional)
            
        Returns:
            Lista de dicionários com informações de estoque
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            resultados = []
            
            if estoque is None or estoque.lower() == 'lopes':
                query = """
                SELECT p.id, p.nome, el.quantidade 
                FROM produtos p
                LEFT JOIN estoque_lopes el ON p.id = el.produto_id
                """
                params = ()
                
                if produto_id is not None:
                    query += " WHERE p.id = ?"
                    params = (produto_id,)
                
                cursor.execute(query, params)
                for row in cursor.fetchall():
                    resultados.append({
                        'id': row[0],
                        'nome': row[1],
                        'estoque': 'Lopes',
                        'quantidade': row[2] or 0
                    })
            
            if estoque is None or estoque.lower() == 'herbert':
                query = """
                SELECT p.id, p.nome, eh.quantidade 
                FROM produtos p
                LEFT JOIN estoque_herbert eh ON p.id = eh.produto_id
                """
                params = ()
                
                if produto_id is not None:
                    query += " WHERE p.id = ?"
                    params = (produto_id,)
                
                cursor.execute(query, params)
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
    
    def list_products(self) -> List[Tuple[int, str]]:
        """
        Lista todos os produtos cadastrados
        
        Returns:
            Lista de tuplas (id, nome) dos produtos
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT id, nome FROM produtos ORDER BY nome")
            return cursor.fetchall()
        finally:
            conn.close()
    
    def delete_product(self, produto_id: int) -> bool:
        """
        Remove um produto do banco de dados
        
        Args:
            produto_id: ID do produto a ser removido
            
        Returns:
            True se a remoção foi bem-sucedida, False caso contrário
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            # Remover registros de estoque
            cursor.execute("DELETE FROM estoque_lopes WHERE produto_id = ?", (produto_id,))
            cursor.execute("DELETE FROM estoque_herbert WHERE produto_id = ?", (produto_id,))
            
            # Remover produto
            cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
            
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao remover produto: {e}")
            return False
        finally:
            conn.close()

# Exemplo de uso:
if __name__ == "__main__":
    db = EstoqueDB()
    produtos = db.list_products()
    print("Produtos cadastrados:")
    for id, nome in produtos:
        print(f"ID: {id}, Nome: {nome}")
