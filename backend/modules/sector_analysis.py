#!/usr/bin/env python3
"""
Sector Analysis Module
Calcola benchmark dinamici per settore usando le prime 10 aziende per market cap
"""

import requests
import json
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from modules.financial_ratios import FinancialRatios


@dataclass
class SectorCompany:
    """Classe per rappresentare un'azienda nel settore"""
    symbol: str
    name: str
    market_cap: float
    pe_ratio: Optional[float] = None
    pb_ratio: Optional[float] = None
    roe_percent: Optional[float] = None


class SectorAnalyzer:
    """Analizzatore di settore per calcolare benchmark dinamici"""
    
    def __init__(self, fmp_client):
        """
        Inizializza l'analizzatore di settore
        
        Args:
            fmp_client: Istanza di FinancialModelingPrepClient
        """
        self.fmp_client = fmp_client
        self.api_key = fmp_client.api_key
        self.base_url = "https://financialmodelingprep.com/api/v3"
        self.session = requests.Session()
        self.session.params = {'apikey': self.api_key}
        
        # Cache per i benchmark settoriali (24h)
        self._benchmark_cache = {}
        self._cache_timestamps = {}
        
    def get_companies_by_sector(self, sector: str, limit: int = 20) -> List[Dict]:
        """
        Ottiene le aziende di un settore specifico
        
        Args:
            sector: Nome del settore
            limit: Numero massimo di aziende da recuperare
            
        Returns:
            Lista di dizionari con informazioni aziendali
        """
        endpoint = f"{self.base_url}/stock-screener"
        params = {
            'sector': sector,
            'limit': limit,
            'exchange': 'NASDAQ,NYSE,AMEX'
        }
        
        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            
            companies = response.json()
            
            # Filtra e ordina per market cap
            valid_companies = []
            for company in companies:
                market_cap = company.get('marketCap')
                if market_cap and market_cap > 0:
                    valid_companies.append(company)
            
            # Ordina per market cap (decrescente)
            valid_companies.sort(key=lambda x: x.get('marketCap', 0), reverse=True)
            
            return valid_companies[:10]  # Top 10
            
        except Exception as e:
            print(f"Errore nel recupero aziende settore {sector}: {e}")
            return []
    
    def get_company_ratios(self, symbol: str) -> Tuple[Optional[float], Optional[float], Optional[float]]:
        """
        Ottiene i ratios finanziari per un'azienda
        
        Args:
            symbol: Ticker symbol dell'azienda
            
        Returns:
            Tupla con (PE, PB, ROE)
        """
        try:
            ratios_calculator = FinancialRatios(symbol)
            ratios = ratios_calculator.get_all_ratios()
            
            return (
                ratios.get('pe_ratio'),
                ratios.get('pb_ratio'),
                ratios.get('roe_percent')
            )
        except Exception as e:
            print(f"Errore nel calcolo ratios per {symbol}: {e}")
            return (None, None, None)
    
    def calculate_sector_averages(self, companies: List[SectorCompany]) -> Dict[str, float]:
        """
        Calcola le medie settoriali per i ratios
        
        Args:
            companies: Lista di aziende del settore
            
        Returns:
            Dizionario con medie calcolate
        """
        # Raccoglie tutti i valori validi
        pe_values = [c.pe_ratio for c in companies if c.pe_ratio is not None and c.pe_ratio > 0]
        pb_values = [c.pb_ratio for c in companies if c.pb_ratio is not None and c.pb_ratio > 0]
        roe_values = [c.roe_percent for c in companies if c.roe_percent is not None]
        
        # Calcola medie
        avg_pe = sum(pe_values) / len(pe_values) if pe_values else None
        avg_pb = sum(pb_values) / len(pb_values) if pb_values else None
        avg_roe = sum(roe_values) / len(roe_values) if roe_values else None
        
        return {
            "PE": round(avg_pe, 2) if avg_pe else None,
            "PB": round(avg_pb, 2) if avg_pb else None,
            "ROE": round(avg_roe, 2) if avg_roe else None
        }
    
    async def calculate_sector_benchmark(self, sector: str) -> Dict:
        """
        Calcola il benchmark settoriale dinamico
        
        Args:
            sector: Nome del settore
            
        Returns:
            Dizionario con benchmark e aziende utilizzate
        """
        # Controlla cache (24h)
        cache_key = f"sector_{sector}"
        current_time = time.time()
        
        if (cache_key in self._benchmark_cache and 
            cache_key in self._cache_timestamps and
            current_time - self._cache_timestamps[cache_key] < 86400):  # 24h
            return self._benchmark_cache[cache_key]
        
        print(f"Calcolando benchmark per settore: {sector}")
        
        # Ottieni aziende del settore
        sector_companies = self.get_companies_by_sector(sector)
        
        if not sector_companies:
            raise ValueError(f"Nessuna azienda trovata per il settore: {sector}")
        
        # Processa le prime 10 aziende
        processed_companies = []
        companies_used = []
        
        for company_data in sector_companies[:10]:
            symbol = company_data.get('symbol')
            name = company_data.get('companyName', 'N/A')
            market_cap = company_data.get('marketCap', 0)
            
            if not symbol:
                continue
            
            # Ottieni ratios finanziari
            pe, pb, roe = self.get_company_ratios(symbol)
            
            company = SectorCompany(
                symbol=symbol,
                name=name,
                market_cap=market_cap,
                pe_ratio=pe,
                pb_ratio=pb,
                roe_percent=roe
            )
            
            processed_companies.append(company)
            companies_used.append(symbol)
            
            # Pausa per evitare rate limiting
            time.sleep(0.1)
        
        # Calcola benchmark
        benchmark = self.calculate_sector_averages(processed_companies)
        
        # Prepara risultato
        result = {
            "sector": sector,
            "companies_used": companies_used,
            "benchmark": benchmark
        }
        
        # Aggiorna cache
        self._benchmark_cache[cache_key] = result
        self._cache_timestamps[cache_key] = current_time
        
        print(f"Benchmark calcolato per {sector}: {benchmark}")
        
        return result
    
    def get_cache_status(self) -> Dict:
        """Restituisce lo stato della cache"""
        return {
            "cached_sectors": list(self._benchmark_cache.keys()),
            "cache_timestamps": self._cache_timestamps
        }
    
    def clear_cache(self):
        """Pulisce la cache"""
        self._benchmark_cache.clear()
        self._cache_timestamps.clear()
