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

    # Plota o gráfico e salva na pasta estática do Next.js
    plt.figure(figsize=(10, 5))
    days_real = np.arange(-5, 0)
    days_future = np.arange(1, 8)
    plt.plot(days_real, real_last_5_days, label='Últimos 5 dias', marker='o')
    plt.plot(days_future, future_predictions, label='Próximos 7 dias', marker='o')
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





# from fastapi import FastAPI, Request, Form
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# import yfinance as yf
# import matplotlib.pyplot as plt
# import numpy as np
# from model import predict_crypto
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()
# # templates = Jinja2Templates(directory="../frontend/templates")

# # Configuração de CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],  # Domínio do Next.js
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # # Rota para a página inicial
# # @app.get("/", response_class=HTMLResponse)
# # async def get_home(request: Request):
# #     return templates.TemplateResponse("index.html", {"request": request})

# # # Rota para a página inicial
# # @app.get("/", response_class=HTMLResponse)
# # async def get_home(request: Request):
# #     cryptos = ["BTC-USD", "ETH-USD", "BNB-USD"]  # Exemplos de criptoativos
# #     return templates.TemplateResponse("index.html", {"request": request, "cryptos": cryptos})

# @app.post("/predict")
# async def post_predict(crypto: str):
#     future_predictions, real_last_5_days = predict_crypto(crypto)

#     # Plota o gráfico e salva na pasta estática do Next.js
#     plt.figure(figsize=(10, 5))
#     days_real = np.arange(-5, 0)
#     days_future = np.arange(1, 8)
#     plt.plot(days_real, real_last_5_days, label='Últimos 5 dias', marker='o')
#     plt.plot(days_future, future_predictions, label='Próximos 7 dias', marker='o')
#     plt.title(f'Previsão de Preços para {crypto}')
#     plt.legend()
#     image_path = "../nextjs-app/public/prediction_plot.png"
#     plt.savefig(image_path)
#     plt.close()

#     # Formatar as previsões para exibir no frontend
#     predictions = [f"Dia {i+1}: Previsão de fechamento: {price:.2f}" for i, price in enumerate(future_predictions)]

#     return {"imageUrl": "/prediction_plot.png", "predictions": predictions}


# # # Rota para a página inicial
# # @app.post("/testes", response_class=HTMLResponse)
# # async def post_testes(request: Request):
# #     cryptos = ["BTC-USD", "ETH-USD", "BNB-USD", "USDT-USD", "USDC-USD"]  # Exemplos de criptoativos
# #     return templates.TemplateResponse("testes.html", {"request": request, "cryptos": cryptos})

# # # Rota para fazer previsões
# # @app.post("/predict", response_class=HTMLResponse)
# # async def post_predict(request: Request, crypto: str = Form(...)):
# #     # Obtém as previsões usando a função predict_crypto
# #     future_predictions, real_last_5_days = predict_crypto(crypto)

# #     # Plota o gráfico
# #     plt.figure(figsize=(10, 5))
# #     days_real = np.arange(-5, 0)
# #     days_future = np.arange(1, 8)
# #     plt.plot(days_real, real_last_5_days, label='Últimos 5 dias', marker='o')
# #     plt.plot(days_future, future_predictions, label='Próximos 7 dias', marker='o')
# #     plt.title(f'Previsão de Preços para {crypto}')
# #     plt.legend()
# #     plt.savefig("../frontend/static/img/prediction_plot.png")
# #     plt.close()

# #     # Retorna o template com os dados e o gráfico
# #     return templates.TemplateResponse("index.html", {"request": request, "cryptos": ["BTC-USD", "ETH-USD", "BNB-USD"], "image": "/home/inteli/Documentos/GitHub/Ponderada_Mod_7/src/frontend/static/img/prediction_plot.png"})
