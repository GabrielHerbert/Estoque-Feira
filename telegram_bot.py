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
    ADICIONAR_PRODUTOS_LOPES,
    ADICIONAR_PRODUTOS_HERBERT,
    RETIRAR_PRODUTOS_LOPES,
    RETIRAR_PRODUTOS_HERBERT,
) = range(9)

# Token do bot
TOKEN = "Seu token"

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
            InlineKeyboardButton("Adicionar Novo Produto", callback_data="adicionar_produto")
        ],
        [
            InlineKeyboardButton("Encerrar", callback_data="encerrar")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def criar_menu_estoque(filial: str) -> InlineKeyboardMarkup:
    """Cria o menu de opções para um estoque específico"""
    callback_prefix = f"estoque_{filial.lower()}"
    keyboard = [
        [
            InlineKeyboardButton("Adicionar Produtos", callback_data=f"adicionar_{filial.lower()}"),
            InlineKeyboardButton("Retirar Produtos", callback_data=f"retirar_{filial.lower()}")
        ],
        [
            InlineKeyboardButton("Voltar", callback_data="voltar_menu_principal")
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
            "Exemplo: '2.5kg tilápia' ou '3 camarão limpo g'"
        )
        return
    
    # Preparar mensagem de confirmação
    mensagem = f"*{'Adicionando' if operacao == 'adicionar' else 'Retirando'} produtos no estoque {filial.capitalize()}:*\n\n"
    
    sucesso = []
    falha = []
    
    # Adicionar ou retirar cada item do estoque
    for item in itens_processados:
        produto_id = item['produto_id']
        quantidade = item['quantidade']
        nome_produto = item['nome']
        
        # Verificar se a unidade é kg (assumimos que tudo é em kg para o estoque)
        if item['unidade'] != 'kg':
            mensagem += f"⚠️ {nome_produto}: unidade não é kg, convertendo para kg\n"
        
        # Realizar a operação no estoque
        if operacao == 'adicionar':
            resultado = estoque_core.add_to_stock(produto_id, quantidade, filial)
        else:  # retirar
            resultado = estoque_core.remove_from_stock(produto_id, quantidade, filial)
        
        # Registrar resultado
        if resultado:
            sucesso.append(f"✅ {nome_produto}: {quantidade} kg")
        else:
            falha.append(f"❌ {nome_produto}: {quantidade} kg")
    
    # Adicionar resultados à mensagem
    if sucesso:
        mensagem += "\n*Operações realizadas com sucesso:*\n"
        mensagem += "\n".join(sucesso)
    
    if falha:
        mensagem += "\n\n*Operações que falharam:*\n"
        mensagem += "\n".join(falha)
    
    # Enviar mensagem de confirmação
    await update.message.reply_text(mensagem, parse_mode='Markdown')
    
    # Mostrar o estoque atualizado
    estoque_data = estoque_core.get_stock(filial)
    mensagem_estoque = estoque_core.format_stock_message(estoque_data, f"Estoque {filial.capitalize()} Atualizado")
    
    # Criar teclado para voltar ao menu do estoque
    keyboard = [
        [InlineKeyboardButton("Voltar ao Menu", callback_data="voltar_menu_principal")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(mensagem_estoque, parse_mode='Markdown', reply_markup=reply_markup)

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
    
    if query.data == "estoque_lopes":
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
    
    elif query.data == "adicionar_produto":
        await query.edit_message_text(
            "Por favor, digite o nome do novo produto que deseja adicionar ao catálogo:",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Cancelar", callback_data="voltar_menu_principal")
            ]])
        )
        return ADICIONAR_PRODUTO_CATALOGO
    
    elif query.data == "encerrar":
        await query.edit_message_text("Sistema de estoque encerrado. Digite /start para iniciar novamente.")
        return ConversationHandler.END
    
    return MENU_PRINCIPAL

async def estoque_lopes_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Processa os callbacks do menu do estoque Lopes"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "adicionar_lopes":
        await query.edit_message_text(
            "Envie a lista de produtos a serem adicionados ao estoque Lopes.\n"
            "Formato: quantidade produto\n"
            "Exemplo:\n"
            "2.5kg tilápia\n"
            "3 camarão limpo g\n"
            "1.2kg pescada amarela",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Cancelar", callback_data="estoque_lopes")
            ]])
        )
        return ADICIONAR_PRODUTOS_LOPES
    
    elif query.data == "retirar_lopes":
        await query.edit_message_text(
            "Envie a lista de produtos a serem retirados do estoque Lopes.\n"
            "Formato: quantidade produto\n"
            "Exemplo:\n"
            "2.5kg tilápia\n"
            "3 camarão limpo g\n"
            "1.2kg pescada amarela",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Cancelar", callback_data="estoque_lopes")
            ]])
        )
        return RETIRAR_PRODUTOS_LOPES
    
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
    
    if query.data == "adicionar_herbert":
        await query.edit_message_text(
            "Envie a lista de produtos a serem adicionados ao estoque Herbert.\n"
            "Formato: quantidade produto\n"
            "Exemplo:\n"
            "2.5kg tilápia\n"
            "3 camarão limpo g\n"
            "1.2kg pescada amarela",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Cancelar", callback_data="estoque_herbert")
            ]])
        )
        return ADICIONAR_PRODUTOS_HERBERT
    
    elif query.data == "retirar_herbert":
        await query.edit_message_text(
            "Envie a lista de produtos a serem retirados do estoque Herbert.\n"
            "Formato: quantidade produto\n"
            "Exemplo:\n"
            "2.5kg tilápia\n"
            "3 camarão limpo g\n"
            "1.2kg pescada amarela",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Cancelar", callback_data="estoque_herbert")
            ]])
        )
        return RETIRAR_PRODUTOS_HERBERT
    
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
    return ESTOQUE_LOPES

async def adicionar_produtos_herbert(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Processa a lista de produtos a serem adicionados ao estoque Herbert"""
    await processar_lista_produtos(update, context, 'adicionar', 'herbert')
    return ESTOQUE_HERBERT

async def retirar_produtos_lopes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Processa a lista de produtos a serem retirados do estoque Lopes"""
    await processar_lista_produtos(update, context, 'retirar', 'lopes')
    return ESTOQUE_LOPES

async def retirar_produtos_herbert(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Processa a lista de produtos a serem retirados do estoque Herbert"""
    await processar_lista_produtos(update, context, 'retirar', 'herbert')
    return ESTOQUE_HERBERT

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancela a conversa e volta ao menu principal"""
    if update.message:
        await update.message.reply_text(
            "Operação cancelada. Voltando ao menu principal.",
            reply_markup=criar_menu_principal()
        )
    else:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            "Operação cancelada. Voltando ao menu principal.",
            reply_markup=criar_menu_principal()
        )
    
    return MENU_PRINCIPAL

async def stop_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Encerra o bot - disponível para qualquer usuário"""
    user_id = update.effective_user.id
    
    # Enviar mensagem de confirmação
    await update.message.reply_text(
        "🛑 *Bot está sendo desligado...*\n\nPara reiniciar, execute o bot manualmente no servidor.",
        parse_mode='Markdown'
    )
    
    logger.info(f"Bot sendo desligado pelo usuário {update.effective_user.first_name} (ID: {user_id})")
    
    # Parar a aplicação
    await context.application.stop()

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
            ADICIONAR_PRODUTO_CATALOGO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, adicionar_produto_catalogo),
                CallbackQueryHandler(menu_callback)
            ],
            ADICIONAR_PRODUTOS_LOPES: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, adicionar_produtos_lopes),
                CallbackQueryHandler(menu_callback, pattern="^voltar_menu_principal$"),
                CallbackQueryHandler(estoque_lopes_callback)
            ],
            ADICIONAR_PRODUTOS_HERBERT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, adicionar_produtos_herbert),
                CallbackQueryHandler(menu_callback, pattern="^voltar_menu_principal$"),
                CallbackQueryHandler(estoque_herbert_callback)
            ],
            RETIRAR_PRODUTOS_LOPES: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, retirar_produtos_lopes),
                CallbackQueryHandler(menu_callback, pattern="^voltar_menu_principal$"),
                CallbackQueryHandler(estoque_lopes_callback)
            ],
            RETIRAR_PRODUTOS_HERBERT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, retirar_produtos_herbert),
                CallbackQueryHandler(menu_callback, pattern="^voltar_menu_principal$"),
                CallbackQueryHandler(estoque_herbert_callback)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    # Adicionar o conversation handler à aplicação
    application.add_handler(conv_handler)
    
    # Adicionar handler para o comando /estoque
    application.add_handler(CommandHandler("estoque", listar_estoque))
    
    # Adicionar handler para o comando /stop
    application.add_handler(CommandHandler("stop", stop_bot))
    
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
