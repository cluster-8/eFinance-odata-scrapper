import pandas as pd
import numpy as np

# Sklearn e Skforecast
from sklearn.ensemble import RandomForestRegressor
from skforecast.ForecasterAutoreg import ForecasterAutoreg
from skforecast.model_selection import random_search_forecaster
from pmdarima.arima import auto_arima
import pickle5 as pickle

# install
# !pip install skforecast
# !pip install pmdarima

# Carrega Dados
url = 'https://raw.githubusercontent.com/henriquezucareli/LabVI/main/Population%20density.csv'
pop = pd.read_csv(url, sep = ',')
pop = pop.drop(['Country Code', 'Indicator Name', 'Indicator Code', 'region', 'Image URL', '1960'], axis=1)
pop = pop.drop(columns=pop.loc[:, '2024':'2100'].columns)

# Populacao da india
data = pop[pop['Country Name'] == 'India']
data = data.drop(['Country Name'], axis=1)
data = pd.melt(data, var_name='date', value_name='india')

# Juntando os dados de bangladesh
bangladesh = pop[pop['Country Name'] == 'Bangladesh']
bangladesh = bangladesh.drop(['Country Name'], axis=1)
bangladesh = pd.melt(bangladesh, var_name='date', value_name='bangladesh')
data['bangladesh'] = bangladesh['bangladesh']

# Transformando os dados de string para float
data['india'] = data['india'].astype(float)
data['bangladesh'] = data['bangladesh'].astype(float)

# Fazendo o indice anual
data['date'] = pd.to_datetime(data['date'], format='%Y')
data = data.set_index('date')
data = data.asfreq('YS', fill_value=0.0)
data = data.sort_index()

# Tentando sem o indice temporal
data_no_index = data.copy()
data_no_index.reset_index(drop=True, inplace=True)

# Divide dados em treinamento e teste
# Para séries temporais, sempre utilizamos os dados mais recentes para teste
steps = 10
data_train = data_no_index[:-steps]
data_test  = data_no_index[-steps:]

# Tunning
# Usara combinacoes aleatorias dos parametros
# ==============================================================================
forecaster = ForecasterAutoreg(
                 regressor = RandomForestRegressor(random_state=123),
                 lags      = 10 # O valor será substituído durante o tunning
             )

# Valores de lag a testar
lags_grid = [2, 3, 4, 5, 6, 7, 8, 9, 10]

# Regressor hyperparameters
param_distributions = {'n_estimators': np.arange(start=10, stop=100, step=1, dtype=int),
                       'max_depth': np.arange(start=5, stop=30, step=1, dtype=int)}

results = random_search_forecaster(
              forecaster           = forecaster,
              y                    = data_no_index['india'],
              steps                = steps,
              lags_grid            = lags_grid,
              param_distributions  = param_distributions,
              n_iter               = 100,
              metric               = 'mean_squared_error',
              refit                = True,
              initial_train_size   = len(data_no_index['india']) - steps,
              fixed_train_size     = False,
              return_best          = True,
              random_state         = 123,
              verbose              = False
          )



forecaster = ForecasterAutoreg(
                regressor = RandomForestRegressor(max_depth=25, n_estimators=10, random_state=123),
                lags      = 9
             )

forecaster.fit(y=data_train['india'])
predictions = forecaster.predict(steps=steps)


# O ARIMA vem com um tunning automático, o auto_arima
# from pmdarima.arima import auto_arima
model = auto_arima(data_train['india'], trace=True, error_action='ignore', suppress_warnings=True)

# Treina o modelo
model.fit(data_train['india'])

# Previsao
forecast = model.predict(n_periods=len(data_test))

# Converte para um dataframe
forecast = pd.DataFrame(forecast,index = data_test.index,columns=['Prediction'])

# Saving model to disk
pickle.dump(forecast, open('model.pkl','wb'))

# Loading model to compare the results
model = pickle.load(open('model.pkl','rb'))
