# Dockerfile per il frontend React
FROM node:18-alpine AS builder

# Imposta directory di lavoro
WORKDIR /app

# Copia package files
COPY package*.json ./

# Installa dipendenze
RUN npm ci --only=production

# Copia il codice sorgente
COPY . .

# Build dell'applicazione
RUN npm run build

# Stage di produzione con nginx
FROM nginx:alpine

# Copia la build dal stage precedente
COPY --from=builder /app/dist /usr/share/nginx/html

# Copia configurazione nginx personalizzata
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Espone la porta 80
EXPOSE 80

# Comando di avvio
CMD ["nginx", "-g", "daemon off;"]
