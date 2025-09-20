#!/bin/bash

# Script per preparare il deploy su Render + Vercel
set -e

echo "🚀 Preparazione Deploy Render + Vercel"
echo "======================================"

# Colori
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Controlla se siamo nella directory giusta
if [ ! -f "backend/main.py" ] || [ ! -f "frontend/package.json" ]; then
    print_error "Esegui questo script dalla directory root del progetto (dove ci sono le cartelle backend e frontend)"
    exit 1
fi

print_status "Directory corretta ✓"

# Controlla se git è inizializzato
if [ ! -d ".git" ]; then
    print_warning "Git non inizializzato. Inizializzo..."
    git init
    print_status "Git inizializzato ✓"
fi

# Controlla file necessari
print_status "Controllo file necessari..."

required_files=(
    "backend/render.yaml"
    "frontend/vercel.json"
    "backend/env.example"
    "frontend/env.example"
    "DEPLOY_RENDER_VERCEL.md"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        print_error "File mancante: $file"
        exit 1
    fi
done

print_status "Tutti i file necessari presenti ✓"

# Controlla se ci sono modifiche non committate
if ! git diff --quiet; then
    print_warning "Ci sono modifiche non committate. Le aggiungo..."
    git add .
    git commit -m "Prepare for Render + Vercel deploy"
    print_status "Modifiche committate ✓"
fi

# Controlla se il remote origin è configurato
if ! git remote get-url origin > /dev/null 2>&1; then
    print_warning "Remote origin non configurato."
    echo
    echo "Per configurare GitHub:"
    echo "1. Crea un repository su GitHub"
    echo "2. Esegui: git remote add origin https://github.com/TUO_USERNAME/finge.git"
    echo "3. Esegui: git push -u origin main"
    echo
    read -p "Hai già creato il repository su GitHub? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Inserisci l'URL del repository GitHub: " repo_url
        git remote add origin "$repo_url"
        git branch -M main
        git push -u origin main
        print_status "Repository GitHub configurato ✓"
    else
        print_warning "Configura GitHub prima di continuare"
        exit 1
    fi
fi

print_status "Repository GitHub configurato ✓"

# Mostra informazioni per il deploy
echo
echo "🎯 PROSSIMI PASSI:"
echo "=================="
echo
echo "1. BACKEND (Render):"
echo "   - Vai su https://render.com"
echo "   - New Web Service → Connect GitHub"
echo "   - Seleziona il repository 'finge'"
echo "   - Configura:"
echo "     * Name: finge-backend"
echo "     * Environment: Python 3"
echo "     * Build Command: pip install -r requirements.txt"
echo "     * Start Command: python -m uvicorn main:app --host 0.0.0.0 --port \$PORT"
echo "   - Environment Variables:"
echo "     * FMP_API_KEY = PTFU50sPSAUQugvL9GcAmPAE787UfNBI"
echo "     * DEBUG = false"
echo "     * RELOAD = false"
echo "     * CORS_ORIGINS = https://finge.vercel.app"
echo
echo "2. FRONTEND (Vercel):"
echo "   - Vai su https://vercel.com"
echo "   - New Project → Import Git Repository"
echo "   - Seleziona 'finge'"
echo "   - Configura:"
echo "     * Framework Preset: Vite"
echo "     * Root Directory: frontend"
echo "   - Environment Variables:"
echo "     * VITE_API_BASE_URL = [URL_BACKEND_RENDER]/api"
echo
echo "3. DOMINIO (Aruba):"
echo "   - Aggiungi CNAME: app → cname.vercel-dns.com"
echo "   - Aggiungi CNAME: api → [URL_BACKEND_RENDER]"
echo
echo "📖 Guida completa: DEPLOY_RENDER_VERCEL.md"
echo
print_status "Preparazione completata! 🎉"
