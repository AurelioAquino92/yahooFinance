import yfinance as yf
import pandas as pd
from datetime import datetime
import os
import json

def converter_dados(dados):
    dados = dados.reset_index()
    dados['Date'] = pd.to_datetime(dados['Date']).dt.strftime('%Y-%m-%d')
    return dados

anos = 5
acoes = [
    'ITSA4',
    'TAEE11',
    'CPLE6',
    'SANB11',
    'CPFE3',
    'BBDC3',
    'BBAS3', 
    'WIZS3',
    'PSSA3',
    'ODPV3',
    'CXSE3',
    'BBSE3',
    'B3SA3',
    'VIVT3'
]

hoje = datetime.now()
passado = hoje.replace(year=hoje.year-anos)
dataDiretory = 'data/'
if not os.path.exists(dataDiretory):
    os.mkdir(dataDiretory)

precosJustos = {}
for acao in acoes:
    nomeArquivo = dataDiretory + acao + '.csv'
    
    try:
        dados = pd.read_csv(nomeArquivo)
    except Exception as err:
        print('Arquivo não encontrado -> Erro:', err)
        print('Baixando dados...')
        dados = yf.download(acao + '.SA', start=passado, end=hoje, actions=True)
        dados.to_csv(nomeArquivo)
        print(acao + ' Baixada!')
    
    try:
        ultimaData = datetime.strptime(dados['Date'].iloc[-1], '%Y-%m-%d')
    except:
        dados = converter_dados(dados)
        ultimaData = datetime.strptime(dados['Date'].iloc[-1], '%Y-%m-%d')

    if (hoje-ultimaData).days > 0:
        print('Atualizando', acao, '...')
        dataInicio = ultimaData.replace(day=ultimaData.day+1)
        dados2 = yf.download(acao+'.SA', start=dataInicio, end=hoje, actions=True)
        dados = pd.concat([dados.set_index('Date'), dados2])
        dados = converter_dados(dados)
        dados = dados.set_index('Date')
        dados.to_csv(nomeArquivo)
        print(acao, 'atualizada!')
    
    dados = dados.reset_index()
    dados['Date'] = pd.to_datetime(dados['Date'])
    dividendoTotal = dados[dados['Date'] >= passado]['Dividends'].sum()
    precoAtual = round(dados['Close'].iloc[-1], 2)
    precoJusto = round(dividendoTotal / (anos * 0.06), 2)
    precosJustos[acao] = round(precoAtual / precoJusto, 2)

print('Upsides com base nos dividendos dos últimos {anos} anos'.format(anos=anos))
print(json.dumps(dict(sorted(precosJustos.items(), key=lambda x: x[1])), indent=2))

