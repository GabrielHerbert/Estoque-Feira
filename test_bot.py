#!/usr/bin/env python3
import estoque_core

# Teste da função format_stock_message com dados de exemplo
estoque_data = [
    {
        'id': 1,
        'nome': 'Tilápia',
        'estoque': 'Lopes',
        'quantidade': 10.5
    },
    {
        'id': 2,
        'nome': 'Camarão',
        'estoque': 'Lopes',
        'quantidade': 5.25
    }
]

# Teste da formatação com 3 casas decimais
print("Testando formatação de estoque:")
mensagem = estoque_core.format_stock_message(estoque_data, "Teste de Estoque")
print(mensagem)

# Teste de estoque combinado
estoque_combinado = [
    {
        'id': 1,
        'nome': 'Tilápia',
        'qtd_lopes': 10.5,
        'qtd_herbert': 8.75,
        'qtd_total': 19.25
    },
    {
        'id': 2,
        'nome': 'Camarão',
        'qtd_lopes': 5.25,
        'qtd_herbert': 3.0,
        'qtd_total': 8.25
    }
]

print("\nTestando formatação de estoque combinado:")
mensagem_combinada = estoque_core.format_stock_message(estoque_combinado, "Teste de Estoque Combinado")
print(mensagem_combinada)
