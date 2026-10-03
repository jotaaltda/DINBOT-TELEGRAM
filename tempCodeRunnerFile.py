from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

import gspread

import credenciais.credenciais as credenciais

# CONECTA O BOT AO SCRIPT / PLANILHA
conexao_telegram = Application.builder().token(credenciais.token_bot).build()
conexao_planilhas = gspread.service_account(filename='credenciais/google.json')

# ABRE O BANCO DE DADOS (PLANILHA)
dados = conexao_planilhas.open('DINBOT - BANCO DE DADOS')
aba = dados.sheet1

async def receber_mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):

    mensagem = update.message.text.split()
    data = update.message.date

    if '-' in mensagem:

        # CONVERTE O VALOR DA MENSAGEM PARA INT OU FLOAT
        if '.' in mensagem[1]:
            mensagem[1] = float(mensagem[1])
        else:
            mensagem[1] = int(mensagem[1])

        await update.message.reply_text(f'R${mensagem[1]:.2f} GASTOS!')
        aba.append_row([data, 'GASTO', int(mensagem[1]), mensagem[2]])

    if 'gastos' in mensagem:
        gastos = aba.acell('I2').value
        await update.message.reply_text(f'SEU TOTAL DE GASTOS NESSE MÊS É: R${gastos}!')

conexao_telegram.add_handler(MessageHandler(filters.TEXT, receber_mensagem))

conexao_telegram.run_polling()