# 🚀 Finge - Quick Start Guide

## ✅ Configurazione Completata

### Backend (FastAPI)
- ✅ Server attivo su `http://localhost:8000`
- ✅ API key configurata in `config.py`
- ✅ Tutti gli endpoint funzionanti
- ✅ CORS configurato per frontend

### Frontend (React + Vite)
- ✅ Server attivo su `http://localhost:8080`
- ✅ Integrazione backend completata
- ✅ Indicatori di stato implementati

## 🎯 Come Avviare l'Applicazione

### 1. Avvia il Backend
```bash
cd backend
python3 start_server.py
```
**Oppure** (metodo alternativo):
```bash
cd backend
./start.sh
```

### 2. Avvia il Frontend
```bash
cd frontend
npm run dev
```

### 3. Apri l'Applicazione
Vai su: `http://localhost:8080`

## 🧪 Test dell'Applicazione

1. **Verifica connessione**: L'indicatore in alto a destra dovrebbe essere verde "Backend Connected"

2. **Testa l'analisi**:
   - Inserisci un ticker: `AAPL`, `MSFT`, `GOOGL`, `NVDA`, `META`
   - Clicca "Analyze"
   - Vedi i risultati con dati reali

## 📊 Dati Disponibili

### Aziende Supportate
- **AAPL** - Apple Inc. (Technology)
- **MSFT** - Microsoft Corporation (Technology)
- **GOOGL** - Alphabet Inc. (Technology)
- **NVDA** - NVIDIA Corporation (Technology)
- **META** - Meta Platforms Inc. (Technology)
- **AMZN** - Amazon.com Inc. (Consumer Discretionary)
- **TSLA** - Tesla Inc. (Consumer Discretionary)

### Esempio di Output
```json
{
  "ticker": "AAPL",
  "sector": "Technology",
  "fundamentals": {
    "PE": 37.29,
    "PB": 61.37,
    "ROE": null
  },
  "benchmark": {
    "PE": 25.2,
    "PB": 10.1,
    "ROE": 16.5
  },
  "indicators": {
    "PE": "Overvalued",
    "PB": "Overvalued",
    "ROE": "N/A"
  },
  "score": -0.8,
  "final_signal": "Overvalued"
}
```

## 🔧 Troubleshooting

### Se il Backend non si avvia
```bash
cd backend
pkill -f "python3"
python3 start_server.py
```

### Se il Frontend non si avvia
```bash
cd frontend
npm install
npm run dev
```

### Se vedi errori Cursor/doppi avvii
Usa sempre `python3 start_server.py` invece di `python3 main.py`

## 📁 Struttura File

```
finge/
├── backend/
│   ├── config.py          # ✅ Configurazione API key
│   ├── start_server.py    # ✅ Script di avvio sicuro
│   ├── start.sh          # ✅ Script bash
│   ├── main.py           # ✅ Applicazione principale
│   └── modules/          # ✅ Moduli finanziari
└── frontend/
    ├── src/services/api.ts # ✅ Integrazione backend
    └── src/pages/Index.tsx # ✅ Interfaccia principale
```

## 🎉 Risultato Finale

L'applicazione Finge è ora completamente funzionante con:
- ✅ **Dati reali** da Financial Modeling Prep API
- ✅ **Scoring aggregato** con pesi PE=50%, PB=30%, ROE=20%
- ✅ **Benchmark dinamici** per settore
- ✅ **Interfaccia moderna** React + Tailwind
- ✅ **Gestione errori** robusta
- ✅ **Configurazione semplificata**

**L'applicazione è pronta per la demo!** 🚀
