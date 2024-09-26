# Usar imagem do Node.js como base
FROM node:20

# Define o diretório de trabalho
WORKDIR /app

# Copiar arquivos package.json e package-lock.json
COPY package*.json ./

# Instalar as dependências
RUN npm install

# Copiar o código da aplicação para dentro do contêiner
COPY . .

# Construir a aplicação
RUN npm run build

# Expõe a porta 3000 para o frontend
EXPOSE 3000

# Comando para iniciar a aplicação Next.js
CMD ["npm", "run", "start"]
