#!/bin/bash

# Script per configurare HTTPS con Let's Encrypt
# Uso: ./setup-ssl.sh tuodominio.com

if [ $# -eq 0 ]; then
    echo "❌ Errore: Specifica il dominio"
    echo "Uso: ./setup-ssl.sh tuodominio.com"
    exit 1
fi

DOMAIN=$1
EMAIL="admin@${DOMAIN}"  # Cambia se necessario

echo "🚀 Configurazione SSL per ${DOMAIN}"
echo "📧 Email: ${EMAIL}"

# 1. Installa Certbot
echo "📦 Installazione Certbot..."
apt update
apt install -y certbot

# 2. Crea directory SSL
echo "📁 Creazione directory SSL..."
mkdir -p /home/fugazi/nginx/ssl

# 3. Genera certificati Let's Encrypt (modalità standalone)
echo "🔐 Generazione certificati SSL..."
certbot certonly --standalone \
    --email ${EMAIL} \
    --agree-tos \
    --no-eff-email \
    -d ${DOMAIN} \
    -d www.${DOMAIN} \
    -d api.${DOMAIN}

# 4. Copia certificati nella directory nginx
echo "📋 Copia certificati..."
cp /etc/letsencrypt/live/${DOMAIN}/fullchain.pem /home/fugazi/nginx/ssl/cert.pem
cp /etc/letsencrypt/live/${DOMAIN}/privkey.pem /home/fugazi/nginx/ssl/key.pem

# 5. Imposta permessi
chmod 644 /home/fugazi/nginx/ssl/cert.pem
chmod 600 /home/fugazi/nginx/ssl/key.pem

# 6. Aggiorna nginx.conf con il dominio corretto
sed -i "s/tuodominio.it/${DOMAIN}/g" /home/fugazi/nginx/nginx.conf

echo "✅ Configurazione SSL completata!"
echo "🌐 Domini configurati:"
echo "   - https://${DOMAIN}"
echo "   - https://www.${DOMAIN}"
echo "   - https://api.${DOMAIN}"
echo ""
echo "🔄 Ora esegui: docker compose up -d"

# 7. Configura rinnovo automatico
echo "⏰ Configurazione rinnovo automatico..."
(crontab -l 2>/dev/null; echo "0 3 * * * certbot renew --quiet && cp /etc/letsencrypt/live/${DOMAIN}/fullchain.pem /home/fugazi/nginx/ssl/cert.pem && cp /etc/letsencrypt/live/${DOMAIN}/privkey.pem /home/fugazi/nginx/ssl/key.pem && docker compose -f /home/fugazi/docker-compose.yml restart nginx") | crontab -

echo "✅ Rinnovo automatico configurato!"
