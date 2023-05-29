# !pip install skforecast # !pip install pmdarima

# Configuração do matplotlib
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
plt.rcParams['lines.linewidth'] = 1.5
#%matplotlib inline

import pandas as pd
import numpy as np

# Sklearn e Skforecast
from sklearn.ensemble import RandomForestRegressor
from skforecast.ForecasterAutoreg import ForecasterAutoreg
from skforecast.model_selection import random_search_forecaster
from pmdarima.arima import auto_arima
import pickle5 as pickle

# file_path = '/home/vv/Documents/fatec/semestre-6/api/github/eFinance-odata-scrapper/models/NVDA.csv'
file_path = './models/NVDA.csv'

df = pd.read_csv(file_path)
df = df[['Date', 'Close']]

data = df
data['Close'] = data['Close'].astype(float)

# Tentando sem o indice temporal
data_no_index = data.copy()
data_no_index.reset_index(drop=True, inplace=True)

# Divide dados em treinamento e teste
# Para séries temporais, sempre utilizamos os dados mais recentes para teste
steps = 10
data_train = data_no_index[:-steps]
data_test  = data_no_index[-steps:]

# O ARIMA vem com um tunning automático, o auto_arima
from pmdarima.arima import auto_arima
model = auto_arima(data_train['Close'], trace=True, error_action='ignore', suppress_warnings=True)

# Treina o modelo
model.fit(data_train['Close'])

# Previsao
forecast = model.predict(n_periods=len(data_test))

# Saving model to disk
pickle.dump(forecast, open('./models/model_arima.pkl','wb'))

# Loading model to compare the results
model = pickle.load(open('./models/model_arima.pkl','rb'))
