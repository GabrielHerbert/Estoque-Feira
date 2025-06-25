
import sqlite3
from typing import List, Dict, Any, Optional, Tuple

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

def registrar_operacao(filial: str, operacao: str, mensagem: str, observacao: str = "") -> None:
    """
    Registra uma operação completa no log
    
    Args:
        filial: Nome da filial
        operacao: Tipo de operação ('entrada', 'saida', 'ajuste')
        mensagem: Mensagem original do usuário
        observacao: Observação adicional (opcional)
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO operacoes 
            (filial, operacao, mensagem, observacao)
            VALUES (?, ?, ?, ?)
        """, (filial, operacao, mensagem, observacao))
        conn.commit()
    except Exception as e:
        print(f"Erro ao registrar operação: {e}")
    finally:
        conn.close()

def add_to_stock(produto_id: int, quantidade: int, filial: str, observacao: str = None) -> bool:
    """
    Adiciona uma quantidade de produto ao estoque
    
    Args:
        produto_id: ID do produto
        quantidade: Quantidade a ser adicionada (em gramas)
        filial: Nome da filial ('lopes' ou 'herbert')
        observacao: Observação adicional (opcional)
        
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
        
        quantidade_anterior = 0
        if resultado:
            quantidade_anterior = resultado[0]
            # Atualizar quantidade
            nova_quantidade = quantidade_anterior + quantidade
            cursor.execute(f"UPDATE {tabela} SET quantidade = ? WHERE produto_id = ?", 
                          (nova_quantidade, produto_id))
        else:
            # Inserir novo registro
            nova_quantidade = quantidade
            cursor.execute(f"INSERT INTO {tabela} (produto_id, quantidade) VALUES (?, ?)", 
                          (produto_id, quantidade))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao adicionar ao estoque: {e}")
        return False
    finally:
        conn.close()

def remove_from_stock(produto_id: int, quantidade: int, filial: str, observacao: str = None) -> bool:
    """
    Remove uma quantidade de produto do estoque
    
    Args:
        produto_id: ID do produto
        quantidade: Quantidade a ser removida (em gramas)
        filial: Nome da filial ('lopes' ou 'herbert')
        observacao: Observação adicional (opcional)
        
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
        
        quantidade_anterior = resultado[0]
        
        # Verificar se há quantidade suficiente
        if quantidade_anterior < quantidade:
            print(f"Quantidade insuficiente no estoque. Disponível: {quantidade_anterior}, Solicitado: {quantidade}")
            return False
        
        # Atualizar quantidade
        nova_quantidade = quantidade_anterior - quantidade
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

def get_logs_movimentacao(filial: Optional[str] = None, produto_id: Optional[int] = None, 
                         limite: int = 50) -> List[Dict[str, Any]]:
    """
    Obtém logs de movimentação do estoque
    
    Args:
        filial: Filtrar por filial (opcional)
        produto_id: Filtrar por produto (opcional)
        limite: Número máximo de registros a retornar
        
    Returns:
        Lista de dicionários com informações dos logs
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        query = """
        SELECT l.id, p.nome, l.filial, l.operacao, l.quantidade, 
               l.quantidade_anterior, l.quantidade_nova, l.data_hora, l.observacao
        FROM logs_movimentacao l
        JOIN produtos p ON l.produto_id = p.id
        WHERE 1=1
        """
        params = []
        
        if filial:
            query += " AND l.filial = ?"
            params.append(filial.lower())
        
        if produto_id:
            query += " AND l.produto_id = ?"
            params.append(produto_id)
        
        query += " ORDER BY l.data_hora DESC LIMIT ?"
        params.append(limite)
        
        cursor.execute(query, params)
        resultados = []
        
        for row in cursor.fetchall():
            resultados.append({
                'id': row[0],
                'produto_nome': row[1],
                'filial': row[2],
                'operacao': row[3],
                'quantidade': row[4],
                'quantidade_anterior': row[5],
                'quantidade_nova': row[6],
                'data_hora': row[7],
                'observacao': row[8]
            })
        
        return resultados
    finally:
        conn.close()

def format_logs_message(logs_data: List[Dict[str, Any]], titulo: str = "Logs de Movimentação") -> str:
    """
    Formata os dados de logs para exibição no Telegram
    
    Args:
        logs_data: Lista de dicionários com informações dos logs
        titulo: Título da mensagem
        
    Returns:
        Mensagem formatada
    """
    if not logs_data:
        return f"*{titulo}*\n\nNenhuma movimentação encontrada."
    
    mensagem = f"*{titulo}*\n\n"
    
    for log in logs_data:
        data_formatada = log['data_hora'][:16].replace('T', ' ')  # Formato: YYYY-MM-DD HH:MM
        operacao_emoji = "➕" if log['operacao'] == 'adicionar' else "➖"
        
        # Converter de gramas para kg para exibição
        quantidade_kg = log['quantidade'] / 1000
        quantidade_anterior_kg = log['quantidade_anterior'] / 1000
        quantidade_nova_kg = log['quantidade_nova'] / 1000
        
        mensagem += f"{operacao_emoji} *{log['produto_nome']}* - {log['filial'].capitalize()}\n"
        mensagem += f"   Quantidade: {quantidade_kg:.3f} kg\n"
        mensagem += f"   {quantidade_anterior_kg:.3f} → {quantidade_nova_kg:.3f} kg\n"
        mensagem += f"   Data: {data_formatada}\n"
        
        if log['observacao']:
            mensagem += f"   Obs: {log['observacao']}\n"
        
        mensagem += "\n"
    
    return mensagem

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
            # Converter de gramas para kg para exibição
            qtd_lopes_kg = item['qtd_lopes'] / 1000
            qtd_herbert_kg = item['qtd_herbert'] / 1000
            qtd_total_kg = item['qtd_total'] / 1000
            
            mensagem += f"{item['id']:<3} {item['nome'][:25]:<25} {qtd_lopes_kg:<8.3f} {qtd_herbert_kg:<8.3f} {qtd_total_kg:<8.3f}\n"
        
        mensagem += "```"
    else:  # Estoque individual
        estoque_atual = estoque_data[0]['estoque'] if estoque_data else ""
        mensagem += f"*Filial: {estoque_atual}*\n\n"
        mensagem += "```\n"
        mensagem += f"{'ID':<3} {'Produto':<25} {'Quantidade':<10}\n"
        mensagem += "-" * 40 + "\n"
        
        for item in estoque_data:
            # Converter de gramas para kg para exibição
            quantidade_kg = item['quantidade'] / 1000
            mensagem += f"{item['id']:<3} {item['nome'][:25]:<25} {quantidade_kg:<10.3f}\n"
        
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

def gerar_relatorio_estoque(filial: str) -> str:
    """
    Gera um relatório de estoque formatado para uma filial específica ou conjunto
    
    Args:
        filial: Nome da filial ('lopes', 'herbert' ou 'conjunto')
        
    Returns:
        String com o relatório formatado
    """
    from datetime import datetime
    
    if filial.lower() not in ['lopes', 'herbert', 'conjunto']:
        raise ValueError("Filial deve ser 'lopes', 'herbert' ou 'conjunto'")
    
    # Obter dados do estoque
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        data_atual = datetime.now().strftime("%d/%m/%Y")
        
        if filial.lower() == 'conjunto':
            # Relatório conjunto
            query = """
            SELECT p.nome, 
                   COALESCE(el.quantidade, 0) as qtd_lopes, 
                   COALESCE(eh.quantidade, 0) as qtd_herbert,
                   COALESCE(el.quantidade, 0) + COALESCE(eh.quantidade, 0) as qtd_total
            FROM produtos p
            LEFT JOIN estoque_lopes el ON p.id = el.produto_id
            LEFT JOIN estoque_herbert eh ON p.id = eh.produto_id
            WHERE COALESCE(el.quantidade, 0) + COALESCE(eh.quantidade, 0) > 0
            ORDER BY p.nome
            """
            
            cursor.execute(query)
            produtos = cursor.fetchall()
            
            relatorio = f"ESTOQUE CONJUNTO ({data_atual})\n\n"
            
            for nome_produto, qtd_lopes, qtd_herbert, qtd_total in produtos:
                # Converter de gramas para kg e formatar
                qtd_total_kg = qtd_total / 1000
                qtd_lopes_kg = qtd_lopes / 1000
                qtd_herbert_kg = qtd_herbert / 1000
                
                if qtd_total_kg == int(qtd_total_kg):
                    qtd_total_str = str(int(qtd_total_kg))
                else:
                    qtd_total_str = f"{qtd_total_kg:.3f}".rstrip('0').rstrip('.')
                
                relatorio += f"{qtd_total_str} {nome_produto.lower()}"
                
                # Adicionar detalhes por filial se houver diferença
                if qtd_lopes > 0 and qtd_herbert > 0:
                    lopes_str = f"{qtd_lopes_kg:.3f}".rstrip('0').rstrip('.') if qtd_lopes_kg != int(qtd_lopes_kg) else str(int(qtd_lopes_kg))
                    herbert_str = f"{qtd_herbert_kg:.3f}".rstrip('0').rstrip('.') if qtd_herbert_kg != int(qtd_herbert_kg) else str(int(qtd_herbert_kg))
                    relatorio += f" (Lopes: {lopes_str}, Herbert: {herbert_str})"
                elif qtd_lopes > 0:
                    relatorio += " (apenas Lopes)"
                elif qtd_herbert > 0:
                    relatorio += " (apenas Herbert)"
                
                relatorio += "\n"
        else:
            # Relatório individual
            tabela = f"estoque_{filial.lower()}"
            query = f"""
            SELECT p.nome, es.quantidade
            FROM produtos p
            JOIN {tabela} es ON p.id = es.produto_id
            WHERE es.quantidade > 0
            ORDER BY p.nome
            """
            
            cursor.execute(query)
            produtos = cursor.fetchall()
            
            nome_filial = filial.upper()
            relatorio = f"ESTOQUE {nome_filial} ({data_atual})\n\n"
            
            for nome_produto, quantidade in produtos:
                # Converter de gramas para kg e formatar
                quantidade_kg = quantidade / 1000
                if quantidade_kg == int(quantidade_kg):
                    quantidade_str = str(int(quantidade_kg))
                else:
                    quantidade_str = f"{quantidade_kg:.3f}".rstrip('0').rstrip('.')
                
                relatorio += f"{quantidade_str} {nome_produto.lower()}\n"
        
        return relatorio.strip()
        
    finally:
        conn.close()

def remover_produto_catalogo(produto_id: int) -> bool:
    """
    Remove um produto do catálogo e de todos os estoques
    
    Args:
        produto_id: ID do produto a ser removido
        
    Returns:
        True se a operação foi bem-sucedida, False caso contrário
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Verificar se o produto existe
        cursor.execute("SELECT nome FROM produtos WHERE id = ?", (produto_id,))
        produto = cursor.fetchone()
        
        if not produto:
            print(f"Produto com ID {produto_id} não encontrado")
            return False
        
        nome_produto = produto[0]
        
        # Remover do estoque Lopes
        cursor.execute("DELETE FROM estoque_lopes WHERE produto_id = ?", (produto_id,))
        
        # Remover do estoque Herbert
        cursor.execute("DELETE FROM estoque_herbert WHERE produto_id = ?", (produto_id,))
        
        # Remover do catálogo de produtos
        cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
        
        conn.commit()
        print(f"Produto '{nome_produto}' (ID: {produto_id}) removido com sucesso do sistema")
        return True
        
    except Exception as e:
        print(f"Erro ao remover produto: {e}")
        return False
    finally:
        conn.close()

def listar_produtos_com_id() -> List[Dict[str, Any]]:
    """
    Lista todos os produtos com seus IDs e quantidades em estoque
    
    Returns:
        Lista de dicionários com informações dos produtos
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
        produtos = []
        
        for row in cursor.fetchall():
            produtos.append({
                'id': row[0],
                'nome': row[1],
                'qtd_lopes': row[2],
                'qtd_herbert': row[3],
                'qtd_total': row[4]
            })
        
        return produtos
        
    finally:
        conn.close()

def processar_mensagem_estoque(mensagem: str, filial: str, operacao: str, itens_processados: List[Dict]) -> bool:
    """
    Processa uma mensagem de estoque e registra a operação completa
    
    Args:
        mensagem: Mensagem original do usuário
        filial: Nome da filial
        operacao: Tipo de operação ('entrada' ou 'saida')
        itens_processados: Lista de itens processados pelo text_processor
        
    Returns:
        True se todas as operações foram bem-sucedidas
    """
    sucesso_total = True
    
    # Processar cada item
    for item in itens_processados:
        produto_id = item['produto_id']
        quantidade = item['quantidade']
        observacao = item.get('observacao', None)
        
        if operacao == 'entrada':
            resultado = add_to_stock(produto_id, quantidade, filial, observacao)
        else:  # saida
            resultado = remove_from_stock(produto_id, quantidade, filial, observacao)
        
        if not resultado:
            sucesso_total = False
    
    # Registrar a operação completa no log
    if sucesso_total:
        registrar_operacao(filial, operacao, mensagem)
    
    return sucesso_total

def get_operacoes(filial: Optional[str] = None, limite: int = 20) -> List[Dict[str, Any]]:
    """
    Obtém as operações registradas
    
    Args:
        filial: Nome da filial (opcional, se None retorna todas)
        limite: Número máximo de registros a retornar
        
    Returns:
        Lista de dicionários com as operações
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        query = "SELECT filial, operacao, mensagem, data_hora, observacao FROM operacoes"
        params = []
        
        if filial:
            query += " WHERE filial = ?"
            params.append(filial)
        
        query += " ORDER BY data_hora DESC LIMIT ?"
        params.append(limite)
        
        cursor.execute(query, params)
        
        operacoes = []
        for row in cursor.fetchall():
            operacoes.append({
                'filial': row[0],
                'operacao': row[1],
                'mensagem': row[2],
                'data_hora': row[3],
                'observacao': row[4]
            })
        
        return operacoes
        
    finally:
        conn.close()

def format_operacoes_message(operacoes: List[Dict[str, Any]], titulo: str) -> str:
    """
    Formata as operações para exibição no Telegram
    
    Args:
        operacoes: Lista de operações
        titulo: Título da mensagem
        
    Returns:
        String formatada para o Telegram
    """
    if not operacoes:
        return f"*{titulo}*\n\nNenhuma operação encontrada."
    
    mensagem = f"*{titulo}*\n\n"
    
    for op in operacoes:
        data_formatada = op['data_hora'][:16].replace('T', ' ')  # YYYY-MM-DD HH:MM
        filial_emoji = "🏪" if op['filial'].lower() == 'lopes' else "🏬"
        operacao_emoji = "📥" if op['operacao'] == 'entrada' else "📤"
        
        mensagem += f"{filial_emoji} *{op['filial'].capitalize()}* {operacao_emoji} {op['operacao'].capitalize()}\n"
        mensagem += f"📅 {data_formatada}\n"
        mensagem += f"📝 {op['mensagem']}\n"
        
        if op['observacao']:
            mensagem += f"💬 {op['observacao']}\n"
        
        mensagem += "\n"
    
    return mensagem.strip()

# Redefinir as funções de logs para usar o novo sistema
def get_logs_movimentacao(filial: Optional[str] = None, produto_id: Optional[int] = None, 
                         limite: int = 50) -> List[Dict[str, Any]]:
    """
    Função de compatibilidade - agora usa o sistema de operações
    """
    return get_operacoes(filial, limite)

def format_logs_message(logs: List[Dict[str, Any]], titulo: str) -> str:
    """
    Função de compatibilidade - redireciona para format_operacoes_message
    """
    return format_operacoes_message(logs, titulo)
