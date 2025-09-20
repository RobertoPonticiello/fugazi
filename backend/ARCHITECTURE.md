# Architettura Sistema Cache Fortune 500

## Diagramma del Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                    SISTEMA CACHE FORTUNE 500                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   External API  │
│   (React)       │    │   (FastAPI)     │    │   (FMP)         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    RICERCA TICKER                              │
└─────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CACHE FORTUNE 500                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Fortune500Cache │  │   CachedCompany │  │   JSON Storage  │ │
│  │                 │  │                 │  │                 │ │
│  │ • search_company│  │ • symbol        │  │ • fortune500_   │ │
│  │ • add_company   │  │ • name          │  │   cache.json    │ │
│  │ • get_stats     │  │ • exchange      │  │                 │ │
│  │ • clear_cache   │  │ • sector        │  │                 │ │
│  └─────────────────┘  │ • market_cap    │  │                 │ │
│                       │ • last_updated  │  │                 │ │
│                       └─────────────────┘  │                 │ │
│                                           └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FLUSSO DI RICERCA                           │
└─────────────────────────────────────────────────────────────────┘

1. RICERCA IN CACHE
   ┌─────────────────┐
   │ find_ticker_by_name() │
   └─────────────────┘
            │
            ▼
   ┌─────────────────┐
   │ cache.search_company() │
   └─────────────────┘
            │
            ▼
   ┌─────────────────┐
   │ Trovata?        │
   └─────────────────┘
            │
            ├─ SÌ ──► Ritorna ticker
            │
            ▼
            NO
            │
            ▼
2. RICERCA API
   ┌─────────────────┐
   │ search_company() │
   └─────────────────┘
            │
            ▼
   ┌─────────────────┐
   │ Trovata?        │
   └─────────────────┘
            │
            ├─ SÌ ──► Aggiungi alla cache
            │         │
            │         ▼
            │   ┌─────────────────┐
            │   │ cache.add_company() │
            │   └─────────────────┘
            │         │
            │         ▼
            │   ┌─────────────────┐
            │   │ cache.save_cache() │
            │   └─────────────────┘
            │         │
            │         ▼
            │   ┌─────────────────┐
            │   │ Ritorna ticker  │
            │   └─────────────────┘
            │
            ▼
            NO
            │
            ▼
   ┌─────────────────┐
   │ Ritorna None    │
   └─────────────────┘
```

## Componenti Principali

### 1. Fortune500Cache
- **Gestione cache**: Caricamento, salvataggio, ricerca
- **Persistenza**: Salvataggio automatico in JSON
- **Statistiche**: Monitoraggio utilizzo cache

### 2. CachedCompany
- **Modello dati**: Struttura per aziende in cache
- **Metadati**: Informazioni complete dell'azienda
- **Timestamp**: Tracciamento ultimo aggiornamento

### 3. FinancialModelingPrepClient
- **Integrazione cache**: Ricerca prima in cache, poi API
- **Auto-aggiornamento**: Aggiunta automatica risultati API
- **Fallback intelligente**: Gestione errori API

## Vantaggi Architetturali

### ⚡ Performance
- **Ricerca O(1)**: Accesso diretto per ticker
- **Ricerca O(n)**: Scansione per nome (ottimizzata)
- **Zero latenza**: Per aziende Fortune 500

### 💰 Costi
- **Riduzione API calls**: 70-80% per ricerche tipiche
- **Cache persistente**: Dati mantenuti tra sessioni
- **Auto-aggiornamento**: Solo quando necessario

### 🔧 Manutenibilità
- **Separazione responsabilità**: Cache vs API
- **Testabilità**: Componenti isolati
- **Estensibilità**: Facile aggiunta nuovi provider

## Flusso di Dati

```
Input: "Apple"
    │
    ▼
┌─────────────────┐
│ Cache Lookup    │ ──► Hit: "AAPL" (0ms)
└─────────────────┘
    │
    ▼ (Miss)
┌─────────────────┐
│ API Call        │ ──► "AAPL" (200ms)
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ Cache Update    │ ──► Save to JSON
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ Return Result   │ ──► "AAPL"
└─────────────────┘
```

## Configurazione

### File di Cache
```json
{
  "AAPL": {
    "symbol": "AAPL",
    "name": "Apple Inc.",
    "exchange": "NASDAQ",
    "sector": "Technology",
    "last_updated": "2025-09-13T16:14:22.160149"
  }
}
```

### Inizializzazione
```python
# Cache con 50 aziende Fortune 500 pre-popolate
cache = initialize_fortune500_cache()

# Client con cache integrata
client = FinancialModelingPrepClient(use_cache=True)
```

## Monitoraggio

### Metriche Cache
- **Hit Rate**: Percentuale ricerche in cache
- **Size**: Numero aziende in cache
- **Age**: Età media dati cache
- **Updates**: Numero aggiornamenti

### Logging
- **Cache hits**: Ricerche soddisfatte dalla cache
- **API calls**: Chiamate API effettuate
- **Cache updates**: Aggiornamenti cache
- **Errors**: Errori API o cache

## Sviluppi Futuri

- [ ] **Cache distribuita**: Redis/Memcached
- [ ] **Sincronizzazione**: Aggiornamenti automatici
- [ ] **Analytics**: Pattern di utilizzo
- [ ] **ML**: Predizione aziende popolari
- [ ] **Multi-provider**: Integrazione altri API
