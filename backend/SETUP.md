# Finge Backend - Setup e Configurazione

## Configurazione API Key

### Opzione 1: File di Configurazione (Raccomandato)
L'API key è già configurata nel file `config.py`:
```python
FMP_API_KEY = "hITokCOYLN4BAlL3aVWgRovz9mqjYST7"
```

### Opzione 2: Variabile d'Ambiente
Se preferisci usare una variabile d'ambiente:
```bash
export FMP_API_KEY="hITokCOYLN4BAlL3aVWgRovz9mqjYST7"
```

### Opzione 3: File .env
Crea un file `.env` nella directory backend:
```bash
# Copia il file di esempio
cp env.example .env

# Modifica il file .env con la tua API key
nano .env
```

Contenuto del file `.env`:
```
FMP_API_KEY=hITokCOYLN4BAlL3aVWgRovz9mqjYST7
HOST=0.0.0.0
PORT=8000
DEBUG=True
RELOAD=True
```

## Avvio del Backend

### ⭐ Metodo Raccomandato: Script di Avvio
```bash
cd backend
./start.sh
```

### Metodo Alternativo: Script Python
```bash
cd backend
python3 start_server.py
```

### Metodo Manuale: Main.py
```bash
cd backend
python3 main.py
```

⚠️ **Nota**: Se usi `python3 main.py` direttamente in Cursor, potresti vedere doppi avvii. Usa `start_server.py` o `start.sh` per evitare questo problema.

## Verifica Configurazione

Testa che tutto funzioni:
```bash
curl http://localhost:8000/health
```

Dovresti vedere:
```json
{
  "status": "healthy",
  "api_key_valid": true
}
```

## Configurazione CORS

Il backend è configurato per accettare richieste da:
- `http://localhost:3000` (React default)
- `http://localhost:5173` (Vite default)
- `http://localhost:8080` (Porta alternativa)

Per aggiungere altre origini, modifica il file `config.py`:
```python
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8080",
    "http://tuodominio.com"  # Aggiungi qui
]
```

## Troubleshooting

### Errore "API key non valida"
1. Verifica che l'API key sia corretta
2. Controlla che non ci siano spazi extra
3. Testa l'API key direttamente:
   ```bash
   curl "https://financialmodelingprep.com/stable/ratios?symbol=AAPL&period=annual&apikey=TUO_API_KEY"
   ```

### Errore CORS
1. Verifica che l'URL del frontend sia nelle CORS_ORIGINS
2. Controlla che il frontend sia in esecuzione sulla porta corretta

### Errore "Port already in use"
1. Cambia la porta nel file `config.py`:
   ```python
   PORT = 8001  # Usa una porta diversa
   ```
2. Oppure ferma il processo che usa la porta 8000:
   ```bash
   sudo lsof -ti:8000 | xargs kill -9
   ```
