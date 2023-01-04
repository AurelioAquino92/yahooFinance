import yfinance as yf
import pandas as pd
from datetime import datetime
import os
import json

anos = 3
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

DYs = {}
for acao in acoes:
    nomeArquivo = dataDiretory + acao + '_' + str(anos) + 'anos_' + hoje.strftime('%Y-%m-%d') + '.csv'
    try:
        dados = pd.read_csv(nomeArquivo)
    except Exception as err:
        print('Arquivo não encontrado! Erro:', err)
        dados = yf.download(acao + '.SA', start=passado, end=hoje, actions=True)
        dados.to_csv(nomeArquivo)
        print(acao + ' Baixada!')
    # dividendos = dados['Dividends'].loc[dados['Dividends'] != 0]
    dividendoTotal = dados['Dividends'].sum()
    precoAtual = dados['Close'].iloc[-1]
    DYs[acao] = round(100 * dividendoTotal / (anos * precoAtual), 2)

print('Média de dividendos (%) dos últimos {anos} anos'.format(anos=anos))
print(json.dumps(dict(sorted(DYs.items(), key=lambda x: x[1])), indent=2))

