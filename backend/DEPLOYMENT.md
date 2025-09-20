# Finge Backend - Guida al Deployment

## Stato Attuale

✅ **Backend FastAPI completamente funzionante** con tutti gli endpoint richiesti dal PRD.

## Endpoint Disponibili

### 1. GET /api/company/{ticker}
**Funziona**: ✅  
**Dati**: Ratios finanziari reali da Financial Modeling Prep API  
**Esempio**: `curl http://localhost:8000/api/company/AAPL`

### 2. GET /api/sector/{sector}  
**Funziona**: ✅  
**Dati**: Benchmark mock per Technology, Consumer Discretionary, Healthcare  
**Esempio**: `curl http://localhost:8000/api/sector/Technology`

### 3. GET /api/analysis/{ticker}
**Funziona**: ✅  
**Dati**: Analisi completa con scoring aggregato  
**Esempio**: `curl http://localhost:8000/api/analysis/AAPL`

### Endpoint di Test
- `GET /` - Root endpoint
- `GET /health` - Health check con validazione API key
- `GET /api/test/{ticker}` - Test dati disponibili per un ticker

## Configurazione

### Variabili d'Ambiente
```bash
export FMP_API_KEY="hITokCOYLN4BAlL3aVWgRovz9mqjYST7"
```

### Avvio Server
```bash
cd backend
pip install -r requirements.txt
python3 main.py
```

Server disponibile su: `http://localhost:8000`

## Architettura Implementata

### Moduli
- `modules/financial_ratios.py` - Calcolo ratios (integrato)
- `modules/get_tick.py` - Client FMP API (integrato)  
- `modules/sector_analysis.py` - Analisi settoriale (pronto per uso)
- `modules/scoring_system.py` - Sistema di scoring (funzionante)

### Sistema di Scoring
- **Pesi**: PE=50%, PB=30%, ROE=20%
- **Soglie**: ±20% per classificazione (Overvalued/Fair/Undervalued)
- **Output**: Score normalizzato [-1, 1] con segnale finale

## Dati di Test

### Aziende Supportate
- AAPL, MSFT, GOOGL, AMZN, META, NVDA, TSLA
- Nomi e settori mappati nel codice

### Settori con Benchmark
- Technology (PE: 25.2, PB: 10.1, ROE: 16.5%)
- Consumer Discretionary (PE: 22.8, PB: 8.5, ROE: 18.2%)
- Healthcare (PE: 18.5, PB: 6.2, ROE: 12.8%)

## Prossimi Passi

### Miglioramenti Immediati
1. **Endpoint Profilo Aziendale**: Implementare recupero nome/settore da API
2. **Benchmark Dinamici**: Attivare calcolo reale top 10 aziende per settore
3. **Market Cap**: Aggiungere recupero market cap reale

### Estensioni Future
1. **Cache Redis**: Implementare cache persistente
2. **Database**: Aggiungere MongoDB per persistenza
3. **Nuovi Indicatori**: Debt/Equity, margini, crescita
4. **API Rate Limiting**: Gestire limitazioni FMP

## Test di Funzionamento

```bash
# Test completo
curl http://localhost:8000/api/analysis/AAPL

# Output atteso:
{
  "ticker": "AAPL",
  "sector": "Technology", 
  "fundamentals": {"PE": 37.29, "PB": 61.37, "ROE": null},
  "benchmark": {"PE": 25.2, "PB": 10.1, "ROE": 16.5},
  "indicators": {"PE": "Overvalued", "PB": "Overvalued", "ROE": "N/A"},
  "score": -0.8,
  "final_signal": "Overvalued"
}
```

## Compatibilità Frontend

Il backend è pronto per l'integrazione con il frontend React esistente. Tutti gli endpoint seguono esattamente le specifiche del PRD.
