---
sidebar_position: 3
---

# Pergunta 3

# O modelo foi implementado com uma API de acesso que está disponível para ser utilizada;

## Explicando os modelos LSTM e Prophet

&emsp;Sim, o modelo de machine learning foi implementado com uma API de acesso utilizando o framework FastAPI. A API permite que usuários enviem requisições para realizar previsões de preços de criptoativos com dois modelos diferentes: o LSTM e o Prophet. 
&emsp;Essas previsões podem ser solicitadas via endpoints dedicados, permitindo flexibilidade no uso do sistema.

&emsp;Trecho de código para exemplificar a implementação da API:

```bash
@app.post("/predict_lstm")
async def predict_lstm(crypto: str):
    # Código para realizar a previsão com o modelo LSTM
    prediction = lstm_model.predict(crypto)
    return {"crypto": crypto, "prediction": prediction}

@app.post("/predict_prophet")
async def predict_prophet(crypto: str):
    # Código para realizar a previsão com o modelo Prophet
    prediction = prophet_model.predict(crypto)
    return {"crypto": crypto, "prediction": prediction}

@app.post("/comparation")
async def post_predict(request: CryptoRequest):
    # Código para realizar a previsão com o modelo LSTM e o Prophet
    prediction = lstm_and_prophet(crypto)
    return {"crypto": crypto, "prediction": prediction}
```
&emsp; Aqui eu consigo fazer as predições dos modelos que estão usando os modelos de LSTM, Prophet e ambas para serem comparadas em um formato melhor pelo usuário.

## Local onde estão os modelos salvos:

&emsp; Vale destacar que os modelos são rodados no backend a princípio. Temos que garantir que estamos no diretório correto:

```bash
src>backend
```

&emsp; Depois que estivemos no diretório correto, vamos rodar o código abaixo para poder rodar os modelos:

```bash
python train_models.py
```

&emsp; Dessa forma ele vai na nossa main.py e vai rodar o modelo para três cryptoaticos diferentes que são "BTC-USD", "ETH-USD" e "BNB-USD":

```bash
from model import train_and_save_model
# Treinando e salvando os modelos para diferentes criptoativos
train_and_save_model('BTC-USD')
train_and_save_model('ETH-USD')
train_and_save_model('BNB-USD')
```

```bash
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
```

# Conclusão:

&emsp;A API fornece rotas acessíveis que permitem que o modelo seja usado tanto para previsões quanto para consultas de logs, além de funcionalidades adicionais como o retreinamento do modelo.
