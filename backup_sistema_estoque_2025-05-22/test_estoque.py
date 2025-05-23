
import estoque_core as e

# Listar produtos
print("Produtos cadastrados:")
produtos = e.list_products()
for p in produtos:
    print(f"ID: {p[0]}, Nome: {p[1]}")

# Verificar estoque combinado
print("\nEstoque combinado:")
estoque = e.get_stock_combined()
for item in estoque[:3]:
    print(f"{item['nome']}: Lopes={item['qtd_lopes']}, Herbert={item['qtd_herbert']}, Total={item['qtd_total']}")

# Adicionar quantidade ao estoque
print("\nAdicionando 10kg de Tilápia ao estoque Lopes...")
e.add_to_stock(1, 10, "lopes")

# Adicionar quantidade ao estoque
print("Adicionando 5kg de Tilápia ao estoque Herbert...")
e.add_to_stock(1, 5, "herbert")

# Verificar estoque da Tilápia
print("\nEstoque de Tilápia após adição:")
tilapa = [item for item in e.get_stock_combined() if item['id'] == 1][0]
print(f"Tilápia: Lopes={tilapa['qtd_lopes']}, Herbert={tilapa['qtd_herbert']}, Total={tilapa['qtd_total']}")

# Remover quantidade do estoque
print("\nRemovendo 3kg de Tilápia do estoque Lopes...")
e.remove_from_stock(1, 3, "lopes")

# Verificar estoque da Tilápia novamente
print("\nEstoque de Tilápia após remoção:")
tilapa = [item for item in e.get_stock_combined() if item['id'] == 1][0]
print(f"Tilápia: Lopes={tilapa['qtd_lopes']}, Herbert={tilapa['qtd_herbert']}, Total={tilapa['qtd_total']}")

# Adicionar novo produto
print("\nAdicionando novo produto 'Salmão' ao catálogo...")
novo_id = e.add_produto_catalogo("Salmão")
print(f"Novo produto adicionado com ID: {novo_id}")

# Verificar se o produto foi adicionado
print("\nLista atualizada de produtos:")
produtos = e.list_products()
for p in produtos:
    print(f"ID: {p[0]}, Nome: {p[1]}")

# Formatar mensagem para Telegram
print("\nExemplo de mensagem formatada para Telegram:")
mensagem = e.format_stock_message(e.get_stock("lopes"), "Estoque Lopes")
print(mensagem)
