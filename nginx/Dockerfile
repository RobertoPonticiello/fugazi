# Dockerfile personalizzato per nginx con certificati SSL
FROM nginx:alpine

# Crea la directory per i certificati SSL
RUN mkdir -p /etc/nginx/ssl

# Copia i certificati SSL dal server host al container
# Questi file devono esistere sul server prima del build
COPY ssl/fullchain.pem /etc/nginx/ssl/cert.pem
COPY ssl/privkey.pem /etc/nginx/ssl/key.pem

# Imposta i permessi corretti per i certificati
RUN chmod 644 /etc/nginx/ssl/cert.pem && \
    chmod 600 /etc/nginx/ssl/key.pem

# Copia la configurazione nginx personalizzata
COPY nginx.conf /etc/nginx/nginx.conf

# Espone le porte 80 e 443
EXPOSE 80 443

# Comando di avvio
CMD ["nginx", "-g", "daemon off;"]
