---
sidebar_position: 2
---

# Construção de Dockerfile/Docker Compose para Microsserviço

# Dockerização e DataLake

## Dockerização

&emsp; Nesta atividade, optei por encapsular um Microsserviço utilizando Docker e Docker Compose, com foco em fornecer um ambiente isolado, escalável e de fácil manutenção. O microsserviço é responsável pela previsão de preços de criptoativos, utilizando machine learning (com modelos LSTM e Prophet) e integrando um frontend com visualização gráfica das previsões. 

&emsp; Este serviço foi projetado para se comunicar de forma eficiente com outros componentes do sistema, como o backend (FastAPI) e o frontend (Next.js), criando um ambiente completo para análise e visualização de dados.
Arquivos de Deployment

### 1. Dockerfile

&emsp; O Dockerfile define a imagem customizada do backend baseado em FastAPI, que será utilizado para servir a API de previsão de preços. A escolha por criar um Dockerfile permite um ambiente consistente, independente do sistema operacional, encapsulando todas as dependências necessárias para rodar o serviço.

```bash
# Usar a imagem oficial do Python
FROM python:3.9-slim

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar o arquivo de dependências
COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação
COPY . .

# Expor a porta 8000 para o FastAPI
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

&emsp; O Dockerfile para o backend FastAPI oferece as seguintes vantagens:

    * Reprodutibilidade: A aplicação sempre será executada no mesmo ambiente, eliminando problemas de configuração de dependências locais.

    * Escalabilidade: Ao utilizar containers, é possível escalar o microsserviço facilmente em um ambiente de produção.
    
    * Modularidade: O Dockerfile encapsula apenas o backend, permitindo a separação clara entre backend, frontend e banco de dados, garantindo flexibilidade no desenvolvimento e manutenção.

### 2. docker-compose.yml

&emsp; O arquivo docker-compose.yml orquestra a execução de múltiplos containers, incluindo o backend FastAPI, o frontend Next.js e um banco de dados Postgres. Ele facilita a construção de um ambiente completo para o projeto, gerenciando a comunicação entre os serviços.

```yml
version: '3.8'

services:
  backend:
    build: ./backend
    container_name: fastapi-backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    depends_on:
      - postgres
    environment:
      - DATABASE_URL=postgresql://user:password@postgres/dbname

  frontend:
    build: ./frontend
    container_name: nextjs-frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
    depends_on:
      - backend

  postgres:
    image: postgres:13
    container_name: postgres-db
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: dbname
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  postgres-data:
```
### Justificativa para o Uso de Microsserviço

&emsp; A escolha pelo uso de microsserviços, em vez de um monolito, se justifica por vários fatores relacionados à modularidade, manutenção e escalabilidade do sistema:

#### 1. Escalabilidade e Isolamento:

    * Cada serviço (backend, frontend, banco de dados) roda em seu próprio container isolado, o que facilita o escalonamento independente. Se o backend precisar de mais recursos para processar previsões de criptoativos, ele pode ser escalado sem afetar o frontend ou o banco de dados.
    
    * Isso permite uma alocação de recursos mais eficiente em um ambiente de produção, reduzindo o risco de gargalos em partes específicas do sistema.

#### 2. Facilidade de Atualização:

    * Como os microsserviços são independentes, a atualização de um não afeta os outros. Por exemplo, o backend com o FastAPI pode ser atualizado com novos modelos de machine learning sem necessidade de alterações no frontend.
    
    * Além disso, o Docker Compose facilita o processo de deploy. Com um simples comando (docker-compose up --build), o ambiente completo pode ser reconstruído e atualizado.

#### 3. Separação de Responsabilidades:

    * O backend cuida exclusivamente das previsões de preços e da lógica de negócios, enquanto o frontend (Next.js) trata da interface e visualização dos resultados. Essa separação clara torna o código mais modular e fácil de manter.
    
    * Microsserviços promovem um design mais limpo e permitem que equipes diferentes trabalhem em partes independentes do sistema.

#### 4. Interoperabilidade:

    * Microsserviços permitem fácil integração de novos componentes ou serviços no futuro. Se, por exemplo, decidirmos adicionar novos modelos de previsão ou outro serviço para análise de dados, o sistema pode ser estendido sem grandes mudanças arquiteturais.

## DataLake

### Justificativa: Por que Não Utilize o Data Lake (MinIO)

&emsp; A decisão de não utilizar um Data Lake, como o MinIO, neste projeto foi baseada em fatores chave relacionados às necessidades específicas do sistema. O foco principal do projeto é a previsão de preços de criptoativos com dados estruturados, armazenados e processados em um banco de dados relacional (PostgreSQL). Os motivos são:

  #### 1. Natureza Estruturada dos Dados: 
    * Estamos lidando com dados financeiros bem organizados (históricos de preços), que são gerenciados eficientemente em um banco de dados relacional, sem a necessidade de armazenamento para dados não estruturados.

  #### 2.Complexidade Desnecessária: 
    * A introdução de um Data Lake adicionaria complexidade à arquitetura, sem ganhos significativos para este volume e tipo de dados. O PostgreSQL atende completamente às necessidades do projeto.

  #### 3. Escopo e Volume Moderado de Dados: 
    * O volume de dados e o processamento envolvido no projeto são moderados e podem ser facilmente tratados por um banco relacional, sem exigir a escalabilidade oferecida por um Data Lake.


## Conclusão

&emsp; A escolha pelo uso de um microsserviço encapsulado em containers Docker foi justificada pela necessidade de escalabilidade, modularidade e facilidade de manutenção. A arquitetura baseada em Docker Compose facilita a criação de um ambiente completo, onde cada serviço funciona de maneira independente, permitindo fácil integração, manutenção e futuras expansões. Comentando sobre o datalake concluimos portanto que, a escolha de não usar o MinIO foi feita para simplificar a arquitetura e focar em soluções já adequadas às características dos dados e ao objetivo do projeto.