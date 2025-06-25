#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import re
from typing import Dict, List, Any, Optional, Union, Tuple
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    CallbackQueryHandler,
    ConversationHandler,
    filters, 
    ContextTypes
)

# Importando os módulos do sistema de estoque
import estoque_core
import text_processor

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Estados para o ConversationHandler
(
    MENU_PRINCIPAL, 
    ESTOQUE_LOPES, 
    ESTOQUE_HERBERT, 
    ESTOQUE_CONJUNTO,
    ADICIONAR_PRODUTO_CATALOGO,
    REMOVER_PRODUTO,
    ADICIONAR_PRODUTOS_LOPES,
    ADICIONAR_PRODUTOS_HERBERT,
    RETIRAR_PRODUTOS_LOPES,
    RETIRAR_PRODUTOS_HERBERT,
    VER_LOGS,
    RELATORIO,
) = range(12)

# Token do bot
TOKEN = "7952211429:AAHP8UFrrmd_E96QIZQNwZigd5zjK8VN5QY"

# Lista de IDs de usuários autorizados a usar comandos administrativos
ADMIN_IDS = [
    123456789,  # Substitua pelo ID real do administrador
    987654321   # Adicione mais IDs conforme necessário
]

# Funções auxiliares
def criar_menu_principal() -> InlineKeyboardMarkup:
    """Cria o menu principal com botões para as opções disponíveis"""
    keyboard = [
        [
            InlineKeyboardButton("Estoque Lopes", callback_data="estoque_lopes"),
            InlineKeyboardButton("Estoque Herbert", callback_data="estoque_herbert")
        ],
        [
            InlineKeyboardButton("Estoque Conjunto", callback_data="estoque_conjunto")
        ],
        [
            InlineKeyboardButton("Ver Logs", callback_data="ver_logs"),
            InlineKeyboardButton("📊 Relatório", callback_data="relatorio")
        ],
        [
            InlineKeyboardButton("Cadastrar Novo Produto", callback_data="adicionar_produto")
        ],
        [
            InlineKeyboardButton("🗑️ Remover Produto Cadastrado", callback_data="remover_produto")
        ],
        [
            InlineKeyboardButton("Encerrar", callback_data="encerrar")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def criar_menu_estoque(filial: str) -> InlineKeyboardMarkup:
    """Cria o menu de opções para um estoque específico"""
    keyboard = [
        [
            InlineKeyboardButton("Adicionar Produtos", callback_data=f"adicionar_{filial.lower()}"),
            InlineKeyboardButton("Retirar Produtos", callback_data=f"retirar_{filial.lower()}")
        ],
        [
            InlineKeyboardButton("Ver Logs desta Filial", callback_data=f"logs_{filial.lower()}")
        ],
        [
            InlineKeyboardButton("Voltar", callback_data="voltar_menu_principal")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def criar_menu_operacao_continua(operacao: str, filial: str) -> InlineKeyboardMarkup:
    """Cria o menu para operações contínuas (adicionar/retirar)"""
    acao = "Adicionando" if operacao == "adicionar" else "Retirando"
    keyboard = [
        [
            InlineKeyboardButton(f"Parar de {acao}", callback_data=f"parar_{operacao}_{filial}")
        ],
        [
            InlineKeyboardButton("Ver Estoque Atual", callback_data=f"ver_estoque_{filial}")
        ],
        [
            InlineKeyboardButton("Voltar ao Menu", callback_data="voltar_menu_principal")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

async def processar_lista_produtos(update: Update, context: ContextTypes.DEFAULT_TYPE, operacao: str, filial: str) -> None:
    """
    Processa uma lista de produtos enviada pelo usuário
    
    Args:
        update: Objeto Update do Telegram
        context: Contexto do bot
        operacao: Tipo de operação ('adicionar' ou 'retirar')
        filial: Nome da filial ('lopes' ou 'herbert')
    """
    texto = update.message.text
    
    # Processar o texto para identificar produtos e quantidades
    itens_processados = text_processor.process_text(texto)
    
    if not itens_processados:
        await update.message.reply_text(
            "Não consegui identificar nenhum produto na sua mensagem. Por favor, tente novamente com o formato correto.\n"
            "Exemplo: '2.5kg tilápia' ou '3 camarão limpo g'",
            reply_markup=criar_menu_operacao_continua(operacao, filial)
        )
        return
    
    # Usar o novo sistema de processamento de mensagem
    tipo_operacao = 'entrada' if operacao == 'adicionar' else 'saida'
    sucesso = estoque_core.processar_mensagem_estoque(texto, filial, tipo_operacao, itens_processados)
    
    # Preparar mensagem de confirmação
    mensagem = f"*{'Adicionando' if operacao == 'adicionar' else 'Retirando'} produtos no estoque {filial.capitalize()}:*\n\n"
    
    if sucesso:
        mensagem += "✅ *Operação realizada com sucesso!*\n\n"
        mensagem += f"📝 Registrado: {texto}\n"
    else:
        mensagem += f"❌ *Erro na operação*\n\n"
    
    # Adicionar instruções para continuar
    acao = "adicionar" if operacao == 'adicionar' else "retirar"
    mensagem += f"\n💡 *Modo contínuo ativo*\nVocê pode continuar enviando produtos para {acao}.\nUse os botões abaixo para parar ou ver o estoque atual."
    
    # Enviar mensagem de confirmação com menu de operação contínua
    await update.message.reply_text(
        mensagem, 
        parse_mode='Markdown',
        reply_markup=criar_menu_operacao_continua(operacao, filial)
    )

# Handlers para comandos e callbacks

async def listar_estoque(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Responde com a lista completa de produtos e quantidades em estoque"""
    # Obter dados do estoque combinado
    estoque_data = estoque_core.get_stock_combined()
    
    # Formatar a mensagem com os dados do estoque
    mensagem = estoque_core.format_stock_message(estoque_data, "Estoque Completo")
    
    # Enviar a mensagem formatada
    await update.message.reply_text(
        mensagem,
        parse_mode='Markdown'
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Inicia o bot e mostra o menu principal"""
    await update.message.reply_text(
        "Bem-vindo ao Sistema de Estoque! Escolha uma opção:",
        reply_markup=criar_menu_principal()
    )
    return MENU_PRINCIPAL

async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Processa os callbacks do menu principal"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "voltar_menu_principal":
        await query.edit_message_text(
            "Escolha uma opção:",
            reply_markup=criar_menu_principal()
        )
        return MENU_PRINCIPAL
    
    elif query.data == "estoque_lopes":
        # Mostrar estoque Lopes
        estoque_data = estoque_core.get_stock("lopes")
        mensagem = estoque_core.format_stock_message(estoque_data, "Estoque Lopes")
        await query.edit_message_text(
            text=mensagem,
            parse_mode='Markdown',
            reply_markup=criar_menu_estoque("lopes")
        )
        return ESTOQUE_LOPES
    
    elif query.data == "estoque_herbert":
        # Mostrar estoque Herbert
        estoque_data = estoque_core.get_stock("herbert")
        mensagem = estoque_core.format_stock_message(estoque_data, "Estoque Herbert")
        await query.edit_message_text(
            text=mensagem,
            parse_mode='Markdown',
            reply_markup=criar_menu_estoque("herbert")
        )
        return ESTOQUE_HERBERT
    
    elif query.data == "estoque_conjunto":
        # Mostrar estoque conjunto
        estoque_data = estoque_core.get_stock_combined()
        mensagem = estoque_core.format_stock_message(estoque_data, "Estoque Conjunto")
        keyboard = [
            [InlineKeyboardButton("Voltar", callback_data="voltar_menu_principal")]
        ]
        await query.edit_message_text(
            text=mensagem,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return ESTOQUE_CONJUNTO
    
    elif query.data == "ver_logs":
        # Mostrar logs gerais
        try:
            logs_data = estoque_core.get_operacoes(limite=20)
            mensagem = estoque_core.format_operacoes_message(logs_data, "Últimas 20 Operações")
        except Exception as e:
            mensagem = f"*❌ Erro ao carregar logs:*\n{str(e)}"
        
        keyboard = [
            [InlineKeyboardButton("Voltar", callback_data="voltar_menu_principal")]
        ]
        await query.edit_message_text(
            text=mensagem,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return VER_LOGS
    
    elif query.data == "adicionar_produto":
        await query.edit_message_text(
            "Por favor, digite o nome do novo produto que deseja adicionar ao catálogo:",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Cancelar", callback_data="voltar_menu_principal")
            ]])
        )
        return ADICIONAR_PRODUTO_CATALOGO
    
    elif query.data == "remover_produto":
        # Listar produtos com IDs para remoção
        try:
            produtos = estoque_core.listar_produtos_com_id()
            if not produtos:
                await query.edit_message_text(
                    "❌ Nenhum produto encontrado no catálogo.",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("Voltar", callback_data="voltar_menu_principal")
                    ]])
                )
                return MENU_PRINCIPAL
            
            mensagem = "*🗑️ Remover Produto do Catálogo*\n\n"
            mensagem += "Lista de produtos cadastrados:\n\n"
            
            for produto in produtos[:20]:  # Limitar a 20 produtos
                qtd_total_kg = produto['qtd_total'] / 1000
                qtd_str = f"{qtd_total_kg:.3f}".rstrip('0').rstrip('.') if qtd_total_kg != int(qtd_total_kg) else str(int(qtd_total_kg))
                mensagem += f"ID {produto['id']}: {produto['nome']} ({qtd_str}kg)\n"
            
            if len(produtos) > 20:
                mensagem += f"\n... e mais {len(produtos) - 20} produtos"
            
            mensagem += "\n💡 Digite o ID do produto que deseja remover:"
            
            await query.edit_message_text(
                mensagem,
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("Cancelar", callback_data="voltar_menu_principal")
                ]])
            )
            return REMOVER_PRODUTO
            
        except Exception as e:
            await query.edit_message_text(
                f"❌ Erro ao listar produtos: {str(e)}",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("Voltar", callback_data="voltar_menu_principal")
                ]])
            )
            return MENU_PRINCIPAL
    
    elif query.data == "relatorio":
        keyboard = [
            [InlineKeyboardButton("📊 Lopes", callback_data="relatorio_lopes")],
            [InlineKeyboardButton("📊 Herbert", callback_data="relatorio_herbert")],
            [InlineKeyboardButton("📊 Conjunto", callback_data="relatorio_conjunto")],
            [InlineKeyboardButton("🔙 Menu Principal", callback_data="voltar_menu_principal")]
        ]
        await query.edit_message_text(
            "*📊 Relatório de Estoque*\n\n"
            "Selecione o tipo de relatório:",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return RELATORIO
    
    elif query.data == "encerrar":
        await query.edit_message_text("Sistema de estoque encerrado. Digite /start para iniciar novamente.")
        return ConversationHandler.END
    
    return MENU_PRINCIPAL

async def estoque_lopes_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Processa os callbacks do menu do estoque Lopes"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "estoque_lopes":
        # Mostrar estoque Lopes novamente (usado pelo botão voltar dos logs)
        estoque_data = estoque_core.get_stock("lopes")
        mensagem = estoque_core.format_stock_message(estoque_data, "Estoque Lopes")
        await query.edit_message_text(
            text=mensagem,
            parse_mode='Markdown',
            reply_markup=criar_menu_estoque("lopes")
        )
        return ESTOQUE_LOPES
    
    elif query.data == "adicionar_lopes":
        await query.edit_message_text(
            "🔄 *Modo Contínuo Ativado*\n\n"
            "Envie a lista de produtos a serem adicionados ao estoque Lopes.\n"
            "Formato: quantidade produto\n"
            "Exemplo:\n"
            "2.5kg tilápia\n"
            "3 camarão limpo g\n"
            "1.2kg pescada amarela\n\n"
            "💡 Você pode enviar várias mensagens. Use o botão 'Parar de Adicionar' quando terminar.",
            parse_mode='Markdown',
            reply_markup=criar_menu_operacao_continua("adicionar", "lopes")
        )
        return ADICIONAR_PRODUTOS_LOPES
    
    elif query.data == "retirar_lopes":
        await query.edit_message_text(
            "🔄 *Modo Contínuo Ativado*\n\n"
            "Envie a lista de produtos a serem retirados do estoque Lopes.\n"
            "Formato: quantidade produto\n"
            "Exemplo:\n"
            "2.5kg tilápia\n"
            "3 camarão limpo g\n"
            "1.2kg pescada amarela\n\n"
            "💡 Você pode enviar várias mensagens. Use o botão 'Parar de Retirar' quando terminar.",
            parse_mode='Markdown',
            reply_markup=criar_menu_operacao_continua("retirar", "lopes")
        )
        return RETIRAR_PRODUTOS_LOPES
    
    elif query.data == "logs_lopes":
        # Mostrar logs da filial Lopes
        try:
            logs_data = estoque_core.get_operacoes(filial="lopes", limite=15)
            mensagem = estoque_core.format_operacoes_message(logs_data, "Últimas Operações - Lopes")
        except Exception as e:
            mensagem = f"*❌ Erro ao carregar logs:*\n{str(e)}"
        
        keyboard = [
            [InlineKeyboardButton("Voltar", callback_data="estoque_lopes")]
        ]
        await query.edit_message_text(
            text=mensagem,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return ESTOQUE_LOPES
    
    elif query.data.startswith("parar_"):
        # Parar operação contínua e voltar ao menu do estoque
        parts = query.data.split("_")
        operacao = parts[1]  # adicionar ou retirar
        filial = parts[2]    # lopes ou herbert
        
        # Mensagem de confirmação
        acao_passado = "adição" if operacao == "adicionar" else "retirada"
        mensagem_confirmacao = f"✅ *Operação de {acao_passado} finalizada!*\n\n"
        mensagem_confirmacao += f"Todas as movimentações foram registradas nos logs.\n\n"
        
        # Mostrar estoque atualizado
        estoque_data = estoque_core.get_stock(filial)
        mensagem_estoque = estoque_core.format_stock_message(estoque_data, f"Estoque Atual - {filial.capitalize()}")
        
        mensagem_final = mensagem_confirmacao + mensagem_estoque
        
        await query.edit_message_text(
            text=mensagem_final,
            parse_mode='Markdown',
            reply_markup=criar_menu_estoque(filial)
        )
        return ESTOQUE_LOPES if filial == "lopes" else ESTOQUE_HERBERT
    
    elif query.data.startswith("ver_estoque_"):
        # Mostrar estoque atual durante operação contínua
        filial = query.data.split("_")[2]
        estoque_data = estoque_core.get_stock(filial)
        mensagem = estoque_core.format_stock_message(estoque_data, f"Estoque Atual - {filial.capitalize()}")
        
        # Enviar como mensagem popup (alert)
        await query.answer(f"📊 Estoque {filial.capitalize()}\n\nVeja a mensagem completa abaixo.", show_alert=True)
        
        # Enviar mensagem completa do estoque
        await query.message.reply_text(
            mensagem,
            parse_mode='Markdown'
        )
        
        # Determinar o estado correto baseado na operação atual
        if "adicionar" in str(context.user_data.get('operacao_atual', '')):
            return ADICIONAR_PRODUTOS_LOPES if filial == "lopes" else ADICIONAR_PRODUTOS_HERBERT
        else:
            return RETIRAR_PRODUTOS_LOPES if filial == "lopes" else RETIRAR_PRODUTOS_HERBERT
    
    elif query.data == "voltar_menu_principal":
        await query.edit_message_text(
            "Escolha uma opção:",
            reply_markup=criar_menu_principal()
        )
        return MENU_PRINCIPAL
    
    return ESTOQUE_LOPES

async def estoque_herbert_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Processa os callbacks do menu do estoque Herbert"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "estoque_herbert":
        # Mostrar estoque Herbert novamente
        estoque_data = estoque_core.get_stock("herbert")
        mensagem = estoque_core.format_stock_message(estoque_data, "Estoque Herbert")
        await query.edit_message_text(
            text=mensagem,
            parse_mode='Markdown',
            reply_markup=criar_menu_estoque("herbert")
        )
        return ESTOQUE_HERBERT
    
    elif query.data == "adicionar_herbert":
        await query.edit_message_text(
            "🔄 *Modo Contínuo Ativado*\n\n"
            "Envie a lista de produtos a serem adicionados ao estoque Herbert.\n"
            "Formato: quantidade produto\n"
            "Exemplo:\n"
            "2.5kg tilápia\n"
            "3 camarão limpo g\n"
            "1.2kg pescada amarela\n\n"
            "💡 Você pode enviar várias mensagens. Use o botão 'Parar de Adicionar' quando terminar.",
            parse_mode='Markdown',
            reply_markup=criar_menu_operacao_continua("adicionar", "herbert")
        )
        return ADICIONAR_PRODUTOS_HERBERT
    
    elif query.data == "retirar_herbert":
        await query.edit_message_text(
            "🔄 *Modo Contínuo Ativado*\n\n"
            "Envie a lista de produtos a serem retirados do estoque Herbert.\n"
            "Formato: quantidade produto\n"
            "Exemplo:\n"
            "2.5kg tilápia\n"
            "3 camarão limpo g\n"
            "1.2kg pescada amarela\n\n"
            "💡 Você pode enviar várias mensagens. Use o botão 'Parar de Retirar' quando terminar.",
            parse_mode='Markdown',
            reply_markup=criar_menu_operacao_continua("retirar", "herbert")
        )
        return RETIRAR_PRODUTOS_HERBERT
    
    elif query.data == "logs_herbert":
        # Mostrar logs da filial Herbert
        try:
            logs_data = estoque_core.get_operacoes(filial="herbert", limite=15)
            mensagem = estoque_core.format_operacoes_message(logs_data, "Últimas Operações - Herbert")
        except Exception as e:
            mensagem = f"*❌ Erro ao carregar logs:*\n{str(e)}"
        
        keyboard = [
            [InlineKeyboardButton("Voltar", callback_data="estoque_herbert")]
        ]
        await query.edit_message_text(
            text=mensagem,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return ESTOQUE_HERBERT
    
    elif query.data.startswith("parar_"):
        # Parar operação contínua e voltar ao menu do estoque
        parts = query.data.split("_")
        operacao = parts[1]  # adicionar ou retirar
        filial = parts[2]    # lopes ou herbert
        
        # Mensagem de confirmação
        acao_passado = "adição" if operacao == "adicionar" else "retirada"
        mensagem_confirmacao = f"✅ *Operação de {acao_passado} finalizada!*\n\n"
        mensagem_confirmacao += f"Todas as movimentações foram registradas nos logs.\n\n"
        
        # Mostrar estoque atualizado
        estoque_data = estoque_core.get_stock(filial)
        mensagem_estoque = estoque_core.format_stock_message(estoque_data, f"Estoque Atual - {filial.capitalize()}")
        
        mensagem_final = mensagem_confirmacao + mensagem_estoque
        
        await query.edit_message_text(
            text=mensagem_final,
            parse_mode='Markdown',
            reply_markup=criar_menu_estoque(filial)
        )
        return ESTOQUE_LOPES if filial == "lopes" else ESTOQUE_HERBERT
    
    elif query.data.startswith("ver_estoque_"):
        # Mostrar estoque atual durante operação contínua
        filial = query.data.split("_")[2]
        estoque_data = estoque_core.get_stock(filial)
        mensagem = estoque_core.format_stock_message(estoque_data, f"Estoque Atual - {filial.capitalize()}")
        
        # Enviar como mensagem popup (alert)
        await query.answer(f"📊 Estoque {filial.capitalize()}\n\nVeja a mensagem completa abaixo.", show_alert=True)
        
        # Enviar mensagem completa do estoque
        await query.message.reply_text(
            mensagem,
            parse_mode='Markdown'
        )
        
        # Determinar o estado correto baseado na operação atual
        if "adicionar" in str(context.user_data.get('operacao_atual', '')):
            return ADICIONAR_PRODUTOS_LOPES if filial == "lopes" else ADICIONAR_PRODUTOS_HERBERT
        else:
            return RETIRAR_PRODUTOS_LOPES if filial == "lopes" else RETIRAR_PRODUTOS_HERBERT
    
    elif query.data == "voltar_menu_principal":
        await query.edit_message_text(
            "Escolha uma opção:",
            reply_markup=criar_menu_principal()
        )
        return MENU_PRINCIPAL
    
    return ESTOQUE_HERBERT

async def estoque_conjunto_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Processa os callbacks do menu do estoque conjunto"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "voltar_menu_principal":
        await query.edit_message_text(
            "Escolha uma opção:",
            reply_markup=criar_menu_principal()
        )
        return MENU_PRINCIPAL
    
    return ESTOQUE_CONJUNTO

async def ver_logs_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Processa os callbacks da tela de logs"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "voltar_menu_principal" or query.data == "voltar":
        await query.edit_message_text(
            "Escolha uma opção:",
            reply_markup=criar_menu_principal()
        )
        return MENU_PRINCIPAL
    
    return VER_LOGS

async def processar_remocao_produto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Processa a remoção de um produto do catálogo"""
    try:
        produto_id = int(update.message.text.strip())
        
        # Tentar remover o produto
        sucesso = estoque_core.remover_produto_catalogo(produto_id)
        
        if sucesso:
            await update.message.reply_text(
                f"✅ *Produto removido com sucesso!*\n\n"
                f"O produto com ID {produto_id} foi removido do catálogo e de todos os estoques.",
                parse_mode='Markdown',
                reply_markup=criar_menu_principal()
            )
        else:
            await update.message.reply_text(
                f"❌ *Erro ao remover produto*\n\n"
                f"Produto com ID {produto_id} não foi encontrado.",
                parse_mode='Markdown',
                reply_markup=criar_menu_principal()
            )
        
        return MENU_PRINCIPAL
        
    except ValueError:
        await update.message.reply_text(
            "❌ *ID inválido*\n\n"
            "Por favor, digite apenas o número do ID do produto.",
            parse_mode='Markdown'
        )
        return REMOVER_PRODUTO
    except Exception as e:
        await update.message.reply_text(
            f"❌ *Erro inesperado:* {str(e)}",
            parse_mode='Markdown',
            reply_markup=criar_menu_principal()
        )
        return MENU_PRINCIPAL

async def adicionar_produto_catalogo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Adiciona um novo produto ao catálogo"""
    nome_produto = update.message.text.strip()
    
    # Adicionar o produto ao catálogo
    produto_id = estoque_core.add_produto_catalogo(nome_produto)
    
    if produto_id > 0:
        await update.message.reply_text(
            f"✅ Produto '{nome_produto}' adicionado com sucesso ao catálogo (ID: {produto_id}).",
            reply_markup=criar_menu_principal()
        )
    else:
        await update.message.reply_text(
            f"❌ Erro ao adicionar o produto '{nome_produto}' ao catálogo.",
            reply_markup=criar_menu_principal()
        )
    
    return MENU_PRINCIPAL

async def adicionar_produtos_lopes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Processa a lista de produtos a serem adicionados ao estoque Lopes"""
    await processar_lista_produtos(update, context, 'adicionar', 'lopes')
    return ADICIONAR_PRODUTOS_LOPES  # Mantém no mesmo estado para operação contínua

async def adicionar_produtos_herbert(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Processa a lista de produtos a serem adicionados ao estoque Herbert"""
    await processar_lista_produtos(update, context, 'adicionar', 'herbert')
    return ADICIONAR_PRODUTOS_HERBERT  # Mantém no mesmo estado para operação contínua

async def retirar_produtos_lopes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Processa a lista de produtos a serem retirados do estoque Lopes"""
    await processar_lista_produtos(update, context, 'retirar', 'lopes')
    return RETIRAR_PRODUTOS_LOPES  # Mantém no mesmo estado para operação contínua

async def retirar_produtos_herbert(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Processa a lista de produtos a serem retirados do estoque Herbert"""
    await processar_lista_produtos(update, context, 'retirar', 'herbert')
    return RETIRAR_PRODUTOS_HERBERT  # Mantém no mesmo estado para operação contínua

async def gerar_relatorio(update: Update, context: ContextTypes.DEFAULT_TYPE, filial: str) -> None:
    """
    Gera e envia o relatório de estoque para uma filial
    """
    query = update.callback_query
    await query.answer()
    
    try:
        relatorio = estoque_core.gerar_relatorio_estoque(filial)
        
        # Enviar como arquivo de texto
        from io import BytesIO
        from datetime import datetime
        arquivo = BytesIO(relatorio.encode('utf-8'))
        arquivo.name = f"estoque_{filial.lower()}_{datetime.now().strftime('%Y%m%d')}.txt"
        
        await query.message.reply_document(
            document=arquivo,
            filename=arquivo.name,
            caption=f"📊 Relatório de estoque - {filial.capitalize()}"
        )
        
        # Também enviar uma prévia no chat
        linhas = relatorio.split('\n')
        preview = '\n'.join(linhas[:15])  # Primeiras 15 linhas
        
        if len(linhas) > 15:
            preview += f"\n\n... e mais {len(linhas) - 15} produtos"
        
        await query.message.reply_text(
            f"```\n{preview}\n```",
            parse_mode='Markdown'
        )
        
    except Exception as e:
        await query.message.reply_text(
            f"❌ Erro ao gerar relatório: {str(e)}"
        )

async def relatorio_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Processa os callbacks da tela de relatório"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "relatorio_lopes":
        await gerar_relatorio(update, context, "lopes")
        # Voltar ao menu principal após gerar o relatório
        await query.edit_message_text(
            "Escolha uma opção:",
            reply_markup=criar_menu_principal()
        )
        return MENU_PRINCIPAL
    
    elif query.data == "relatorio_herbert":
        await gerar_relatorio(update, context, "herbert")
        # Voltar ao menu principal após gerar o relatório
        await query.edit_message_text(
            "Escolha uma opção:",
            reply_markup=criar_menu_principal()
        )
        return MENU_PRINCIPAL
    
    elif query.data == "relatorio_conjunto":
        await gerar_relatorio(update, context, "conjunto")
        # Voltar ao menu principal após gerar o relatório
        await query.edit_message_text(
            "Escolha uma opção:",
            reply_markup=criar_menu_principal()
        )
        return MENU_PRINCIPAL
    
    elif query.data == "voltar_menu_principal":
        await query.edit_message_text(
            "Escolha uma opção:",
            reply_markup=criar_menu_principal()
        )
        return MENU_PRINCIPAL
    
    return RELATORIO

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancela a conversa atual"""
    await update.message.reply_text("Operação cancelada. Digite /start para começar novamente.")
    return ConversationHandler.END

async def comando_relatorio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Comando para gerar relatório de estoque
    """
    keyboard = [
        [InlineKeyboardButton("📊 Lopes", callback_data="relatorio_lopes")],
        [InlineKeyboardButton("📊 Herbert", callback_data="relatorio_herbert")],
        [InlineKeyboardButton("📊 Conjunto", callback_data="relatorio_conjunto")],
        [InlineKeyboardButton("🔙 Menu Principal", callback_data="voltar_menu_principal")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "*📊 Relatório de Estoque*\n\n"
        "Selecione o tipo de relatório:",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def stop_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Encerra a conversa - comportamento igual ao botão 'encerrar'"""
    await update.message.reply_text("Sistema de estoque encerrado. Digite /start para iniciar novamente.")
    return ConversationHandler.END

def main() -> None:
    """Função principal para iniciar o bot"""
    # Criar a aplicação
    application = Application.builder().token(TOKEN).build()
    
    # Definir o conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MENU_PRINCIPAL: [
                CallbackQueryHandler(menu_callback)
            ],
            ESTOQUE_LOPES: [
                CallbackQueryHandler(estoque_lopes_callback)
            ],
            ESTOQUE_HERBERT: [
                CallbackQueryHandler(estoque_herbert_callback)
            ],
            ESTOQUE_CONJUNTO: [
                CallbackQueryHandler(estoque_conjunto_callback)
            ],
            VER_LOGS: [
                CallbackQueryHandler(ver_logs_callback)
            ],
            RELATORIO: [
                CallbackQueryHandler(relatorio_callback)
            ],
            ADICIONAR_PRODUTO_CATALOGO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, adicionar_produto_catalogo),
                CallbackQueryHandler(menu_callback)
            ],
            REMOVER_PRODUTO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, processar_remocao_produto),
                CallbackQueryHandler(menu_callback)
            ],
            ADICIONAR_PRODUTOS_LOPES: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, adicionar_produtos_lopes),
                CallbackQueryHandler(estoque_lopes_callback)
            ],
            ADICIONAR_PRODUTOS_HERBERT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, adicionar_produtos_herbert),
                CallbackQueryHandler(estoque_herbert_callback)
            ],
            RETIRAR_PRODUTOS_LOPES: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, retirar_produtos_lopes),
                CallbackQueryHandler(estoque_lopes_callback)
            ],
            RETIRAR_PRODUTOS_HERBERT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, retirar_produtos_herbert),
                CallbackQueryHandler(estoque_herbert_callback)
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            CommandHandler("stop", stop_bot)
        ],
    )
    
    # Adicionar o conversation handler à aplicação
    application.add_handler(conv_handler)
    
    # Adicionar handler para o comando /estoque
    application.add_handler(CommandHandler("estoque", listar_estoque))
    
    # Adicionar handler para o comando /relatorio
    application.add_handler(CommandHandler("relatorio", comando_relatorio))
    
    # Adicionar handler para responder a textos específicos relacionados a estoque
    estoque_pattern = re.compile(r'^(estoque|ver estoque|listar estoque|lista de estoque|produtos em estoque)$', re.IGNORECASE)
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND & 
            filters.Regex(estoque_pattern),
            listar_estoque
        )
    )
    
    # Iniciar o bot
    logger.info("Bot iniciado. Pressione Ctrl+C para parar.")
    application.run_polling()

if __name__ == "__main__":
    main()