# Importações
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import matplotlib.pyplot as plt
import numpy as np
from model import train_and_save_model, predict_with_prophet, predict_crypto
import os
from fpdf import FPDF
import time
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime


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

# Estrutura para armazenar os logs de previsões (em memória para simplificar)
logs = []

# Classe para representar uma requisição de log
class LogEntry(BaseModel):
    crypto: str
    model: str
    timestamp: datetime

# Endpoint para salvar um novo log
@app.post("/api/logs")
async def save_log(log_entry: LogEntry):  # Mudei de "logs" para "log_entry"
    logs.append(log_entry.dict())  # Salva o log no "banco de dados" (neste caso, na memória)
    print(logs)
    return {"message": "Log salvo com sucesso"}

# Endpoint para buscar o histórico de logs
@app.get("/api/logs")
async def get_logs():
    print("bati aqui na rota de get")
    return logs

# Função para gerar o PDF
def create_pdf(filename: str, crypto: str):
    pdf = FPDF()

    # Supondo que os gráficos já estejam salvos como arquivos de imagem:
    image_lstm = f'../nextjs-app/public/lstm_prediction_plot.png'
    image_prophet = f'../nextjs-app/public/prophet_prediction_plot.png'
    image_lstm_ph = f'../nextjs-app/public/lstm_Ph_prediction_plot.png'
    
    # Adicionar primeira imagem (LSTM)
    if os.path.exists(image_lstm):
        pdf.add_page()
        pdf.image(image_lstm, x=10, y=10, w=180)

    # Adicionar segunda imagem (Prophet)
    elif os.path.exists(image_prophet):
        pdf.add_page()
        pdf.image(image_prophet, x=10, y=10, w=180)
    
    elif os.path.exists(image_lstm_ph):
        pdf.add_page()
        pdf.image(image_lstm_ph, x=10, y=10, w=180)

    # Salvar o PDF no servidor
    pdf.output(filename)

# Rota para gerar e servir o PDF
@app.post("/generate-pdf")
async def generate_pdf(request: CryptoRequest, background_tasks: BackgroundTasks):
    crypto = request.crypto
    pdf_filename = f"{crypto}_report.pdf"
    pdf_path = os.path.join(os.getcwd(), pdf_filename)

    # Gera o PDF em background
    background_tasks.add_task(create_pdf, pdf_path, crypto)

    # Retorna o caminho do PDF para o frontend
    pdf_url = f"/download-pdf/{pdf_filename}"
    return {"pdf_url": pdf_url}


# Rota para servir o PDF gerado de forma dinâmica
@app.get("/download-pdf/{filename}")
async def download_pdf(filename: str):
    file_path = os.path.join(os.getcwd(), filename)
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=filename, media_type='application/pdf')
    return {"error": "Arquivo não encontrado"}


@app.post("/comparation")
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
    days_future_ph = np.arange(1, 8)  # Próximos 7 dias

    plt.plot(days_real, real_last_5_days, label='Últimos 5 dias', marker='o')
    plt.plot(days_future, future_predictions, label='Próximos 7 dias (LSTM)', marker='o')
    plt.plot(days_future_ph, future_predictions_ph, label='Próximos 7 dias (Prophet)', marker='o')

    # Destacar o melhor dia para comprar e vender
    plt.scatter(best_day_buy, future_predictions[best_day_buy - 1], color='green', label='Melhor Dia para Comprar (LSTM)', marker='^', s=100)
    plt.scatter(best_day_sell, future_predictions[best_day_sell - 1], color='red', label='Melhor Dia para Vender (LSTM)', marker='v', s=100)

    plt.scatter(best_day_buy_ph, future_predictions_ph[best_day_buy_ph - 1], color='green', label='Melhor Dia para Comprar (Prophet)', marker='^', s=100)
    plt.scatter(best_day_sell_ph, future_predictions_ph[best_day_sell_ph - 1], color='red', label='Melhor Dia para Vender (Prophet)', marker='v', s=100)

    # Configuração do gráfico
    plt.title(f'Previsão de Preços para {crypto} em dólares (USD)')
    plt.legend()

    # Ajustar o caminho para salvar a imagem na pasta 'public' do Next.js
    current_dir = os.path.dirname(__file__)
    image_path_lstm = os.path.join(current_dir, '../nextjs-app/public/lstm_Ph_prediction_plot.png')
    plt.savefig(image_path_lstm)
    plt.close()

    # Formatar as previsões para exibir no frontend
    predictions = [f"Dia {i+1}: Previsão de fechamento: R$ {float(price*5.53):.2f}" for i, price in enumerate(future_predictions)]

    return {"imageUrl": "/lstm_Ph_prediction_plot.png", "predictions": predictions}

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
    plt.plot(days_future, future_predictions, label='Próximos 7 dias (LSTM)', marker='o')

    # Destacar o melhor dia para comprar e vender
    plt.scatter(best_day_buy, future_predictions[best_day_buy - 1], color='green', label='Melhor Dia para Comprar (LSTM)', marker='^', s=100)
    plt.scatter(best_day_sell, future_predictions[best_day_sell - 1], color='red', label='Melhor Dia para Vender (LSTM)', marker='v', s=100)

    # Configuração do gráfico
    plt.title(f'Previsão de Preços para {crypto} em dólares (USD)')
    plt.legend()

    # Ajustar o caminho para salvar a imagem na pasta 'public' do Next.js
    current_dir = os.path.dirname(__file__)
    image_path_lstm = os.path.join(current_dir, '../nextjs-app/public/lstm_prediction_plot.png')
    plt.savefig(image_path_lstm)
    plt.close()

    # Formatar as previsões para exibir no frontend
    predictions = [f"Dia {i+1}: Previsão de fechamento: R$ {float(price*5.53):.2f}" for i, price in enumerate(future_predictions)]

    return {"imageUrl": "/lstm_prediction_plot.png", "predictions": predictions}

# Rota POST para previsões Prophet
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
    plt.plot(days_future_ph, future_predictions_ph, label='Próximos 7 dias (Prophet)', marker='o')

    plt.scatter(best_day_buy_ph, future_predictions_ph[best_day_buy_ph - 1], color='green', label='Melhor Dia para Comprar (Prophet)', marker='^', s=100)
    plt.scatter(best_day_sell_ph, future_predictions_ph[best_day_sell_ph - 1], color='red', label='Melhor Dia para Vender (Prophet)', marker='v', s=100)

    # Configuração do gráfico
    plt.title(f'Previsão de Preços para {crypto} em dólares (USD)')
    plt.legend()

    # Ajustar o caminho para salvar a imagem na pasta 'public' do Next.js
    current_dir_ph = os.path.dirname(__file__)
    image_path_ph = os.path.join(current_dir_ph, '../nextjs-app/public/prophet_prediction_plot.png')  # Renomeado para prophet
    plt.savefig(image_path_ph)
    plt.close()

    # Formatar as previsões para exibir no frontend
    predictions_ph = [f"Dia {i+1}: Previsão de fechamento: R$ {float(price*5.53):.2f}" for i, price in enumerate(future_predictions_ph)]

    return {"imageUrl": "/prophet_prediction_plot.png", "predictions": predictions_ph}  # Certifique-se que o nome corresponde ao esperado no frontend
