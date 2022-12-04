import yfinance as yf
import pandas as pd
from datetime import datetime
import os

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
    'SAPR4',
    'BBSE3',
    'B3SA3',
    'CSMG3',
    'ALUP11'
]
hoje = datetime.now()
passado = hoje.replace(year=hoje.year-anos)
dataDiretory = 'data/'
if not os.path.exists(dataDiretory):
    os.mkdir(dataDiretory)

DYs = {}
for acao in acoes:
    nomeArquivo = dataDiretory + acao + '_' + hoje.strftime('%Y-%m-%d') + '.csv'
    try:
        dados = pd.read_csv(nomeArquivo)
    except Exception as err:
        print('Arquivo não encontrado! Erro:', err)
        dados = yf.download(acao + '.SA', start=passado, end=hoje, actions=True)
        dados.to_csv(nomeArquivo)
        print(acao + ' Baixada!')
    dividendos = dados['Dividends'].loc[dados['Dividends'] != 0]
    dividendoTotal = dividendos.sum()
    precoAtual = dados['Close'].iloc[-1]
    DYs[acao] = round(100 * dividendoTotal / (anos * precoAtual), 2)
print(dict(sorted(DYs.items(), key=lambda x: x[1])))
