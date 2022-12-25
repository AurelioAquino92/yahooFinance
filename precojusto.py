import yfinance as yf
import pandas as pd
from datetime import datetime
import os
import json

anos = 5
acoes = [
    'CPLE6',
    'WIZS3',
    'PSSA3',
    'SANB11',
    'BBAS3', 
    'BBDC3',
    'ODPV3',
    'CXSE3',
    'BBSE3',
    'ITSA4',
    'TAEE11'
]

hoje = datetime.now()
passado = hoje.replace(year=hoje.year-anos)
dataDiretory = 'data/'
if not os.path.exists(dataDiretory):
    os.mkdir(dataDiretory)

precosJustos = {}
for acao in acoes:
    nomeArquivo = dataDiretory + acao + '_' + str(anos) + 'anos_' + hoje.strftime('%Y-%m-%d') + '.csv'
    try:
        dados = pd.read_csv(nomeArquivo)
    except Exception as err:
        print('Arquivo não encontrado! Erro:', err)
        dados = yf.download(acao + '.SA', start=passado, end=hoje, actions=True)
        dados.to_csv(nomeArquivo)
        print(acao + ' Baixada!')
    dividendos = dados['Dividends'].loc[dados['Dividends'] != 0]
    dividendoTotal = dividendos.sum()
    precoAtual = round(dados['Close'].iloc[-1], 2)
    precoJusto = round(dividendoTotal / (anos * 0.06), 2)
    precosJustos[acao] = round(precoJusto / precoAtual, 2)

print('Upsides com base nos dividendos dos últimos {anos} anos'.format(anos=anos))
print(json.dumps(dict(sorted(precosJustos.items(), key=lambda x: x[1])), indent=2))

