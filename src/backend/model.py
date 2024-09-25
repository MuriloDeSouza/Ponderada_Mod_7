import os
import numpy as np
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout
from prophet import Prophet
import pandas as pd
from sklearn.metrics import mean_absolute_error

def train_and_save_model(crypto='BNB-USD'):
    # Carregar dados do criptoativo
    ticker = yf.Ticker(crypto)
    data = ticker.history(period='2y')['Close'].values.reshape(-1, 1)

    # Normalizando os dados
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)

    # Criar sequência de dados para treino
    def create_sequences(data, time_step=60):
        X, y = [], []
        for i in range(len(data) - time_step - 1):
            X.append(data[i:(i + time_step), 0])
            y.append(data[i + time_step, 0])
        return np.array(X), np.array(y)

    time_step = 60
    X, y = create_sequences(scaled_data, time_step)
    X = X.reshape(X.shape[0], X.shape[1], 1)

    # Dividindo em treino e teste
    train_size = int(0.8 * len(X))
    X_train, y_train = X[:train_size], y[:train_size]
    X_test, y_test = X[train_size:], y[train_size:]

    # Criando o modelo LSTM
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(units=25))
    model.add(Dense(units=1))

    # Compilando o modelo
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Treinando o modelo
    model.fit(X_train, y_train, batch_size=64, epochs=10)

    # Salvando o modelo e o scaler
    model_save_path = f'saved_models/model_{crypto}.h5'
    model.save(model_save_path)

    # Salvando o scaler
    scaler_save_path = f'saved_models/scaler_{crypto}.npy'
    np.save(scaler_save_path, scaler)

    return model, scaler

def predict_with_prophet(crypto='BNB-USD'):
    # Carregar dados do criptoativo
    ticker = yf.Ticker(crypto)
    df = ticker.history(period='2y')[['Close']].reset_index()

    # Renomear as colunas para o formato esperado pelo Prophet
    df.columns = ['ds', 'y']

    # Remover timezone dos dados (caso exista)
    df['ds'] = pd.to_datetime(df['ds']).dt.tz_localize(None)

    # Inicializar e treinar o modelo Prophet
    model = Prophet()
    model.fit(df)

    # Criar datas futuras para a previsão (próximos 7 dias)
    future = model.make_future_dataframe(periods=7)

    # Fazer previsões
    forecast = model.predict(future)

    # Previsões dos próximos 7 dias
    future_predictions = forecast[['ds', 'yhat']].tail(7)

    # Retornar as previsões futuras e os últimos 5 dias reais
    print(future_predictions['yhat'].values, df['y'].tail(5).values)
    return future_predictions['yhat'].values, df['y'].tail(5).values

def predict_crypto(crypto='BNB-USD'):
    # Carregar o modelo
    model_path = f'saved_models/model_{crypto}.h5'
    scaler_path = f'saved_models/scaler_{crypto}.npy'
    model = load_model(model_path)
    scaler = np.load(scaler_path, allow_pickle=True).item()

    # Carregar os dados mais recentes do criptoativo
    ticker = yf.Ticker(crypto)
    data = ticker.history(period='2y')['Close'].values.reshape(-1, 1)

    # Normalizar os dados
    scaled_data = scaler.transform(data)

    # Usar os últimos 60 dias para prever os próximos 7 dias
    time_step = 60
    last_60_days = scaled_data[-time_step:]
    last_60_days = last_60_days.reshape(1, time_step, 1)

    future_predictions = []
    for day in range(7):
        predicted_price = model.predict(last_60_days)
        future_predictions.append(predicted_price[0, 0])
        predicted_price = predicted_price.reshape(1, 1, 1)
        last_60_days = np.append(last_60_days[:, 1:, :], predicted_price, axis=1)

    # Reverter a normalização
    future_predictions = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1))

    # Obter os preços reais dos últimos 5 dias
    real_last_5_days = data[-5:].reshape(-1)

    print(future_predictions, real_last_5_days)
    return future_predictions, real_last_5_days