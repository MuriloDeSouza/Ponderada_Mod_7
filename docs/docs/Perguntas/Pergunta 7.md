---
sidebar_position: 6
---

# Pergunta 7

# A utilização do sistema é armazenada (logs de uso do sistema)

## Entendimento da página de logs

&emsp; Sim, o sistema foi projetado para registrar logs de uso, capturando informações sobre as interações dos usuários e o desempenho do modelo. Esses logs são úteis para monitorar a utilização do sistema, diagnosticar problemas e realizar auditorias.

&emsp; Logs armazenados:

* Ações dos usuários: Cada vez que um usuário solicita uma previsão ou interage com o sistema, uma entrada de log é criada com o timestamp, criptoativo selecionado e o resultado da previsão.

* Erros e exceções: Falhas no sistema são registradas para facilitar a depuração e a melhoria contínua do sistema.

* Métricas de desempenho do modelo: Informações sobre o tempo de resposta do modelo e a acurácia das previsões são registradas.

## Como está a aplicação no backend para os logs

Aqui se define uma lista vazia para podermos salvar as interações que fizemos predizendo
```bash
# Estrutura para armazenar os logs de previsões (em memória para simplificar)
logs = []

```

Aqui estamos definindo a estrutura dos dados que vamos receber para plotar na página de logs
```bash
# Classe para representar uma requisição de log
class LogEntry(BaseModel):
    crypto: str
    model: str
    timestamp: datetime
```

Aqui temos a criação do método post para que, quando os botões de previsão forem apertados, vamos add na lista vazia para poder salvar.
```bash
# Endpoint para salvar um novo log
@app.post("/api/logs")
async def save_log(log_entry: LogEntry):  # Mudei de "logs" para "log_entry"
    logs.append(log_entry.dict())  # Salva o log no "banco de dados" (neste caso, na memória)
    print(logs)
    return {"message": "Log salvo com sucesso"}
```

Agora, nos temos a rota de get para pegar os logs e mostrar na página que eu fiz
```bash
# Endpoint para buscar o histórico de logs
@app.get("/api/logs")
async def get_logs():
    print("bati aqui na rota de get")
    return logs
```

Na parte do front, dentro do CryptoForm, temos o botão de "Ver Histórico de Previsões" para que ele nos leve para a devida página.
```bash
<div className="mt-4">
      <Link href="/logs">
         <button className="p-2 bg-gray-500 text-white rounded-md">Ver Histórico de Previsões</button>
      </Link>
    </div>
```

Agora, um exemplo de como estamos implementando as rotas dentro dos botões para que cadastre na página de log
(parte do botão padrão dos modelos)
```bash
const handlePredictLSTMandPh = async () => {
    setLoading(true);
    setLstmAndProphet(false);
    setShowPdfButton(false); // Reseta botão de PDF ao carregar
    try {
      const response = await axios.post('http://localhost:8000/comparation', { crypto });
      const { imageUrl, predictions } = response.data;
      onPrediction(imageUrl, predictions);
      setLstmAndProphet(true);
      setShowPdfButton(true);
```

Introdução da função de salvamento na página de logs.
```bash
      await axios.post('http://localhost:8000/api/logs', {
        crypto: 'BTC-USD',  // Exemplo, pode ser dinâmico
        model: 'LSTMandProphet',
        timestamp: new Date().toISOString()
      });
      console.log('Log salvo com sucesso');
    } catch (error) {
      console.error('Erro ao salvar log:', error);
    }
    setLoading(false);
  };
```



