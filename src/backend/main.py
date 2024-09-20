# Importações
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import matplotlib.pyplot as plt
import numpy as np
from model import train_and_save_model, predict_with_prophet, predict_crypto
import os

# Inicializar o FastAPI
app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Domínio do Next.js
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Definir o formato da entrada de dados usando Pydantic
class CryptoRequest(BaseModel):
    crypto: str
    
# Rota POST para previsões
@app.post("/predict")
async def post_predict(request: CryptoRequest):
    crypto = request.crypto
    future_predictions, real_last_5_days = predict_crypto(crypto)
    future_predictions_ph, real_last_5_days_ph = predict_with_prophet(crypto)
    
    # Encontrando o melhor dia para comprar e vender
    best_day_buy = np.argmin(future_predictions) + 1  # Melhor dia para comprar (menor valor)
    best_day_sell = np.argmax(future_predictions) + 1  # Melhor dia para vender (maior valor)

    # Encontrando o melhor dia para comprar e vender
    best_day_buy_ph = np.argmin(future_predictions_ph) + 1  # Melhor dia para comprar (menor valor)
    best_day_sell_ph = np.argmax(future_predictions_ph) + 1  # Melhor dia para vender (maior valor)

    # Plota o gráfico e salva na pasta estática do Next.js
    plt.figure(figsize=(10, 5))
    days_real = np.arange(-5, 0)  # Últimos 5 dias
    days_future = np.arange(1, 8)  # Próximos 7 dias

    # Plota o gráfico e salva na pasta estática do Next.js
    plt.figure(figsize=(10, 5))
    days_real_ph = np.arange(-5, 0)  # Últimos 5 dias
    days_future_ph = np.arange(1, 8)  # Próximos 7 dias

    plt.plot(days_real, real_last_5_days, label='Últimos 5 dias', marker='o')
    plt.plot(days_future, future_predictions, label='Próximos 7 dias', marker='o')

    plt.plot(days_real_ph, real_last_5_days_ph, label='Últimos 5 dias', marker='o')
    plt.plot(days_future_ph, future_predictions_ph, label='Próximos 7 dias', marker='o')

    # Destacar o melhor dia para comprar e vender
    plt.scatter(best_day_buy, future_predictions[best_day_buy - 1], color='green', label='Melhor Dia para Comprar', marker='^', s=100)
    plt.scatter(best_day_sell, future_predictions[best_day_sell - 1], color='red', label='Melhor Dia para Vender', marker='v', s=100)

    plt.scatter(best_day_buy_ph, future_predictions_ph[best_day_buy_ph - 1], color='green', label='Melhor Dia para Comprar', marker='^', s=100)
    plt.scatter(best_day_sell_ph, future_predictions_ph[best_day_sell_ph - 1], color='red', label='Melhor Dia para Vender', marker='v', s=100)

    # Configuração do gráfico
    plt.title(f'Previsão de Preços para {crypto}')
    plt.legend()

    # Ajustar o caminho para salvar a imagem na pasta 'public' do Next.js
    current_dir = os.path.dirname(__file__)
    image_path_lstm = os.path.join(current_dir, '../nextjs-app/public/lstm_prediction_plot.png')
    plt.savefig(image_path_lstm)
    plt.close()

    # Ajustar o caminho para salvar a imagem na pasta 'public' do Next.js
    current_dir_ph = os.path.dirname(__file__)
    image_path_ph = os.path.join(current_dir_ph, '../nextjs-app/public/prophet_prediction_plot.png')
    plt.savefig(image_path_ph)
    plt.close()

    # Formatar as previsões para exibir no frontend
    predictions = [f"Dia {i+1}: Previsão de fechamento: {float(price):.2f}" for i, price in enumerate(future_predictions)]

    # Formatar as previsões para exibir no frontend
    predictions_ph = [f"Dia {i+1}: Previsão de fechamento: {float(price):.2f}" for i, price in enumerate(future_predictions_ph)]

    return {"imageUrl": "/lstm_prediction_plot.png", "predictions": predictions}

# Rota POST para previsões
@app.post("/predict_prophet")
async def post_predict_prophet(request: CryptoRequest):
    crypto = request.crypto
    future_predictions_ph, real_last_5_days_ph = predict_with_prophet(crypto)

    # Encontrando o melhor dia para comprar e vender
    best_day_buy_ph = np.argmin(future_predictions_ph) + 1  # Melhor dia para comprar (menor valor)
    best_day_sell_ph = np.argmax(future_predictions_ph) + 1  # Melhor dia para vender (maior valor)

    # Plota o gráfico e salva na pasta estática do Next.js
    plt.figure(figsize=(10, 5))
    days_real_ph = np.arange(-5, 0)  # Últimos 5 dias
    days_future_ph = np.arange(1, 8)  # Próximos 7 dias

    plt.plot(days_real_ph, real_last_5_days_ph, label='Últimos 5 dias', marker='o')
    plt.plot(days_future_ph, future_predictions_ph, label='Próximos 7 dias', marker='o')

    plt.scatter(best_day_buy_ph, future_predictions_ph[best_day_buy_ph - 1], color='green', label='Melhor Dia para Comprar', marker='^', s=100)
    plt.scatter(best_day_sell_ph, future_predictions_ph[best_day_sell_ph - 1], color='red', label='Melhor Dia para Vender', marker='v', s=100)

    # Configuração do gráfico
    plt.title(f'Previsão de Preços para {crypto}')
    plt.legend()

    # Ajustar o caminho para salvar a imagem na pasta 'public' do Next.js
    current_dir_ph = os.path.dirname(__file__)
    image_path_ph = os.path.join(current_dir_ph, '../nextjs-app/public/prophet_prediction_plot.png')  # Renomeado para prophet
    plt.savefig(image_path_ph)
    plt.close()

    # Formatar as previsões para exibir no frontend
    predictions_ph = [f"Dia {i+1}: Previsão de fechamento: {float(price):.2f}" for i, price in enumerate(future_predictions_ph)]

    return {"imageUrl": "/prophet_prediction_plot.png", "predictions": predictions_ph}

# # Importações
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import matplotlib.pyplot as plt
# import numpy as np
# from model import train_and_save_model, predict_with_prophet, predict_crypto
# import os

# # Inicializar o FastAPI
# app = FastAPI()

# # Configuração do CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],  # Domínio do Next.js
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Definir o formato da entrada de dados usando Pydantic
# class CryptoRequest(BaseModel):
#     crypto: str
    
# # Rota POST para previsões
# @app.post("/predict")
# async def post_predict(request: CryptoRequest):
#     crypto = request.crypto
#     future_predictions, real_last_5_days = predict_crypto(crypto)
#     future_predictions_ph, real_last_5_days_ph = predict_with_prophet(crypto)
    
#     # Encontrando o melhor dia para comprar e vender (LSTM)
#     best_day_buy = np.argmin(future_predictions) + 1  # Melhor dia para comprar (menor valor)
#     best_day_sell = np.argmax(future_predictions) + 1  # Melhor dia para vender (maior valor)

#     # Encontrando o melhor dia para comprar e vender (Prophet)
#     best_day_buy_ph = np.argmin(future_predictions_ph) + 1  # Melhor dia para comprar (menor valor)
#     best_day_sell_ph = np.argmax(future_predictions_ph) + 1  # Melhor dia para vender (maior valor)

#     # Plotar gráfico para o LSTM
#     plt.figure(figsize=(10, 5))
#     days_real = np.arange(-5, 0)  # Últimos 5 dias
#     days_future = np.arange(1, 8)  # Próximos 7 dias

#     plt.plot(days_real, real_last_5_days, label='Últimos 5 dias (LSTM)', marker='o')
#     plt.plot(days_future, future_predictions, label='Próximos 7 dias (LSTM)', marker='o')

#     # Destacar o melhor dia para comprar e vender no gráfico (LSTM)
#     plt.scatter(best_day_buy, future_predictions[best_day_buy - 1], color='green', label='Melhor Dia para Comprar (LSTM)', marker='^', s=100)
#     plt.scatter(best_day_sell, future_predictions[best_day_sell - 1], color='red', label='Melhor Dia para Vender (LSTM)', marker='v', s=100)

#     plt.title(f'Previsão de Preços para {crypto} (LSTM)')
#     plt.legend()

#     # Ajustar o caminho para salvar a imagem do LSTM
#     current_dir = os.path.dirname(__file__)
#     image_path_lstm = os.path.join(current_dir, '../nextjs-app/public/lstm_prediction_plot.png')
#     plt.savefig(image_path_lstm)
#     plt.close()

#     # Plotar gráfico para o Prophet
#     plt.figure(figsize=(10, 5))
#     days_real_ph = np.arange(-5, 0)  # Últimos 5 dias
#     days_future_ph = np.arange(1, 8)  # Próximos 7 dias

#     plt.plot(days_real_ph, real_last_5_days_ph, label='Últimos 5 dias (Prophet)', marker='o')
#     plt.plot(days_future_ph, future_predictions_ph, label='Próximos 7 dias (Prophet)', marker='o')

#     # Destacar o melhor dia para comprar e vender no gráfico (Prophet)
#     plt.scatter(best_day_buy_ph, future_predictions_ph[best_day_buy_ph - 1], color='green', label='Melhor Dia para Comprar (Prophet)', marker='^', s=100)
#     plt.scatter(best_day_sell_ph, future_predictions_ph[best_day_sell_ph - 1], color='red', label='Melhor Dia para Vender (Prophet)', marker='v', s=100)

#     plt.title(f'Previsão de Preços para {crypto} (Prophet)')
#     plt.legend()

#     # Ajustar o caminho para salvar a imagem do Prophet
#     image_path_ph = os.path.join(current_dir, '../nextjs-app/public/prophet_prediction_plot.png')
#     plt.savefig(image_path_ph)
#     plt.close()

#     # Formatar as previsões para exibir no frontend
#     predictions = [f"Dia {i+1}: Previsão de fechamento (LSTM): {float(price):.2f}" for i, price in enumerate(future_predictions)]
#     predictions_ph = [f"Dia {i+1}: Previsão de fechamento (Prophet): {float(price):.2f}" for i, price in enumerate(future_predictions_ph)]

#     return {
#         "imageUrl_lstm": "/lstm_prediction_plot.png",
#         "predictions_lstm": predictions,
#         "imageUrl_prophet": "/prophet_prediction_plot.png",
#         "predictions_prophet": predictions_ph
#     }


# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import matplotlib.pyplot as plt
# import numpy as np
# from model import predict_with_lstm, predict_with_prophet
# import os

# app = FastAPI()

# # Configuração do CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],  # Domínio do Next.js
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class CryptoRequest(BaseModel):
#     crypto: str

# # Rota para previsão com LSTM
# @app.post("/predict_lstm")
# async def predict_lstm(request: CryptoRequest):
#     crypto = request.crypto
#     future_predictions, real_last_5_days, accuracy = predict_with_lstm(crypto)

#     # Gerar gráfico LSTM
#     plt.figure(figsize=(10, 5))
#     days_real = np.arange(-5, 0)
#     days_future = np.arange(1, 8)
#     plt.plot(days_real, real_last_5_days, label='Últimos 5 dias (LSTM)', marker='o')
#     plt.plot(days_future, future_predictions, label='Próximos 7 dias (LSTM)', marker='o')

#     plt.title(f'Previsão de Preços para {crypto} (LSTM)')
#     plt.legend()
    
#     # Salvar imagem
#     current_dir = os.path.dirname(__file__)
#     image_path = os.path.join(current_dir, 'static', 'lstm_prediction.png')
#     plt.savefig(image_path)
#     plt.close()

#     return {
#         "imageUrl": "/static/lstm_prediction.png",
#         "accuracy": accuracy,
#         "predictions": future_predictions.tolist()
#     }

# # Rota para previsão com Prophet
# @app.post("/predict_prophet")
# async def predict_prophet(request: CryptoRequest):
#     crypto = request.crypto
#     future_predictions, real_last_5_days, accuracy = predict_with_prophet(crypto)

#     # Gerar gráfico Prophet
#     plt.figure(figsize=(10, 5))
#     days_real = np.arange(-5, 0)
#     days_future = np.arange(1, 8)
#     plt.plot(days_real, real_last_5_days, label='Últimos 5 dias (Prophet)', marker='o')
#     plt.plot(days_future, future_predictions, label='Próximos 7 dias (Prophet)', marker='o')

#     plt.title(f'Previsão de Preços para {crypto} (Prophet)')
#     plt.legend()

#     # Salvar imagem
#     current_dir = os.path.dirname(__file__)
#     image_path = os.path.join(current_dir, 'static', 'prophet_prediction.png')
#     plt.savefig(image_path)
#     plt.close()

#     return {
#         "imageUrl": "/static/prophet_prediction.png",
#         "accuracy": accuracy,
#         "predictions": future_predictions.tolist()
#     }
