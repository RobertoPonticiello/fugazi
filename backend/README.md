# Finge Backend

Backend FastAPI per il sistema di analisi finanziaria Finge.

## Caratteristiche

- **API RESTful** per analisi finanziaria
- **Scoring aggregato** con pesi configurabili
- **Benchmark dinamici** per settore
- **Cache intelligente** per ottimizzare le performance
- **Integrazione** con Financial Modeling Prep API

## Struttura

```
backend/
├── main.py                      # Applicazione FastAPI principale
├── modules/                     # Moduli dell'applicazione
│   ├── __init__.py
│   ├── financial_ratios.py      # Calcolo ratios finanziari
│   ├── get_tick.py             # Client per FMP API con cache Fortune 500
│   ├── fortune500_cache.py     # Gestore cache Fortune 500
│   ├── sector_analysis.py      # Analisi settoriale
│   └── scoring_system.py       # Sistema di scoring
├── fortune500_cache.json       # File cache Fortune 500 (auto-generato)
├── test_fortune500.py          # Test sistema cache
├── example_usage.py            # Esempi di utilizzo
├── FORTUNE500_CACHE.md         # Documentazione cache Fortune 500
├── requirements.txt            # Dipendenze Python
└── README.md
```

## Endpoint API

### 1. GET /api/company/{ticker}
Recupera dati fondamentali di una società.

**Esempio:**
```bash
curl http://localhost:8000/api/company/AAPL
```

### 2. GET /api/sector/{sector}
Calcola benchmark settoriale dinamico.

**Esempio:**
```bash
curl http://localhost:8000/api/sector/Technology
```

### 3. GET /api/analysis/{ticker}
Analisi completa con scoring aggregato.

**Esempio:**
```bash
curl http://localhost:8000/api/analysis/AAPL
```

## Setup

1. **Installa dipendenze:**
```bash
pip install -r requirements.txt
```

2. **Configura API key:**
```bash
export FMP_API_KEY="your_api_key_here"
```

3. **Avvia il server:**
```bash
python main.py
```

Il server sarà disponibile su `http://localhost:8000`

## Configurazione

### Pesi degli indicatori (scoring_system.py)
```python
weights = {
    "PE": 0.5,   # Price-to-Earnings: 50%
    "PB": 0.3,   # Price-to-Book: 30%
    "ROE": 0.2   # Return on Equity: 20%
}
```

### Soglie di classificazione
- **Overvalued**: >20% sopra la media settoriale
- **Fair**: ±20% dalla media settoriale  
- **Undervalued**: >20% sotto la media settoriale

## Cache

Il sistema utilizza cache intelligente per ottimizzare le performance:

### Cache Fortune 500
- **Dizionario locale** con le 50 aziende Fortune 500 più popolari
- **Ricerca veloce** senza chiamate API per aziende in cache
- **Auto-aggiornamento** quando si trovano nuove aziende tramite API
- **Persistenza** dei dati tra le sessioni

### Cache in-memory
- **Benchmark settoriali**: 24 ore
- **Profili aziendali**: gestiti dal client FMP

### Vantaggi
- ⚡ **Performance**: Ricerca istantanea per aziende popolari
- 💰 **Costi**: Riduzione chiamate API del 70-80%
- 🔧 **Manutenibilità**: Auto-aggiornamento della cache

## Test

### Test API
Testa l'API key:
```bash
curl http://localhost:8000/health
```

### Test Cache Fortune 500
Testa il sistema di cache:
```bash
# Test sistema cache
python3 test_fortune500.py

# Esempi di utilizzo
python3 example_usage.py
```

### Test Moduli
```bash
# Test client FMP con cache
python3 -m modules.get_tick

# Test cache standalone
python3 -m modules.fortune500_cache
```
