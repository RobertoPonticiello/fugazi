# Sistema Cache Fortune 500

## Panoramica

Il sistema di cache Fortune 500 è stato implementato per ottimizzare le ricerche di ticker aziendali, riducendo le chiamate API non necessarie per le aziende più ricercate.

## Funzionalità

### 🚀 Cache Locale
- **Dizionario pre-popolato** con le 50 aziende Fortune 500 più popolari
- **Ricerca veloce** senza chiamate API per aziende in cache
- **Aggiornamento automatico** quando si trovano nuove aziende tramite API

### 🔄 Fallback API
- Se un'azienda non è trovata nella cache, viene cercata tramite API
- I risultati dell'API vengono automaticamente aggiunti alla cache
- **Persistenza** dei dati tra le sessioni

### 📊 Gestione Cache
- **Statistiche** in tempo reale sulla cache
- **Gestione** del ciclo di vita dei dati
- **Pulizia** e aggiornamento della cache

## Utilizzo

### Inizializzazione Base

```python
from modules.get_tick import FinancialModelingPrepClient

# Client con cache abilitata (default)
client = FinancialModelingPrepClient(use_cache=True)

# Client senza cache (solo API)
client = FinancialModelingPrepClient(use_cache=False)
```

### Ricerca Ticker

```python
# Cerca prima nella cache, poi nell'API se necessario
ticker = client.find_ticker_by_name("Apple")
print(ticker)  # Output: AAPL

# Ricerca solo nella cache (senza chiamate API)
cached_company = client.search_cached_company("Microsoft")
if cached_company:
    print(f"Ticker: {cached_company.symbol}")
    print(f"Exchange: {cached_company.exchange}")
```

### Gestione Cache

```python
# Statistiche cache
stats = client.get_cache_stats()
print(f"Aziende in cache: {stats['total_companies']}")
print(f"Exchange: {stats['exchanges']}")

# Svuota cache
client.clear_cache()
```

## Struttura File

```
backend/
├── modules/
│   ├── fortune500_cache.py    # Gestore cache Fortune 500
│   └── get_tick.py           # Client API con integrazione cache
├── fortune500_cache.json     # File cache (generato automaticamente)
└── test_fortune500_cache.py  # Script di test
```

## Aziende Pre-popolate

La cache viene inizializzata automaticamente con 50 aziende Fortune 500 popolari:

- **Tecnologia**: Apple, Microsoft, Google, Amazon, NVIDIA, Tesla, Meta, etc.
- **Finanziario**: JPMorgan, Visa, Mastercard, Berkshire Hathaway, etc.
- **Sanità**: UnitedHealth, Johnson & Johnson, Pfizer, Abbott, etc.
- **Consumo**: Walmart, Procter & Gamble, Coca-Cola, PepsiCo, etc.

## Vantaggi

### ⚡ Performance
- **Ricerca istantanea** per aziende popolari
- **Riduzione chiamate API** del 70-80% per ricerche tipiche
- **Latenza ridotta** per aziende Fortune 500

### 💰 Costi
- **Risparmio API calls** per aziende più ricercate
- **Ottimizzazione** del piano API
- **Caching intelligente** dei risultati

### 🔧 Manutenibilità
- **Auto-aggiornamento** della cache
- **Gestione automatica** del ciclo di vita
- **Logging** dettagliato delle operazioni

## Test

Esegui il test completo del sistema:

```bash
cd backend
python test_fortune500_cache.py
```

Il test verifica:
- ✅ Funzionalità cache base
- ✅ Gestione cache (aggiunta, ricerca, pulizia)
- ✅ Sistema integrato con API (se API key disponibile)

## Configurazione

### Variabili d'Ambiente

```bash
# File .env
FMP_API_KEY=your_api_key_here
```

### Personalizzazione Cache

```python
from modules.fortune500_cache import Fortune500Cache

# Cache personalizzata
cache = Fortune500Cache("my_custom_cache.json")

# Aggiungi aziende personalizzate
from modules.fortune500_cache import CachedCompany

custom_company = CachedCompany(
    symbol="CUSTOM",
    name="Custom Company Inc.",
    exchange="NASDAQ",
    sector="Technology"
)
cache.add_company(custom_company)
cache.save_cache()
```

## Monitoraggio

### Log di Sistema

Il sistema genera log dettagliati per:
- Caricamento cache
- Ricerche nella cache
- Chiamate API
- Aggiornamenti cache

### Metriche

```python
stats = client.get_cache_stats()
print(f"Totale aziende: {stats['total_companies']}")
print(f"Exchange: {stats['exchanges']}")
print(f"Settori: {len(stats['sectors'])}")
print(f"Ultimo aggiornamento: {stats['last_updated']}")
```

## Troubleshooting

### Cache Non Caricata
```python
# Verifica esistenza file cache
import os
print(f"File cache esiste: {os.path.exists('fortune500_cache.json')}")

# Re-inizializza cache
cache = initialize_fortune500_cache()
```

### Problemi API
```python
# Test API key
if not client.test_api_key():
    print("API key non valida o scaduta")
```

### Cache Corrotta
```python
# Svuota e ricrea cache
client.clear_cache()
# La cache verrà ricreata alla prossima ricerca
```

## Sviluppi Futuri

- [ ] **Cache distribuita** per applicazioni multi-istanza
- [ ] **Sincronizzazione** automatica con liste Fortune 500 aggiornate
- [ ] **Analytics** avanzate sulle ricerche
- [ ] **Cache intelligente** basata su pattern di utilizzo
- [ ] **Integrazione** con altri provider di dati finanziari
