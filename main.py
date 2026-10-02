from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

import credenciais.credenciais as credenciais

# CONECTA O BOT AO SCRIPT
conexao = Application.builder().token(credenciais.token_bot).build()

async def receber_mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # SÓ ACEITA MENSAGENS MINHAS
    if update.effective_user.id != credenciais.id_usuario:
        return

    if '-' in update.message.text:
        await update.message.reply_text("Saiu dinheiro!")

    if '+' in update.message.text:
            await update.message.reply_text("Entrou dinheiro!")

conexao.add_handler(MessageHandler(filters.TEXT, receber_mensagem))

conexao.run_polling()