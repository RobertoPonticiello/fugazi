#!/usr/bin/env python3
"""
Financial Modeling Prep API Client
Scopo: Effettuare chiamate API a Financial Modeling Prep per trovare il ticker
di un'azienda basandosi sul nome dell'azienda.
"""

import requests
import json
import os
from typing import Optional, Dict, List
from dataclasses import dataclass
from dotenv import load_dotenv
from .fortune500_cache import Fortune500Cache, CachedCompany, initialize_fortune500_cache

# Carica le variabili d'ambiente dal file .env
load_dotenv()


@dataclass
class CompanyInfo:
    """Classe per rappresentare le informazioni di un'azienda"""
    symbol: str
    name: str
    exchange: str
    market_cap: Optional[float] = None
    sector: Optional[str] = None
    industry: Optional[str] = None


class FinancialModelingPrepClient:
    """Client per interagire con l'API di Financial Modeling Prep"""
    
    def __init__(self, api_key: Optional[str] = None, use_cache: bool = True):
        """
        Inizializza il client con la chiave API
        
        Args:
            api_key: Chiave API di Financial Modeling Prep. Se non fornita,
                     cerca di recuperarla dalla variabile d'ambiente FMP_API_KEY
            use_cache: Se True, utilizza la cache Fortune 500 per evitare chiamate API
        """
        self.api_key = api_key or os.getenv('FMP_API_KEY')
        if not self.api_key:
            raise ValueError(
                "API key non trovata. Forniscila come parametro o imposta la "
                "variabile d'ambiente FMP_API_KEY"
            )
        
        self.base_url = "https://financialmodelingprep.com/api/v3"
        self.session = requests.Session()
        self.session.params = {'apikey': self.api_key}
        
        # Inizializza la cache Fortune 500
        self.use_cache = use_cache
        self.cache = initialize_fortune500_cache() if use_cache else None
    
    def test_api_key(self) -> bool:
        """
        Testa se l'API key è valida facendo una chiamata semplice
        
        Returns:
            True se l'API key è valida, False altrimenti
        """
        try:
            # Prova con l'endpoint /stable/search-name che sappiamo funzionare
            endpoint = "https://financialmodelingprep.com/stable/search-name"
            params = {
                'query': 'AAPL',
                'apikey': self.api_key
            }
            response = self.session.get(endpoint, params=params)
            
            if response.status_code == 200:
                print("✓ API key valida")
                return True
            elif response.status_code == 403:
                print("✗ API key non valida o scaduta")
                return False
            else:
                print(f"✗ Errore API: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"✗ Errore nel test API key: {e}")
            return False
    
    def search_company(self, company_name: str, limit: int = 10, exchange_filter: str = None) -> List[CompanyInfo]:
        """
        Cerca un'azienda per nome e restituisce una lista di possibili match
        
        Args:
            company_name: Nome dell'azienda da cercare
            limit: Numero massimo di risultati da restituire
            exchange_filter: Filtro per exchange specifico (es. 'NASDAQ', 'NYSE', 'AMEX')
            
        Returns:
            Lista di oggetti CompanyInfo con i risultati della ricerca
            
        Raises:
            requests.RequestException: In caso di errore nella chiamata API
        """
        # Usa l'endpoint /stable/search-name che funziona con la tua API key
        endpoint = f"https://financialmodelingprep.com/stable/search-name"
        params = {
            'query': company_name,
            'apikey': self.api_key
        }
        
        try:
            response = self.session.get(endpoint, params=params)
            
            if response.status_code == 403:
                print("Errore 403: Accesso negato. Possibili cause:")
                print("1. API key non valida o scaduta")
                print("2. Piano gratuito con limitazioni")
                print("3. Endpoint non disponibile per il tuo piano")
                print(f"URL tentato: {response.url}")
                return []
            
            response.raise_for_status()
            
            data = response.json()
            
            companies = []
            for item in data:
                # Applica il filtro per exchange se specificato
                if exchange_filter and item.get('exchange', '').upper() != exchange_filter.upper():
                    continue
                
                company = CompanyInfo(
                    symbol=item.get('symbol', ''),
                    name=item.get('name', ''),
                    exchange=item.get('exchange', ''),
                    market_cap=item.get('marketCap'),
                    sector=item.get('sector'),
                    industry=item.get('industry')
                )
                companies.append(company)
                
                # Limita i risultati dopo aver applicato il filtro
                if len(companies) >= limit:
                    break
            
            return companies
            
        except requests.exceptions.RequestException as e:
            print(f"Errore nella chiamata API: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Status Code: {e.response.status_code}")
                print(f"Response: {e.response.text}")
            return []
    
    def get_company_profile(self, symbol: str) -> Optional[Dict]:
        """
        Ottiene il profilo completo di un'azienda tramite il suo ticker
        
        Args:
            symbol: Ticker symbol dell'azienda
            
        Returns:
            Dizionario con i dati del profilo aziendale o None se non trovato
        """
        # Usa l'endpoint /stable/company-profile che sappiamo funzionare
        endpoint = f"https://financialmodelingprep.com/stable/company-profile/{symbol}"
        params = {'apikey': self.api_key}
        
        try:
            response = self.session.get(endpoint, params=params)
            
            if response.status_code == 403:
                print(f"Errore 403 per {symbol}: API key non valida per questo endpoint")
                return None
            elif response.status_code == 404:
                print(f"Profilo non trovato per {symbol}")
                return None
            
            response.raise_for_status()
            
            data = response.json()
            return data[0] if data else None
            
        except requests.exceptions.RequestException as e:
            print(f"Errore nel recupero del profilo per {symbol}: {e}")
            return None
    
    def search_nasdaq_company(self, company_name: str, limit: int = 10) -> List[CompanyInfo]:
        """
        Cerca un'azienda per nome limitando i risultati solo a NASDAQ
        
        Args:
            company_name: Nome dell'azienda da cercare
            limit: Numero massimo di risultati da restituire
            
        Returns:
            Lista di oggetti CompanyInfo con i risultati della ricerca (solo NASDAQ)
        """
        return self.search_company(company_name, limit, exchange_filter='NASDAQ')
    
    def find_ticker_by_name(self, company_name: str, nasdaq_only: bool = False) -> Optional[str]:
        """
        Trova il ticker di un'azienda basandosi sul nome.
        Prima cerca nella cache Fortune 500, poi nell'API se necessario.
        
        Args:
            company_name: Nome dell'azienda da cercare
            nasdaq_only: Se True, cerca solo aziende quotate su NASDAQ
            
        Returns:
            Ticker symbol dell'azienda o None se non trovato
        """
        # Prima cerca nella cache Fortune 500
        if self.use_cache and self.cache:
            cached_company = self.cache.search_company(company_name)
            if cached_company:
                print(f"✓ Trovata nella cache Fortune 500: {cached_company.name} -> {cached_company.symbol}")
                return cached_company.symbol
        
        # Se non trovata nella cache, cerca tramite API
        print(f"Ricerca tramite API per: {company_name}")
        if nasdaq_only:
            companies = self.search_nasdaq_company(company_name, limit=5)
        else:
            companies = self.search_company(company_name, limit=5)
        
        if not companies:
            return None
        
        # Restituisce il primo risultato (più probabile match)
        best_match = companies[0]
        
        # Aggiungi il risultato alla cache per future ricerche
        if self.use_cache and self.cache:
            cached_company = CachedCompany(
                symbol=best_match.symbol,
                name=best_match.name,
                exchange=best_match.exchange,
                market_cap=best_match.market_cap,
                sector=best_match.sector,
                industry=best_match.industry
            )
            self.cache.add_company(cached_company)
            self.cache.save_cache()
            print(f"✓ Aggiunta alla cache: {best_match.name} -> {best_match.symbol}")
        
        return best_match.symbol
    
    def get_cache_stats(self) -> Optional[Dict]:
        """
        Ottiene statistiche sulla cache Fortune 500
        
        Returns:
            Dizionario con statistiche della cache o None se la cache non è abilitata
        """
        if self.use_cache and self.cache:
            return self.cache.get_cache_stats()
        return None
    
    def clear_cache(self) -> None:
        """Svuota la cache Fortune 500"""
        if self.use_cache and self.cache:
            self.cache.clear_cache()
            print("Cache Fortune 500 svuotata")
    
    def search_cached_company(self, company_name: str) -> Optional[CachedCompany]:
        """
        Cerca un'azienda solo nella cache Fortune 500 (senza chiamate API)
        
        Args:
            company_name: Nome dell'azienda da cercare
            
        Returns:
            CachedCompany se trovata nella cache, None altrimenti
        """
        if self.use_cache and self.cache:
            return self.cache.search_company(company_name)
        return None


def main():
    """Funzione principale per testare il client con cache Fortune 500"""
    try:
        # Inizializza il client con cache abilitata
        client = FinancialModelingPrepClient(use_cache=True)
        
        # Mostra statistiche cache
        stats = client.get_cache_stats()
        if stats:
            print("📊 Statistiche Cache Fortune 500:")
            print(f"   Aziende in cache: {stats['total_companies']}")
            print(f"   Exchange: {list(stats['exchanges'].keys())}")
            print(f"   Settori: {len(stats['sectors'])}")
            print()
        
        # Testa l'API key prima di procedere
        print("🔑 Test API key...")
        if not client.test_api_key():
            print("\nRisoluzione problemi:")
            print("1. Verifica che la tua API key sia corretta")
            print("2. Controlla che non sia scaduta")
            print("3. Verifica il piano di abbonamento su https://financialmodelingprep.com/")
            print("4. Alcuni endpoint potrebbero non essere disponibili nel piano gratuito")
            return
        
        # Test con aziende popolari (dovrebbero essere nella cache)
        print("\n🧪 Test con aziende Fortune 500 popolari:")
        test_companies = ["Apple", "Microsoft", "Google", "Amazon", "Tesla"]
        
        for company in test_companies:
            print(f"\nRicerca: {company}")
            ticker = client.find_ticker_by_name(company)
            if ticker:
                print(f"   ✓ Ticker trovato: {ticker}")
            else:
                print(f"   ✗ Ticker non trovato")
        
        # Test con azienda non in cache
        print(f"\n🔍 Test con azienda non in cache:")
        company_name = input("Inserisci il nome di un'azienda (o premi Enter per 'NVIDIA'): ").strip()
        if not company_name:
            company_name = "NVIDIA"
        
        print(f"\nRicerca di '{company_name}'...")
        ticker = client.find_ticker_by_name(company_name)
        
        if ticker:
            print(f"✓ Ticker trovato: {ticker}")
            
            # Mostra informazioni dettagliate se disponibili
            cached_company = client.search_cached_company(company_name)
            if cached_company:
                print(f"   Nome completo: {cached_company.name}")
                print(f"   Exchange: {cached_company.exchange}")
                if cached_company.sector:
                    print(f"   Settore: {cached_company.sector}")
        else:
            print(f"✗ Ticker non trovato per '{company_name}'")
        
        # Mostra statistiche aggiornate
        stats = client.get_cache_stats()
        if stats:
            print(f"\n📊 Statistiche Cache aggiornate:")
            print(f"   Aziende in cache: {stats['total_companies']}")
    
    except ValueError as e:
        print(f"Errore di configurazione: {e}")
        print("\nPer utilizzare questo script, devi:")
        print("1. Ottenere una API key da https://financialmodelingprep.com/")
        print("2. Creare un file .env con FMP_API_KEY=your_api_key_here")
        print("3. Oppure impostare la variabile d'ambiente FMP_API_KEY")
        print("   Esempio: export FMP_API_KEY='your_api_key_here'")
    
    except Exception as e:
        print(f"Errore inaspettato: {e}")


if __name__ == "__main__":
    main()
