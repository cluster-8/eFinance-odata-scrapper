from pmdarima.arima import auto_arima
from pmdarima.datasets import load_lynx
import numpy as np
import pandas as pd

# For serialization:
import joblib
import pickle

# Load data and fit a model
# y = pd.read_csv('./models/DATA-OK.csv')
# y = pd.read_csv('./models/NVDA.csv')
y = pd.read_csv('./models/DATA.csv')


arima = auto_arima(y['Close'], seasonal=True)

# Serialize with Pickle
with open('./models/auto_arima.pkl', 'wb') as pkl:
    pickle.dump(arima, pkl)

# You can still make predictions from the model at this point
arima.predict(n_periods=5)

# Now read it back and make a prediction
with open('./models/auto_arima.pkl', 'rb') as pkl:
    pickle_preds = pickle.load(pkl).predict(n_periods=5)

# Or maybe joblib tickles your fancy
joblib.dump(arima, './models/arima.pkl')
joblib_preds = joblib.load('./models/arima.pkl').predict(n_periods=5)

# show they're the same
np.allclose(pickle_preds, joblib_preds)