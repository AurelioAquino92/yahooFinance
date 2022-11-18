import yfinance as yf
import pandas as pd
from matplotlib import pyplot as plt

petr = yf.Ticker('PETR4.SA')
hist = petr.history(period='3y', interval='1mo').dropna()[:-1]

filtro = pd.DataFrame()
filtro['HL'] = hist['High'] - hist['Low']
filtro['OC'] = hist['Open'] - hist['Close']

# calculando a probabilidade de ocorrer variação X
nums = []
for i in range(100):
    nums.append(len(filtro[filtro['HL'] >= i/10])/len(filtro))

plt.plot(nums)
plt.grid(True)
plt.show()
