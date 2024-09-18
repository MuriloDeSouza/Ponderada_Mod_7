import numpy as np
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

def predict_crypto(crypto):
    # Carregando os dados do criptoativo
    ticker = yf.Ticker(crypto)
    data = ticker.history(period='2y')['Close'].values.reshape(-1, 1)

    # Normalizando os dados
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)

    # Preparando os dados (use time_step=60 como no exemplo)
    time_step = 60
    last_60_days = scaled_data[-time_step:]
    last_60_days = last_60_days.reshape(1, time_step, 1)

    # Carregar modelo treinado (exemplo: colocar em arquivo .h5)
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(last_60_days.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(units=25))
    model.add(Dense(units=1))
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Prevendo os próximos 7 dias
    future_predictions = []
    for day in range(7):
        predicted_price = model.predict(last_60_days)
        future_predictions.append(predicted_price[0, 0])
        predicted_price = predicted_price.reshape(1, 1, 1)
        last_60_days = np.append(last_60_days[:, 1:, :], predicted_price, axis=1)

    future_predictions = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1))

    # Pegando os fechamentos reais dos últimos 5 dias
    real_last_5_days = data[-5:]

    return future_predictions, real_last_5_days
