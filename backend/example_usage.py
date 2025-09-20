#!/usr/bin/env python3
"""
Esempio di utilizzo del sistema di cache Fortune 500
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.get_tick import FinancialModelingPrepClient
from modules.fortune500_cache import Fortune500Cache

def example_without_api():
    """Esempio di utilizzo senza API key (solo cache)"""
    print("📚 Esempio: Utilizzo Cache Fortune 500 (Senza API)")
    print("=" * 60)
    
    # Inizializza solo la cache
    cache = Fortune500Cache()
    
    # Lista di aziende da cercare
    companies_to_search = [
        "Apple",
        "Microsoft", 
        "Google",
        "Amazon",
        "Tesla",
        "NVIDIA",
        "Meta",
        "Azienda Non Esistente"
    ]
    
    print("🔍 Ricerca aziende nella cache Fortune 500:")
    print("-" * 50)
    
    for company in companies_to_search:
        result = cache.search_company(company)
        if result:
            print(f"✅ {company:20} -> {result.symbol:6} ({result.name})")
        else:
            print(f"❌ {company:20} -> Non trovata")
    
    # Statistiche
    stats = cache.get_cache_stats()
    print(f"\n📊 Statistiche Cache:")
    print(f"   Aziende totali: {stats['total_companies']}")
    print(f"   Exchange: {list(stats['exchanges'].keys())}")
    print(f"   Settori: {len(stats['sectors'])}")

def example_with_api():
    """Esempio di utilizzo con API key (cache + API)"""
    print("\n📚 Esempio: Utilizzo Sistema Completo (Cache + API)")
    print("=" * 60)
    
    # Verifica se l'API key è disponibile
    api_key = os.getenv('FMP_API_KEY')
    if not api_key:
        print("⚠️ API key non trovata. Per testare il sistema completo:")
        print("   export FMP_API_KEY='your_api_key_here'")
        return
    
    try:
        # Inizializza il client con cache
        client = FinancialModelingPrepClient(use_cache=True)
        
        # Mostra statistiche iniziali
        stats = client.get_cache_stats()
        print(f"📊 Cache iniziale: {stats['total_companies']} aziende")
        
        # Test con aziende Fortune 500 (dovrebbero essere in cache)
        print(f"\n🧪 Test aziende Fortune 500:")
        fortune500_companies = ["Apple", "Microsoft", "Amazon", "Tesla"]
        
        for company in fortune500_companies:
            print(f"\nRicerca: {company}")
            ticker = client.find_ticker_by_name(company)
            if ticker:
                print(f"   ✅ Ticker: {ticker}")
            else:
                print(f"   ❌ Non trovato")
        
        # Test con azienda non in cache (richiederà API)
        print(f"\n🔍 Test azienda non in cache:")
        new_company = "NVIDIA"
        print(f"Ricerca: {new_company}")
        ticker = client.find_ticker_by_name(new_company)
        
        if ticker:
            print(f"   ✅ Ticker trovato: {ticker}")
            
            # Verifica che sia stata aggiunta alla cache
            cached = client.search_cached_company(new_company)
            if cached:
                print(f"   ✅ Aggiunta alla cache: {cached.name}")
        else:
            print(f"   ❌ Ticker non trovato")
        
        # Statistiche finali
        stats = client.get_cache_stats()
        print(f"\n📊 Cache finale: {stats['total_companies']} aziende")
        
    except Exception as e:
        print(f"❌ Errore: {e}")

def example_cache_management():
    """Esempio di gestione della cache"""
    print("\n📚 Esempio: Gestione Cache")
    print("=" * 60)
    
    cache = Fortune500Cache()
    
    # Aggiungi un'azienda personalizzata
    from modules.fortune500_cache import CachedCompany
    
    custom_company = CachedCompany(
        symbol="CUSTOM",
        name="Custom Company Inc.",
        exchange="NASDAQ",
        sector="Technology",
        market_cap=1000000000
    )
    
    print("➕ Aggiunta azienda personalizzata...")
    cache.add_company(custom_company)
    cache.save_cache()
    
    # Verifica aggiunta
    found = cache.search_company("Custom Company")
    if found:
        print(f"✅ Azienda trovata: {found.name} -> {found.symbol}")
        print(f"   Exchange: {found.exchange}")
        print(f"   Settore: {found.sector}")
        print(f"   Market Cap: ${found.market_cap:,}")
    
    # Ricerca per ticker
    found_by_ticker = cache.get_company_by_symbol("CUSTOM")
    if found_by_ticker:
        print(f"✅ Ricerca per ticker: {found_by_ticker.name}")
    
    # Statistiche aggiornate
    stats = cache.get_cache_stats()
    print(f"\n📊 Statistiche aggiornate: {stats['total_companies']} aziende")

def main():
    """Funzione principale"""
    print("🚀 Esempi di Utilizzo Sistema Cache Fortune 500")
    print("=" * 70)
    
    # Esempio 1: Solo cache
    example_without_api()
    
    # Esempio 2: Cache + API
    example_with_api()
    
    # Esempio 3: Gestione cache
    example_cache_management()
    
    print(f"\n🎉 Esempi completati!")
    print(f"\n💡 Per maggiori informazioni, consulta FORTUNE500_CACHE.md")

if __name__ == "__main__":
    main()
