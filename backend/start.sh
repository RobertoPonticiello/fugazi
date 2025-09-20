#!/bin/bash

echo "🚀 Avvio Finge Backend Server"
echo "================================"

# Verifica che Python sia installato
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 non trovato. Installa Python3 prima di continuare."
    exit 1
fi

# Verifica che le dipendenze siano installate
if [ ! -d "venv" ] && [ ! -f "requirements.txt" ]; then
    echo "⚠️  Installa le dipendenze con: pip install -r requirements.txt"
fi

# Avvia il server
echo "📍 Avvio server su http://localhost:8000"
echo "🔑 API Key configurata automaticamente"
echo "🌐 Frontend supportato: http://localhost:8080"
echo ""
echo "Per fermare il server: Ctrl+C"
echo "================================"

python3 start_server.py
