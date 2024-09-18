from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
from src.backend.model import predict_crypto

app = FastAPI()
templates = Jinja2Templates(directory="src/frontend/templates")

# Rota para a página inicial
@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    cryptos = ["BTC-USD", "ETH-USD", "BNB-USD"]  # Exemplos de criptoativos
    return templates.TemplateResponse("index.html", {"request": request, "cryptos": cryptos})

# Rota para fazer previsões
@app.post("/predict", response_class=HTMLResponse)
async def post_predict(request: Request, crypto: str = Form(...)):
    # Obtém as previsões usando a função predict_crypto
    future_predictions, real_last_5_days = predict_crypto(crypto)

    # Plota o gráfico
    plt.figure(figsize=(10, 5))
    days_real = np.arange(-5, 0)
    days_future = np.arange(1, 8)
    plt.plot(days_real, real_last_5_days, label='Últimos 5 dias', marker='o')
    plt.plot(days_future, future_predictions, label='Próximos 7 dias', marker='o')
    plt.title(f'Previsão de Preços para {crypto}')
    plt.legend()
    plt.savefig("src/frontend/static/prediction_plot.png")
    plt.close()

    # Retorna o template com os dados e o gráfico
    return templates.TemplateResponse("index.html", {"request": request, "cryptos": ["BTC-USD", "ETH-USD", "BNB-USD"], "image": "/static/prediction_plot.png"})
