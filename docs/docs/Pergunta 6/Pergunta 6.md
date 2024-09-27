---
sidebar_position: 5
---

# Pergunta 6

# Existe um planejamento para que o modelo possa ser retreiando com novos dados;

&emsp; Sim, o sistema foi planejado para permitir o retreinamento contínuo do modelo com novos dados. O planejamento envolve a coleta de novos dados de criptoativos em intervalos regulares e a atualização do modelo LSTM para melhorar a acurácia à medida que novos padrões de mercado surgem.

## Processos de retreinamento:

1. Coleta de novos dados: Utilizamos uma API de mercado financeiro para obter os dados de preços históricos e os preços mais recentes dos criptoativos.

2. Pré-processamento: Os novos dados são processados, normalizados e convertidos para o formato utilizado pelo LSTM.

3. Treinamento incremental: O modelo LSTM é retreinado utilizando os novos dados para ajustar suas previsões futuras, mantendo um histórico de dados relevante.

**(Vale destacar que, conforme o "barema" está mencionando um planejamento do sobre o retreino do modelo, elaborei esse código como uma atualização futura para podermos implementar no código, naparte do backand (main.py))**

## Exemplo de código para retreinamento no backend (FastAPI):

```bash
# Função para retreinar o modelo
@router.post("/retrain")
async def retrain_model():
    # Busca novos dados de preços do criptoativo
    new_data = fetch_new_data()

    # Carrega o modelo previamente treinado
    lstm = LSTMModel.load('models/lstm_model.h5')

    # Treina novamente o modelo com os novos dados
    lstm.train(new_data['features'], new_data['labels'])

    # Salva o modelo atualizado
    lstm.save('models/lstm_model.h5')

    return {"message": "Modelo retreinado com sucesso!"}
```

&emsp; Neste exemplo, um endpoint /retrain permite o retreinamento manual do modelo LSTM com novos dados, que podem ser coletados a partir de uma API financeira. Este planejamento pode ser automatizado para rodar em intervalos regulares ou sob demanda.

# Conclusão:

&emsp; 