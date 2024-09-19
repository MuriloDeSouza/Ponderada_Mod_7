# Importações
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import matplotlib.pyplot as plt
import numpy as np
from model import predict_crypto
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

    # Encontrando o melhor dia para comprar e vender
    best_day_buy = np.argmin(future_predictions) + 1  # Melhor dia para comprar (menor valor)
    best_day_sell = np.argmax(future_predictions) + 1  # Melhor dia para vender (maior valor)

    # Plota o gráfico e salva na pasta estática do Next.js
    plt.figure(figsize=(10, 5))
    days_real = np.arange(-5, 0)  # Últimos 5 dias
    days_future = np.arange(1, 8)  # Próximos 7 dias

    plt.plot(days_real, real_last_5_days, label='Últimos 5 dias', marker='o')
    plt.plot(days_future, future_predictions, label='Próximos 7 dias', marker='o')

    # Destacar o melhor dia para comprar e vender
    plt.scatter(best_day_buy, future_predictions[best_day_buy - 1], color='green', label='Melhor Dia para Comprar', marker='^', s=100)
    plt.scatter(best_day_sell, future_predictions[best_day_sell - 1], color='red', label='Melhor Dia para Vender', marker='v', s=100)

    # Configuração do gráfico
    plt.title(f'Previsão de Preços para {crypto}')
    plt.legend()

    # Ajustar o caminho para salvar a imagem na pasta 'public' do Next.js
    current_dir = os.path.dirname(__file__)
    image_path = os.path.join(current_dir, '../nextjs-app/public/prediction_plot.png')
    plt.savefig(image_path)
    plt.close()

    # Formatar as previsões para exibir no frontend
    predictions = [f"Dia {i+1}: Previsão de fechamento: {float(price):.2f}" for i, price in enumerate(future_predictions)]

    return {"imageUrl": "/prediction_plot.png", "predictions": predictions}
