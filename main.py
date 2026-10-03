from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

import gspread

import credenciais.credenciais as credenciais

# CONECTA O BOT AO SCRIPT / PLANILHA
conexao_telegram = Application.builder().token(credenciais.token_bot).build()
conexao_planilhas = gspread.service_account(filename='credenciais/google.json')

# ABRE O BANCO DE DADOS (PLANILHA)
dados = conexao_planilhas.open('DINBOT - BANCO DE DADOS')

async def receber_mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):

    mensagem = update.message.text.split()
    data = update.message.date.strftime('%d/%m/%Y')

    if '/10/' in data:
        aba = dados.worksheet('OUTUBRO')
    if '/11/' in data:
        aba = dados.worksheet('NOVEMBRO')
    if '/12/' in data:
        aba = dados.worksheet('DEZEMBRO')

    if '-' in mensagem:
        # CONVERTE O VALOR DA MENSAGEM PARA INT OU FLOAT
        if '.' in mensagem[1]:
            mensagem[1] = float(mensagem[1])
        else:
            mensagem[1] = int(mensagem[1])

        await update.message.reply_text(f' 📉 *GASTO* DE *R${mensagem[1]:.2f}* ADICIONADO!', parse_mode='Markdown')

        if 'crédito' in mensagem:
            if 'picpay' in mensagem:
                aba.append_row([data, 'GASTO', mensagem[1], mensagem[2], 'CRÉDITO PICPAY'])
            if 'mercado' in mensagem:
                aba.append_row([data, 'GASTO', mensagem[1], mensagem[2], 'CRÉDITO MERCADO PAGO'])
        else:
            aba.append_row([data, 'GASTO', mensagem[1], mensagem[2]])

    if '+' in mensagem:
        if '.' in mensagem[1]:
            mensagem[1] = float(mensagem[1])
        else:
            mensagem[1] = int(mensagem[1])
    
        await update.message.reply_text(f' 📈 *GANHO* DE *R${mensagem[1]:.2f}* ADICIONADO!', parse_mode='Markdown')

        if 'crédito' in mensagem:
            if 'picpay' in mensagem:
                aba.append_row([data, 'GANHO', mensagem[1], mensagem[2], 'CRÉDITO PICPAY'])
            if 'mercado' in mensagem:
                aba.append_row([data, 'GANHO', mensagem[1], mensagem[2], 'CRÉDITO MERCADO PAGO'])
        else:
            aba.append_row([data, 'GANHO', mensagem[1], mensagem[2]])

    if 'CDI' in mensagem:
            if '.' in mensagem[1]:
                mensagem[1] = float(mensagem[1])
            else:
                mensagem[1] = int(mensagem[1])
        
            await update.message.reply_text(f'*INVESTIMENTO* DE *R${mensagem[1]:.2f}* ADICIONADO!', parse_mode='Markdown')
            aba.append_row([data, 'CDI', mensagem[1]])

    if 'Investidos' in mensagem:
        investidos = aba.acell('H11').value
        await update.message.reply_text(f'SEU TOTAL DE GASTOS NESSE MÊS É: {gastos}!')
        
    if 'Gastos' in mensagem:

        if 'outubro' in mensagem:
            aba = dados.worksheet('OUTUBRO')
        if 'novembro' in mensagem:
            aba = dados.worksheet('NOVEMBRO')
        if 'dezembro' in mensagem:
            aba = dados.worksheet('DEZEMBRO')

        await update.message.reply_text(f'''
💸 SEUS GASTOS NO MÊS DE *{aba.title}*:

🍖 ALIMENTAÇÃO: *{aba.acell('K2').value}*
🎢 LAZER: *{aba.acell('K3').value}*
🧾 DESPESAS: *{aba.acell('K4').value}*
🛍️ COMPRAS: *{aba.acell('K5').value}*
🚗 TRANSPORTE: *{aba.acell('K6').value}*

TOTAL: *{aba.acell('K7').value}*
''', parse_mode='Markdown')

    if 'Ganhos' in mensagem:
        if 'outubro' in mensagem:
            aba = dados.worksheet('OUTUBRO')
        if 'novembro' in mensagem:
            aba = dados.worksheet('NOVEMBRO')
        if 'dezembro' in mensagem:
            aba = dados.worksheet('DEZEMBRO')
        
        await update.message.reply_text(f'''
💰 SEUS GANHOS NO MÊS DE *{aba.title}*:
        
👷 SALÁRIO: *{aba.acell('N2').value}*
👨‍🎓 BOLSA: *{aba.acell('N3').value}*
🛒 VENDAS: *{aba.acell('N4').value}*
🎁 GANHOS: *{aba.acell('N5').value}*
        
TOTAL: *{aba.acell('N6').value}*
''', parse_mode='Markdown')

conexao_telegram.add_handler(MessageHandler(filters.TEXT, receber_mensagem))

conexao_telegram.run_polling()