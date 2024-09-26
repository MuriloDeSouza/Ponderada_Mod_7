---
sidebar_position: 4
---

# Pergunta 4

# Existe um dashboard que apresenta os resultados do modelo:

## Dashboard de apresentação

&emsp; Sim, o sistema inclui um dashboard interativo que exibe os resultados das previsões dos modelos LSTM e Prophet. 
&emsp; O frontend foi implementado utilizando Next.js, o que permite uma visualização clara dos resultados, com gráficos que mostram tanto as previsões futuras quanto os dados históricos de preços dos criptoativos.

&emsp; Os resultados de cada previsão são apresentados visualmente com gráficos gerados via Matplotlib, que são atualizados dinamicamente de acordo com as requisições feitas pelos usuários.

&emsp; Exemplo de código gerando os gráficos para o LSTM:

```bash
# Gerar e salvar gráfico da previsão do modelo LSTM
plt.figure(figsize=(10, 5))
plt.plot(real_data, label="Fechamentos reais")
plt.plot(predictions, label="Previsões LSTM")
plt.legend()
plt.savefig("/nextjs-app/public/lstm_prediction_plot.png")
```

&emsp; Na parte do backend ficou dessa maneira para que os gráficos fossem gerados:
