#!/bin/bash

# Script di deploy per Finge
# Uso: ./deploy.sh [vps|paas]

set -e

echo "🚀 Finge Deploy Script"
echo "======================"

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Funzione per stampare messaggi colorati
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Controlla se Docker è installato
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker non è installato. Installa Docker prima di continuare."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose non è installato. Installa Docker Compose prima di continuare."
        exit 1
    fi
    
    print_status "Docker e Docker Compose sono installati ✓"
}

# Controlla file di configurazione
check_config() {
    if [ ! -f ".env" ]; then
        print_warning "File .env non trovato. Creo da env.example..."
        cp env.example .env
        print_warning "Modifica il file .env con i tuoi valori prima di continuare!"
        exit 1
    fi
    
    if [ ! -f "backend/.env" ]; then
        print_warning "File backend/.env non trovato. Creo da env.example..."
        cp backend/env.example backend/.env
        print_warning "Modifica il file backend/.env con i tuoi valori prima di continuare!"
        exit 1
    fi
    
    if [ ! -f "frontend/.env" ]; then
        print_warning "File frontend/.env non trovato. Creo da env.example..."
        cp frontend/env.example frontend/.env
        print_warning "Modifica il file frontend/.env con i tuoi valori prima di continuare!"
        exit 1
    fi
    
    print_status "File di configurazione trovati ✓"
}

# Deploy VPS
deploy_vps() {
    print_status "Iniziando deploy VPS..."
    
    check_docker
    check_config
    
    # Crea directory SSL se non esiste
    mkdir -p nginx/ssl
    
    # Controlla se i certificati SSL esistono
    if [ ! -f "nginx/ssl/cert.pem" ] || [ ! -f "nginx/ssl/key.pem" ]; then
        print_warning "Certificati SSL non trovati in nginx/ssl/"
        print_warning "Genera certificati SSL con Let's Encrypt o usa certificati self-signed per test"
        print_warning "Per test, puoi generare certificati self-signed con:"
        echo "openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout nginx/ssl/key.pem -out nginx/ssl/cert.pem"
        read -p "Vuoi continuare senza SSL? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    
    # Build e avvia i container
    print_status "Building e avviando container..."
    docker-compose down
    docker-compose build --no-cache
    docker-compose up -d
    
    # Attendi che i servizi siano pronti
    print_status "Attendo che i servizi siano pronti..."
    sleep 10
    
    # Test health check
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        print_status "Backend è online ✓"
    else
        print_error "Backend non risponde. Controlla i logs: docker-compose logs backend"
    fi
    
    if curl -f http://localhost > /dev/null 2>&1; then
        print_status "Frontend è online ✓"
    else
        print_error "Frontend non risponde. Controlla i logs: docker-compose logs frontend"
    fi
    
    print_status "Deploy VPS completato!"
    print_status "Frontend: http://localhost (o il tuo dominio)"
    print_status "Backend: http://localhost:8000"
    print_status "Health check: http://localhost:8000/health"
}

# Deploy PaaS
deploy_paas() {
    print_status "Deploy PaaS - Istruzioni:"
    echo
    echo "1. BACKEND (Render/Railway/Fly.io):"
    echo "   - Connetti il repository GitHub"
    echo "   - Imposta variabili d'ambiente:"
    echo "     FMP_API_KEY=la_tua_api_key"
    echo "     DEBUG=false"
    echo "     RELOAD=false"
    echo "     CORS_ORIGINS=https://app.tuodominio.it"
    echo
    echo "2. FRONTEND (Vercel/Netlify):"
    echo "   - Connetti il repository GitHub"
    echo "   - Imposta variabili d'ambiente:"
    echo "     VITE_API_BASE_URL=https://api.tuodominio.it/api"
    echo
    echo "3. DNS (Pannello Aruba):"
    echo "   - A record: app.tuodominio.it -> IP_SERVER"
    echo "   - A record: api.tuodominio.it -> IP_SERVER"
    echo
    print_status "Consulta DEPLOY.md per istruzioni dettagliate"
}

# Main
case "${1:-vps}" in
    "vps")
        deploy_vps
        ;;
    "paas")
        deploy_paas
        ;;
    *)
        echo "Uso: $0 [vps|paas]"
        echo "  vps  - Deploy su VPS con Docker (default)"
        echo "  paas - Istruzioni per deploy PaaS"
        exit 1
        ;;
esac
