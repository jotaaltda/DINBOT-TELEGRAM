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
    data = update.message.date.strftime('%d/%m/%Y')

    if '-' in mensagem:
        # CONVERTE O VALOR DA MENSAGEM PARA INT OU FLOAT
        if '.' in mensagem[1]:
            mensagem[1] = float(mensagem[1])
        else:
            mensagem[1] = int(mensagem[1])

        await update.message.reply_text(f'*GASTO* DE *R${mensagem[1]:.2f}* ADICIONADO!', parse_mode='Markdown')
        aba.append_row([data, 'GASTO', mensagem[1], mensagem[2]])

    if '+' in mensagem:
        if '.' in mensagem[1]:
            mensagem[1] = float(mensagem[1])
        else:
            mensagem[1] = int(mensagem[1])
    
        await update.message.reply_text(f'*GANHO* DE *R${mensagem[1]:.2f}* ADICIONADO!', parse_mode='Markdown')
        aba.append_row([data, 'GANHO', mensagem[1], mensagem[2]])

    if 'CDI' in mensagem:
            if '.' in mensagem[1]:
                mensagem[1] = float(mensagem[1])
            else:
                mensagem[1] = int(mensagem[1])
        
            await update.message.reply_text(f'*INVESTIMENTO* DE *R${mensagem[1]:.2f}* ADICIONADO!', parse_mode='Markdown')
            aba.append_row([data, 'CDI', mensagem[1]])

    if 'gastos' in mensagem:

        if 'alimentação' in mensagem:
            ...
        if 'lazer' in mensagem:
            ...
        if 'despesa' in mensagem:
            ...
        if 'compra' in mensagem:
            ...
        else:
            gastos = aba.acell('K6').value
            await update.message.reply_text(f'SEU TOTAL DE GASTOS NESSE MÊS É: {gastos}!')

conexao_telegram.add_handler(MessageHandler(filters.TEXT, receber_mensagem))

conexao_telegram.run_polling()