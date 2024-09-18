---
sidebar_position: 2
---

# Pergunta 2

# Foi construída uma narrativa de dados que justifica a escolha dos modelos e dados;

## Narrativa de Dados: Justificativa do Modelo ARIMA

&emsp;Agora que temos os dados explorados, podemos construir a narrativa para justificar o uso do ARIMA com base nos pontos fortes e fracos:
## Pontos Fortes do ARIMA:

    * Modelo clássico para séries temporais: O ARIMA é amplamente utilizado em previsões de séries temporais financeiras, como o preço de criptoativos, pois considera tanto a autocorrelação entre os dados quanto as diferenças nas tendências ao longo do tempo.

    * Capacidade de capturar padrões históricos: O ARIMA é adequado para capturar padrões históricos de preço ao remover tendências (com diferenciação) e analisar a relação entre valores passados (autocorrelação).

    * Facilidade de implementação e ajuste: Comparado a modelos mais complexos, o ARIMA é relativamente simples de ajustar e interpretar, com poucos parâmetros a configurar (p, d, q).

    * Estacionariedade dos dados: Com a diferenciação dos dados, como mostrado pelo teste de Dickey-Fuller, o ARIMA se torna uma escolha eficaz para modelar séries temporais estacionárias.

## Pontos Fracos do ARIMA:

    * Desempenho em séries não estacionárias: O ARIMA pode não ser o mais adequado para séries que apresentam grande volatilidade ou comportamento não linear, o que pode ser comum em criptoativos.

    * Limitação em capturar longos ciclos: O ARIMA tem dificuldade em capturar ciclos longos ou complexos sem ajustes adicionais. Se a série temporal apresenta sazonalidade, um modelo como SARIMA (que adiciona componentes sazonais) pode ser mais adequado.

    * Sensível a mudanças bruscas: O ARIMA não lida bem com mudanças repentinas no mercado (e.g., crash de preços de criptos devido a eventos externos), o que pode ser um problema para criptoativos altamente voláteis.

# Melhorias Potenciais:

    * SARIMA: Se os dados mostrarem padrões sazonais (variações cíclicas), uma versão sazonal do ARIMA (SARIMA) pode ser mais eficaz.

    * Modelos LSTM: Caso haja padrões complexos ou dependências de longo prazo que o ARIMA não captura, modelos baseados em redes neurais como LSTM podem complementar a análise.

# Conclusão da Narrativa:

&emsp; Baseando-se na análise dos dados e na transformação para garantir a estacionariedade, o ARIMA é uma escolha justificada para prever os preços de criptoativos no curto prazo. No entanto, o modelo pode ser limitado em situações de alta volatilidade ou mudanças bruscas, o que abre espaço para testes futuros com modelos mais complexos.