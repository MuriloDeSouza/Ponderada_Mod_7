---
sidebar_position: 2
---

# Pergunta 2

# Foi construída uma narrativa de dados que justifica a escolha dos modelos e dados;

## Narrativa de Dados: Justificativa do Modelo LSTM

&emsp;Depois que ocorreu a exploração dos dados, vamos construir uma narrativa para justificar o uso do modelo LSTM (Long Short-Term Memory) com base nos pontos fortes e fracos, comparando com o modelo ARIMA (modelo que eu iria utilizar se não fosse o LSTM).

## Pontos Fortes do LSTM:

    * Capacidade de Capturar Padrões de Longo Prazo e Não Lineares: O modelo LSTM é uma rede neural recorrente que lida bem com dependências temporais complexas e não lineares, algo crucial para prever os preços de criptoativos, que tendem a ser altamente voláteis e seguir padrões imprevisíveis.

    * Memória Longa: Diferente de modelos tradicionais como o ARIMA, o LSTM tem "células de memória" que permitem armazenar informações por longos períodos, sendo eficaz em capturar tendências de longo prazo e movimentos de mercado.

    * Robustez em Dados Não Estacionários: Ao contrário do ARIMA, que requer dados estacionários, o LSTM não exige esse pré-processamento, tornando-o mais eficiente para séries temporais com volatilidade e mudanças bruscas, comuns nos preços de criptoativos.

    * Flexibilidade para Análise de Séries Temporais Voláteis: O LSTM consegue se ajustar melhor a séries temporais com alto nível de ruído e variações, como é o caso de criptomoedas, que podem sofrer influência de notícias de mercado ou eventos globais.

## Pontos Fracos do LSTM:

    * Necessidade de Grandes Quantidades de Dados: O LSTM exige um volume significativo de dados históricos para treinar o modelo de forma adequada, o que pode ser um desafio para séries temporais mais curtas.

    * Complexidade e Custo Computacional: Comparado ao ARIMA, o LSTM demanda maior poder de processamento e tempo para treinamento, devido à sua arquitetura de rede neural.

    * Interpretação Mais Difícil: Ao contrário do ARIMA, que é fácil de interpretar e ajustar, os resultados e os parâmetros do LSTM são menos intuitivos e requerem mais esforço para serem compreendidos.

## Pontos Fortes do ARIMA:

    * Modelo clássico para séries temporais: O ARIMA é amplamente utilizado em previsões de séries temporais financeiras, como o preço de criptoativos, pois considera tanto a autocorrelação entre os dados quanto as diferenças nas tendências ao longo do tempo.

    * Capacidade de capturar padrões históricos: O ARIMA é adequado para capturar padrões históricos de preço ao remover tendências (com diferenciação) e analisar a relação entre valores passados (autocorrelação).

    * Facilidade de implementação e ajuste: Comparado a modelos mais complexos, o ARIMA é relativamente simples de ajustar e interpretar, com poucos parâmetros a configurar (p, d, q).

    * Estacionariedade dos dados: Com a diferenciação dos dados, como mostrado pelo teste de Dickey-Fuller, o ARIMA se torna uma escolha eficaz para modelar séries temporais estacionárias.

## Pontos Fracos do ARIMA:

    * Desempenho em séries não estacionárias: O ARIMA pode não ser o mais adequado para séries que apresentam grande volatilidade ou comportamento não linear, o que pode ser comum em criptoativos.

    * Limitação em capturar longos ciclos: O ARIMA tem dificuldade em capturar ciclos longos ou complexos sem ajustes adicionais. Se a série temporal apresenta sazonalidade, um modelo como SARIMA (que adiciona componentes sazonais) pode ser mais adequado.

    * Sensível a mudanças bruscas: O ARIMA não lida bem com mudanças repentinas no mercado (e.g., crash de preços de criptos devido a eventos externos), o que pode ser um problema para criptoativos altamente voláteis.

## Por que não utilizamos o ARIMA:

    * Volatilidade dos Criptoativos: O ARIMA é mais indicado para séries temporais estacionárias e com padrões lineares. No entanto, criptoativos como o Bitcoin apresentam grande volatilidade e comportamentos não lineares, que o ARIMA tem dificuldades em modelar adequadamente.

    * Limitações para Capturar Padrões Complexos: O ARIMA é limitado em capturar longas dependências temporais e mudanças bruscas nos preços, características comuns em criptoativos. Por isso, o LSTM, com sua capacidade de lidar com longos ciclos e não linearidades, foi a escolha mais adequada.

    * Sazonalidade e Não Estacionariedade: Embora o ARIMA possa ser adaptado para lidar com sazonalidade (SARIMA), ele ainda apresenta dificuldades em modelar séries não estacionárias, como é o caso dos criptoativos, sem uma diferenciação contínua dos dados. O LSTM se ajusta melhor a esse tipo de dado sem necessidade de diferenciações.

# Conclusão da Narrativa:

&emsp; O LSTM foi escolhido por sua capacidade de lidar com séries temporais não estacionárias, voláteis e com padrões complexos, típicos dos criptoativos. Sua flexibilidade e robustez o tornam mais adequado para prever o comportamento dos preços de criptomoedas no curto e médio prazo, compensando as limitações de modelos tradicionais como o ARIMA.