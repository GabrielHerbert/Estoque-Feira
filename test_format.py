#!/usr/bin/env python3
import sys
import traceback

# Função de formatação similar à do estoque_core.py
def format_stock_message(estoque_data, titulo="Estoque Atual"):
    """
    Formata os dados de estoque para exibição no Telegram
    
    Args:
        estoque_data: Lista de dicionários com informações de estoque
        titulo: Título da mensagem
        
    Returns:
        Mensagem formatada
    """
    try:
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
    except Exception as e:
        print(f"Erro ao formatar mensagem: {e}")
        traceback.print_exc()
        return f"Erro ao formatar mensagem: {e}"

# Teste com dados de exemplo
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
mensagem = format_stock_message(estoque_data, "Teste de Estoque")
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
mensagem_combinada = format_stock_message(estoque_combinado, "Teste de Estoque Combinado")
print(mensagem_combinada)
