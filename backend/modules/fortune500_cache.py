#!/usr/bin/env python3
"""
Fortune 500 Cache Manager
Gestisce un dizionario locale con le aziende Fortune 500 per evitare chiamate API non necessarie.
Se un'azienda non viene trovata nel dizionario, viene cercata tramite API e aggiunta alla cache.
"""

import json
import os
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import logging

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class CachedCompany:
    """Classe per rappresentare un'azienda nella cache"""
    symbol: str
    name: str
    exchange: str
    market_cap: Optional[float] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    last_updated: str = None
    
    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.now().isoformat()


class Fortune500Cache:
    """Gestore della cache Fortune 500"""
    
    def __init__(self, cache_file: str = "fortune500_cache.json"):
        """
        Inizializza il gestore della cache
        
        Args:
            cache_file: Percorso del file di cache JSON
        """
        self.cache_file = cache_file
        self.cache: Dict[str, CachedCompany] = {}
        self.load_cache()
    
    def load_cache(self) -> None:
        """Carica la cache dal file JSON"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.cache = {
                        key: CachedCompany(**value) 
                        for key, value in data.items()
                    }
                logger.info(f"Cache caricata: {len(self.cache)} aziende")
            else:
                logger.info("File cache non trovato, inizializzazione cache vuota")
                self.cache = {}
        except Exception as e:
            logger.error(f"Errore nel caricamento della cache: {e}")
            self.cache = {}
    
    def save_cache(self) -> None:
        """Salva la cache nel file JSON"""
        try:
            # Crea la directory se non esiste (solo se il percorso ha una directory)
            cache_dir = os.path.dirname(self.cache_file)
            if cache_dir:
                os.makedirs(cache_dir, exist_ok=True)
            
            # Converte i dataclass in dizionari per la serializzazione JSON
            cache_data = {
                key: asdict(company) 
                for key, company in self.cache.items()
            }
            
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Cache salvata: {len(self.cache)} aziende")
        except Exception as e:
            logger.error(f"Errore nel salvataggio della cache: {e}")
    
    def search_company(self, company_name: str) -> Optional[CachedCompany]:
        """
        Cerca un'azienda nella cache per nome
        
        Args:
            company_name: Nome dell'azienda da cercare
            
        Returns:
            CachedCompany se trovata, None altrimenti
        """
        company_name_lower = company_name.lower().strip()
        
        # Cerca corrispondenze esatte
        for key, company in self.cache.items():
            if company.name.lower() == company_name_lower:
                return company
        
        # Cerca corrispondenze parziali (contiene)
        for key, company in self.cache.items():
            if company_name_lower in company.name.lower() or company.name.lower() in company_name_lower:
                return company
        
        # Cerca per ticker symbol
        if company_name_lower.upper() in self.cache:
            return self.cache[company_name_lower.upper()]
        
        return None
    
    def add_company(self, company: CachedCompany) -> None:
        """
        Aggiunge un'azienda alla cache
        
        Args:
            company: Oggetto CachedCompany da aggiungere
        """
        # Usa il ticker come chiave principale
        key = company.symbol.upper()
        self.cache[key] = company
        
        # Aggiungi anche una chiave per il nome per ricerche più veloci
        name_key = f"name_{company.name.lower().replace(' ', '_')}"
        self.cache[name_key] = company
        
        logger.info(f"Aggiunta alla cache: {company.name} ({company.symbol})")
    
    def get_company_by_symbol(self, symbol: str) -> Optional[CachedCompany]:
        """
        Ottiene un'azienda dalla cache tramite il ticker symbol
        
        Args:
            symbol: Ticker symbol dell'azienda
            
        Returns:
            CachedCompany se trovata, None altrimenti
        """
        return self.cache.get(symbol.upper())
    
    def is_cache_stale(self, max_age_days: int = 30) -> bool:
        """
        Verifica se la cache è obsoleta
        
        Args:
            max_age_days: Età massima della cache in giorni
            
        Returns:
            True se la cache è obsoleta, False altrimenti
        """
        if not self.cache:
            return True
        
        # Controlla l'ultima modifica del file
        try:
            file_mtime = os.path.getmtime(self.cache_file)
            file_age = datetime.now() - datetime.fromtimestamp(file_mtime)
            return file_age > timedelta(days=max_age_days)
        except:
            return True
    
    def get_cache_stats(self) -> Dict:
        """
        Ottiene statistiche sulla cache
        
        Returns:
            Dizionario con statistiche della cache
        """
        if not self.cache:
            return {"total_companies": 0, "exchanges": {}, "sectors": {}}
        
        exchanges = {}
        sectors = {}
        
        for company in self.cache.values():
            # Conta solo le aziende con ticker (non le chiavi per nome)
            if not company.symbol.startswith("name_"):
                exchanges[company.exchange] = exchanges.get(company.exchange, 0) + 1
                if company.sector:
                    sectors[company.sector] = sectors.get(company.sector, 0) + 1
        
        return {
            "total_companies": len([c for c in self.cache.values() if not c.symbol.startswith("name_")]),
            "exchanges": exchanges,
            "sectors": sectors,
            "last_updated": max([c.last_updated for c in self.cache.values()]) if self.cache else None
        }
    
    def clear_cache(self) -> None:
        """Svuota la cache"""
        self.cache = {}
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)
        logger.info("Cache svuotata")


def initialize_fortune500_cache() -> Fortune500Cache:
    """
    Inizializza la cache Fortune 500 con alcune aziende popolari
    
    Returns:
        Istanza di Fortune500Cache inizializzata
    """
    cache = Fortune500Cache()
    
    # Se la cache è vuota, aggiungi alcune aziende Fortune 500 popolari
    if not cache.cache:
        logger.info("Inizializzazione cache con aziende Fortune 500 popolari...")
        
        # Lista di aziende Fortune 500 popolari (top 50)
        popular_companies = [
            ("AAPL", "Apple Inc.", "NASDAQ", "Technology"),
            ("MSFT", "Microsoft Corporation", "NASDAQ", "Technology"),
            ("GOOGL", "Alphabet Inc. Class A", "NASDAQ", "Technology"),
            ("AMZN", "Amazon.com Inc.", "NASDAQ", "Consumer Discretionary"),
            ("NVDA", "NVIDIA Corporation", "NASDAQ", "Technology"),
            ("META", "Meta Platforms Inc.", "NASDAQ", "Technology"),
            ("TSLA", "Tesla Inc.", "NASDAQ", "Consumer Discretionary"),
            ("BRK.B", "Berkshire Hathaway Inc. Class B", "NYSE", "Financials"),
            ("UNH", "UnitedHealth Group Incorporated", "NYSE", "Health Care"),
            ("JNJ", "Johnson & Johnson", "NYSE", "Health Care"),
            ("JPM", "JPMorgan Chase & Co.", "NYSE", "Financials"),
            ("V", "Visa Inc.", "NYSE", "Financials"),
            ("PG", "Procter & Gamble Co.", "NYSE", "Consumer Staples"),
            ("HD", "Home Depot Inc.", "NYSE", "Consumer Discretionary"),
            ("MA", "Mastercard Incorporated", "NYSE", "Financials"),
            ("DIS", "Walt Disney Co.", "NYSE", "Communication Services"),
            ("PYPL", "PayPal Holdings Inc.", "NASDAQ", "Financials"),
            ("ADBE", "Adobe Inc.", "NASDAQ", "Technology"),
            ("CMCSA", "Comcast Corporation", "NASDAQ", "Communication Services"),
            ("NFLX", "Netflix Inc.", "NASDAQ", "Communication Services"),
            ("CRM", "Salesforce Inc.", "NYSE", "Technology"),
            ("INTC", "Intel Corporation", "NASDAQ", "Technology"),
            ("PFE", "Pfizer Inc.", "NYSE", "Health Care"),
            ("ABT", "Abbott Laboratories", "NYSE", "Health Care"),
            ("TMO", "Thermo Fisher Scientific Inc.", "NYSE", "Health Care"),
            ("ACN", "Accenture plc", "NYSE", "Technology"),
            ("COST", "Costco Wholesale Corporation", "NASDAQ", "Consumer Staples"),
            ("DHR", "Danaher Corporation", "NYSE", "Health Care"),
            ("VZ", "Verizon Communications Inc.", "NYSE", "Communication Services"),
            ("WMT", "Walmart Inc.", "NYSE", "Consumer Staples"),
            ("T", "AT&T Inc.", "NYSE", "Communication Services"),
            ("NKE", "Nike Inc.", "NYSE", "Consumer Discretionary"),
            ("ABBV", "AbbVie Inc.", "NYSE", "Health Care"),
            ("MRK", "Merck & Co. Inc.", "NYSE", "Health Care"),
            ("PEP", "PepsiCo Inc.", "NASDAQ", "Consumer Staples"),
            ("KO", "Coca-Cola Co.", "NYSE", "Consumer Staples"),
            ("AVGO", "Broadcom Inc.", "NASDAQ", "Technology"),
            ("TXN", "Texas Instruments Incorporated", "NASDAQ", "Technology"),
            ("QCOM", "QUALCOMM Incorporated", "NASDAQ", "Technology"),
            ("CSCO", "Cisco Systems Inc.", "NASDAQ", "Technology"),
            ("ORCL", "Oracle Corporation", "NYSE", "Technology"),
            ("IBM", "International Business Machines Corporation", "NYSE", "Technology"),
            ("AMD", "Advanced Micro Devices Inc.", "NASDAQ", "Technology"),
            ("AMAT", "Applied Materials Inc.", "NASDAQ", "Technology"),
            ("MU", "Micron Technology Inc.", "NASDAQ", "Technology"),
            ("ADP", "Automatic Data Processing Inc.", "NASDAQ", "Technology"),
            ("INTU", "Intuit Inc.", "NASDAQ", "Technology"),
            ("ISRG", "Intuitive Surgical Inc.", "NASDAQ", "Health Care"),
            ("GILD", "Gilead Sciences Inc.", "NASDAQ", "Health Care")
        ]
        
        for symbol, name, exchange, sector in popular_companies:
            company = CachedCompany(
                symbol=symbol,
                name=name,
                exchange=exchange,
                sector=sector
            )
            cache.add_company(company)
        
        cache.save_cache()
        logger.info(f"Cache inizializzata con {len(popular_companies)} aziende Fortune 500")
    
    return cache


if __name__ == "__main__":
    """Test del sistema di cache"""
    cache = initialize_fortune500_cache()
    
    # Test di ricerca
    test_companies = ["Apple", "Microsoft", "Google", "Amazon", "Tesla", "Azienda Inesistente"]
    
    print("Test ricerca nella cache Fortune 500:")
    print("=" * 50)
    
    for company_name in test_companies:
        result = cache.search_company(company_name)
        if result:
            print(f"✓ Trovata: {company_name} -> {result.symbol} ({result.name})")
        else:
            print(f"✗ Non trovata: {company_name}")
    
    # Statistiche cache
    stats = cache.get_cache_stats()
    print(f"\nStatistiche cache:")
    print(f"Totale aziende: {stats['total_companies']}")
    print(f"Exchange: {stats['exchanges']}")
    print(f"Settori: {len(stats['sectors'])}")
