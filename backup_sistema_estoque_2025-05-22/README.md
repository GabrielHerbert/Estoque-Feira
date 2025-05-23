# Sistema de Controle de Estoque com Bot Telegram

Este sistema permite gerenciar o estoque de produtos em duas filiais (Lopes e Herbert) através de um bot do Telegram.

## Estrutura do Projeto

- `estoque.db`: Banco de dados SQLite com as tabelas de produtos e estoques
- `db_setup.py`: Script para configuração inicial do banco de dados
- `estoque_db.py`: Classe para interação com o banco de dados (versão original)
- `estoque_core.py`: Módulo com funções para gerenciamento do estoque (usado pelo bot)
- `test_estoque.py`: Script para testar as funcionalidades do módulo

## Funcionalidades Implementadas

O módulo `estoque_core.py` implementa as seguintes funcionalidades:

1. **Adicionar produtos ao catálogo**
   - `add_produto_catalogo(nome)`: Adiciona um novo produto ao catálogo

2. **Gerenciar estoque**
   - `add_to_stock(produto_id, quantidade, filial)`: Adiciona quantidade ao estoque
   - `remove_from_stock(produto_id, quantidade, filial)`: Remove quantidade do estoque

3. **Visualizar estoque**
   - `get_stock(filial)`: Obtém o estoque de uma filial específica
   - `get_stock_combined()`: Obtém o estoque combinado das duas filiais

4. **Gerenciar produtos**
   - `list_products()`: Lista todos os produtos cadastrados
   - `get_product_by_id(produto_id)`: Obtém um produto pelo ID
   - `get_product_by_name(nome)`: Obtém um produto pelo nome
   - `search_products(termo)`: Busca produtos pelo nome

5. **Formatação para Telegram**
   - `format_stock_message(estoque_data, titulo)`: Formata os dados de estoque para exibição no Telegram

## Estrutura do Banco de Dados

### Tabela `produtos`
- `id`: ID do produto (chave primária)
- `nome`: Nome do produto (único)

### Tabelas `estoque_lopes` e `estoque_herbert`
- `id`: ID do registro (chave primária)
- `produto_id`: ID do produto (chave estrangeira)
- `quantidade`: Quantidade em estoque

## Exemplo de Uso

```python
import estoque_core as e

# Listar produtos
produtos = e.list_products()
for p in produtos:
    print(f"ID: {p[0]}, Nome: {p[1]}")

# Adicionar produto ao estoque
e.add_to_stock(1, 10, "lopes")  # Adiciona 10kg de Tilápia ao estoque Lopes

# Remover produto do estoque
e.remove_from_stock(1, 3, "lopes")  # Remove 3kg de Tilápia do estoque Lopes

# Visualizar estoque
estoque = e.get_stock_combined()
for item in estoque:
    print(f"{item['nome']}: Lopes={item['qtd_lopes']}, Herbert={item['qtd_herbert']}, Total={item['qtd_total']}")

# Adicionar novo produto
novo_id = e.add_produto_catalogo("Salmão")
```

## Integração com Bot do Telegram

O módulo `estoque_core.py` foi projetado para ser facilmente integrado com um bot do Telegram. A função `format_stock_message()` formata os dados de estoque para exibição no Telegram com formatação Markdown.

Para integrar com o bot do Telegram, basta importar o módulo e chamar as funções conforme necessário.
