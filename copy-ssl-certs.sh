#!/bin/bash

# Script per copiare i certificati SSL di Let's Encrypt nella directory nginx
# Uso: ./copy-ssl-certs.sh

DOMAIN="www.fugasi.it"
NGINX_SSL_DIR="./nginx/ssl"

echo "🔐 Copia certificati SSL per ${DOMAIN}..."

# Crea la directory ssl se non esiste
mkdir -p ${NGINX_SSL_DIR}

# Controlla se i certificati esistono
if [ ! -f "/etc/letsencrypt/live/${DOMAIN}/fullchain.pem" ]; then
    echo "❌ Errore: Certificato non trovato in /etc/letsencrypt/live/${DOMAIN}/fullchain.pem"
    echo "💡 Prima genera i certificati con: ./setup-ssl.sh ${DOMAIN}"
    exit 1
fi

# Copia i certificati
echo "📋 Copia fullchain.pem..."
cp /etc/letsencrypt/live/${DOMAIN}/fullchain.pem ${NGINX_SSL_DIR}/fullchain.pem

echo "📋 Copia privkey.pem..."
cp /etc/letsencrypt/live/${DOMAIN}/privkey.pem ${NGINX_SSL_DIR}/privkey.pem

# Imposta i permessi
chmod 644 ${NGINX_SSL_DIR}/fullchain.pem
chmod 600 ${NGINX_SSL_DIR}/privkey.pem

echo "✅ Certificati copiati con successo!"
echo "📁 Certificati disponibili in: ${NGINX_SSL_DIR}/"
echo "🚀 Ora puoi eseguire: docker compose build nginx && docker compose up -d"
