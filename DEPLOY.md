# 🚀 Guida al Deploy di Finge

## 📋 Panoramica

Finge è un'applicazione di analisi finanziaria con:
- **Backend**: FastAPI (Python) con suggerimenti degli analisti
- **Frontend**: React + TypeScript + Tailwind CSS
- **Database**: Nessuno (usa API esterne)
- **Sicurezza**: API key protette, CORS configurato, HTTPS

## 🔧 Preparazione Locale

### 1. Configurazione Variabili d'Ambiente

```bash
# Copia i file di esempio
cp env.example .env
cp backend/env.example backend/.env
cp frontend/env.example frontend/.env

# Modifica i file .env con i tuoi valori
```

### 2. Test Locale

```bash
# Backend
cd backend
source venv/bin/activate
FMP_API_KEY=la_tua_api_key python main.py

# Frontend (in un altro terminale)
cd frontend
npm install
npm run dev
```

## 🌐 Opzioni di Deploy

### Opzione A: VPS + Docker (Raccomandato)

#### Provider VPS Consigliati:
- **Hetzner**: €3.29/mese (Cloud Server CX11)
- **DigitalOcean**: $6/mese (Basic Droplet)
- **OVH**: €3.50/mese (VPS Starter)
- **Contabo**: €3.99/mese (VPS S)

#### Passi per VPS:

1. **Creazione Server**
   ```bash
   # Connettiti al server
   ssh root@tuo_server_ip
   
   # Aggiorna sistema
   apt update && apt upgrade -y
   
   # Installa Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   
   # Installa Docker Compose
   apt install docker-compose-plugin -y
   ```

2. **Configurazione Dominio**
   ```bash
   # Nel pannello Aruba, imposta:
   # A record: app.tuodominio.it -> IP_SERVER
   # A record: api.tuodominio.it -> IP_SERVER
   # A record: www.tuodominio.it -> IP_SERVER
   ```

3. **Deploy dell'Applicazione**
   ```bash
   # Clona il repository
   git clone https://github.com/tuo_username/finge.git
   cd finge
   
   # Configura variabili d'ambiente
   cp env.example .env
   nano .env  # Modifica con i tuoi valori
   
   # Genera certificati SSL
   mkdir -p nginx/ssl
   # Usa Let's Encrypt o genera certificati self-signed per test
   
   # Avvia l'applicazione
   docker-compose up -d
   ```

4. **Configurazione SSL con Let's Encrypt**
   ```bash
   # Installa Certbot
   apt install certbot -y
   
   # Genera certificati
   certbot certonly --standalone -d app.tuodominio.it -d api.tuodominio.it -d www.tuodominio.it
   
   # Copia certificati
   cp /etc/letsencrypt/live/tuodominio.it/fullchain.pem nginx/ssl/cert.pem
   cp /etc/letsencrypt/live/tuodominio.it/privkey.pem nginx/ssl/key.pem
   
   # Riavvia nginx
   docker-compose restart nginx
   ```

### Opzione B: PaaS (Più Semplice)

#### Backend su Render/Railway/Fly.io:

1. **Render** (Gratuito con limiti):
   - Connetti GitHub repository
   - Imposta variabili d'ambiente: `FMP_API_KEY`, `DEBUG=false`, `RELOAD=false`
   - Deploy automatico

2. **Railway** (Gratuito con limiti):
   - Deploy da GitHub
   - Configura env vars nel dashboard
   - Ottieni URL pubblico

3. **Fly.io** (Gratuito con limiti):
   ```bash
   flyctl auth login
   flyctl launch
   flyctl secrets set FMP_API_KEY=la_tua_api_key
   flyctl deploy
   ```

#### Frontend su Vercel/Netlify:

1. **Vercel**:
   - Connetti GitHub repository
   - Imposta `VITE_API_BASE_URL=https://api.tuodominio.it/api`
   - Deploy automatico

2. **Netlify**:
   - Deploy da GitHub
   - Build command: `npm run build`
   - Publish directory: `dist`
   - Environment variables: `VITE_API_BASE_URL`

## 🔒 Sicurezza

### Checklist Sicurezza:

- ✅ API key mai committate nel codice
- ✅ CORS configurato per domini specifici
- ✅ HTTPS abilitato ovunque
- ✅ Headers di sicurezza configurati
- ✅ Container eseguiti come utenti non-root
- ✅ Firewall configurato (solo porte 80, 443, 22)
- ✅ Certificati SSL validi
- ✅ Rate limiting (opzionale con Cloudflare)

### Configurazione Firewall:
```bash
# UFW
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable
```

## 📊 Monitoraggio

### Health Checks:
- Backend: `https://api.tuodominio.it/health`
- Frontend: Accesso diretto al sito

### Logs:
```bash
# Docker logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f nginx
```

## 🔄 Aggiornamenti

```bash
# Pull ultime modifiche
git pull origin main

# Rebuild e restart
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 🆘 Troubleshooting

### Problemi Comuni:

1. **CORS Error**: Verifica `CORS_ORIGINS` nel file `.env`
2. **API Key Invalid**: Controlla `FMP_API_KEY` nel backend
3. **SSL Certificate**: Rinnova con `certbot renew`
4. **Port Conflicts**: Cambia porte in `docker-compose.yml`

### Comandi Utili:
```bash
# Restart servizi
docker-compose restart

# View logs
docker-compose logs -f

# Check status
docker-compose ps

# Clean up
docker system prune -a
```

## 💰 Costi Stimati

### VPS (Opzione A):
- Server: €3-5/mese
- Dominio: €10-15/anno
- **Totale**: ~€50-70/anno

### PaaS (Opzione B):
- Render/Railway: Gratuito (con limiti)
- Vercel/Netlify: Gratuito (con limiti)
- Dominio: €10-15/anno
- **Totale**: ~€10-15/anno

## 📞 Supporto

Per problemi o domande:
1. Controlla i logs: `docker-compose logs`
2. Verifica configurazione: file `.env`
3. Testa endpoint: `curl https://api.tuodominio.it/health`
4. Controlla DNS: `nslookup app.tuodominio.it`
