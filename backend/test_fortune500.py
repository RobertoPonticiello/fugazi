#!/usr/bin/env python3
"""
Test del sistema di cache Fortune 500
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.fortune500_cache import Fortune500Cache, initialize_fortune500_cache

def test_cache_basic():
    """Test delle funzionalità base della cache"""
    print("🧪 Test Cache Fortune 500")
    print("=" * 50)
    
    # Inizializza la cache
    cache = initialize_fortune500_cache()
    
    # Test di ricerca
    test_companies = [
        "Apple",
        "Microsoft", 
        "Google",
        "Amazon",
        "Tesla",
        "NVIDIA",
        "Meta",
        "Azienda Inesistente"
    ]
    
    print("\n📋 Test ricerca nella cache:")
    for company in test_companies:
        result = cache.search_company(company)
        if result:
            print(f"✓ {company} -> {result.symbol} ({result.name})")
        else:
            print(f"✗ {company} -> Non trovata")
    
    # Statistiche
    stats = cache.get_cache_stats()
    print(f"\n📊 Statistiche cache:")
    print(f"   Totale aziende: {stats['total_companies']}")
    print(f"   Exchange: {stats['exchanges']}")
    print(f"   Settori: {len(stats['sectors'])}")
    
    return cache

def test_cache_management():
    """Test delle funzionalità di gestione della cache"""
    print("\n⚙️ Test Gestione Cache")
    print("=" * 50)
    
    cache = Fortune500Cache()
    
    # Test aggiunta azienda
    from modules.fortune500_cache import CachedCompany
    test_company = CachedCompany(
        symbol="TEST",
        name="Test Company Inc.",
        exchange="NASDAQ",
        sector="Technology"
    )
    
    cache.add_company(test_company)
    print("✓ Azienda di test aggiunta")
    
    # Verifica aggiunta
    found = cache.search_company("Test Company")
    if found:
        print(f"✓ Azienda trovata: {found.name} -> {found.symbol}")
    else:
        print("✗ Azienda non trovata dopo l'aggiunta")
    
    # Test ricerca per ticker
    found_by_symbol = cache.get_company_by_symbol("TEST")
    if found_by_symbol:
        print(f"✓ Ricerca per ticker: {found_by_symbol.name}")
    else:
        print("✗ Ricerca per ticker fallita")
    
    # Test statistiche
    stats = cache.get_cache_stats()
    print(f"📊 Statistiche: {stats['total_companies']} aziende")
    
    # Test svuotamento cache
    cache.clear_cache()
    print("✓ Cache svuotata")
    
    stats_after_clear = cache.get_cache_stats()
    print(f"📊 Dopo svuotamento: {stats_after_clear['total_companies']} aziende")

def main():
    """Funzione principale di test"""
    print("🚀 Test Sistema Cache Fortune 500")
    print("=" * 60)
    
    # Test 1: Funzionalità cache
    test_cache_basic()
    
    # Test 2: Gestione cache
    test_cache_management()
    
    print(f"\n🎉 Test completati!")
    print(f"\n💡 Per testare il sistema completo con API, imposta FMP_API_KEY")
    print(f"   export FMP_API_KEY='your_api_key_here'")

if __name__ == "__main__":
    main()
