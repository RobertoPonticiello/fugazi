#!/usr/bin/env python3
"""
Finge Backend - FastAPI Application
MVP per analisi finanziaria con scoring aggregato e benchmark dinamici
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List, Optional
import uvicorn
import os
import requests
from dotenv import load_dotenv

from modules.financial_ratios import FinancialRatios
from modules.get_tick import FinancialModelingPrepClient
from modules.sector_analysis import SectorAnalyzer
from modules.scoring_system import ScoringSystem
from modules.analyst_recommendations import AnalystRecommendationsClient
from config import get_api_key, get_host, get_port, get_cors_origins, RELOAD

# Carica variabili d'ambiente
load_dotenv()

app = FastAPI(
    title="Finge API",
    description="API per analisi finanziaria con scoring aggregato e benchmark dinamici",
    version="1.0.0"
)

# CORS middleware per permettere richieste dal frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inizializza i moduli
fmp_client = FinancialModelingPrepClient(api_key=get_api_key())
sector_analyzer = SectorAnalyzer(fmp_client)
scoring_system = ScoringSystem()
analyst_client = AnalystRecommendationsClient(api_key=get_api_key())

@app.get("/")
async def root():
    """Endpoint di test"""
    return {"message": "Finge API - Sistema di analisi finanziaria"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "api_key_valid": fmp_client.test_api_key()}

@app.get("/api/test/{ticker}")
async def test_ticker_data(ticker: str):
    """
    Endpoint di test per verificare i dati disponibili per un ticker
    """
    try:
        # Test income statement
        income_endpoint = f"https://financialmodelingprep.com/stable/income-statement?symbol={ticker}&period=annual&apikey={fmp_client.api_key}"
        response = requests.get(income_endpoint)
        income_data = response.json() if response.status_code == 200 else None
        
        # Test balance sheet
        balance_endpoint = f"https://financialmodelingprep.com/stable/balance-sheet-statement?symbol={ticker}&period=annual&apikey={fmp_client.api_key}"
        response = requests.get(balance_endpoint)
        balance_data = response.json() if response.status_code == 200 else None
        
        # Test ratios
        ratios_endpoint = f"https://financialmodelingprep.com/stable/ratios?symbol={ticker}&period=annual&apikey={fmp_client.api_key}"
        response = requests.get(ratios_endpoint)
        ratios_data = response.json() if response.status_code == 200 else None
        
        return {
            "ticker": ticker,
            "income_statement_available": income_data is not None and len(income_data) > 0,
            "balance_sheet_available": balance_data is not None and len(balance_data) > 0,
            "ratios_available": ratios_data is not None and len(ratios_data) > 0,
            "sample_income_data": income_data[0] if income_data else None,
            "sample_balance_data": balance_data[0] if balance_data else None,
            "sample_ratios_data": ratios_data[0] if ratios_data else None
        }
        
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/company/{ticker}")
async def get_company_data(ticker: str):
    """
    Endpoint per ottenere dati fondamentali di una società
    
    Args:
        ticker: Simbolo ticker dell'azienda (es. AAPL)
    
    Returns:
        Dizionario con dati fondamentali e settore
    """
    try:
        # Usa direttamente gli endpoint che sappiamo funzionare
        ticker_upper = ticker.upper()
        
        # Ottieni ratios direttamente
        ratios_endpoint = f"https://financialmodelingprep.com/stable/ratios?symbol={ticker_upper}&period=annual&apikey={fmp_client.api_key}"
        response = requests.get(ratios_endpoint)
        
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail=f"Dati non disponibili per ticker {ticker}")
        
        ratios_data = response.json()
        if not ratios_data or len(ratios_data) == 0:
            raise HTTPException(status_code=404, detail=f"Dati non disponibili per ticker {ticker}")
        
        latest_ratios = ratios_data[0]
        
        # Estrai i dati necessari
        pe_ratio = latest_ratios.get('priceToEarningsRatio')
        pb_ratio = latest_ratios.get('priceToBookRatio')
        
        # Calcola ROE dal net income e equity
        roe = latest_ratios.get('returnOnEquity')
        if roe is not None:
            roe_percent = round(roe * 100, 2)
        else:
            # Prova a calcolare ROE manualmente
            try:
                income_endpoint = f"https://financialmodelingprep.com/stable/income-statement?symbol={ticker_upper}&period=annual&apikey={fmp_client.api_key}"
                income_response = requests.get(income_endpoint)
                balance_endpoint = f"https://financialmodelingprep.com/stable/balance-sheet-statement?symbol={ticker_upper}&period=annual&apikey={fmp_client.api_key}"
                balance_response = requests.get(balance_endpoint)
                
                if (income_response.status_code == 200 and balance_response.status_code == 200):
                    income_data = income_response.json()
                    balance_data = balance_response.json()
                    
                    if income_data and balance_data and len(income_data) > 0 and len(balance_data) > 0:
                        net_income = income_data[0].get('netIncome')
                        total_equity = balance_data[0].get('totalStockholdersEquity')
                        
                        if net_income and total_equity and total_equity != 0:
                            roe_calculated = (net_income / total_equity) * 100
                            roe_percent = round(roe_calculated, 2)
            except Exception as e:
                print(f"Errore nel calcolo ROE per {ticker_upper}: {e}")
                roe_percent = None
        
        # Recupera market cap dai dati di balance sheet e income statement
        market_cap = None
        try:
            # Prova a ottenere market cap da balance sheet
            balance_endpoint = f"https://financialmodelingprep.com/stable/balance-sheet-statement?symbol={ticker_upper}&period=annual&apikey={fmp_client.api_key}"
            balance_response = requests.get(balance_endpoint)
            if balance_response.status_code == 200:
                balance_data = balance_response.json()
                if balance_data and len(balance_data) > 0:
                    # Usa totalAssets come proxy per market cap (approssimativo)
                    total_assets = balance_data[0].get('totalAssets')
                    if total_assets:
                        market_cap = total_assets
        except Exception as e:
            print(f"Errore nel recupero market cap per {ticker_upper}: {e}")
        
        # Per ora usiamo dati mock per nome e settore (da migliorare in futuro)
        company_names = {
            "AAPL": "Apple Inc.",
            "MSFT": "Microsoft Corporation", 
            "GOOGL": "Alphabet Inc.",
            "AMZN": "Amazon.com Inc.",
            "META": "Meta Platforms Inc.",
            "NVDA": "NVIDIA Corporation",
            "TSLA": "Tesla Inc."
        }
        
        sectors = {
            "AAPL": "Technology",
            "MSFT": "Technology",
            "GOOGL": "Technology", 
            "AMZN": "Consumer Discretionary",
            "META": "Technology",
            "NVDA": "Technology",
            "TSLA": "Consumer Discretionary"
        }
        
        # Prepara la risposta
        response = {
            "ticker": ticker_upper,
            "name": company_names.get(ticker_upper, f"{ticker_upper} Inc."),
            "sector": sectors.get(ticker_upper, "Technology"),
            "market_cap": market_cap,
            "fundamentals": {
                "PE": round(pe_ratio, 2) if pe_ratio else None,
                "PB": round(pb_ratio, 2) if pb_ratio else None,
                "ROE": roe_percent
            }
        }
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore nel recupero dati: {str(e)}")

@app.get("/api/sector/{sector}")
async def get_sector_benchmark(sector: str):
    """
    Endpoint per calcolare benchmark settoriale dinamico
    
    Args:
        sector: Nome del settore (es. Technology)
    
    Returns:
        Benchmark con media delle prime 10 aziende del settore
    """
    try:
        # Per ora usiamo benchmark mock basati su dati reali del settore Technology
        # In futuro questo sarà sostituito dal calcolo dinamico reale
        
        benchmark_mock = {
            "Technology": {
                "sector": "Technology",
                "companies_used": ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "ORCL", "CRM", "TSM", "INTC"],
                "benchmark": {
                    "PE": 25.2,
                    "PB": 10.1,
                    "ROE": 16.5
                }
            },
            "Consumer Discretionary": {
                "sector": "Consumer Discretionary", 
                "companies_used": ["AMZN", "TSLA", "HD", "MCD", "NKE", "SBUX", "LOW", "BKNG", "TJX", "CMG"],
                "benchmark": {
                    "PE": 22.8,
                    "PB": 8.5,
                    "ROE": 18.2
                }
            },
            "Healthcare": {
                "sector": "Healthcare",
                "companies_used": ["JNJ", "UNH", "PFE", "ABBV", "MRK", "TMO", "ABT", "DHR", "BMY", "AMGN"],
                "benchmark": {
                    "PE": 18.5,
                    "PB": 6.2,
                    "ROE": 12.8
                }
            }
        }
        
        # Restituisce il benchmark per il settore richiesto o usa Technology come default
        benchmark_data = benchmark_mock.get(sector, benchmark_mock["Technology"])
        
        return benchmark_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore nel calcolo benchmark: {str(e)}")

@app.get("/api/analysis/{ticker}")
async def get_company_analysis(ticker: str):
    """
    Endpoint per analisi completa con scoring aggregato
    
    Args:
        ticker: Simbolo ticker dell'azienda
    
    Returns:
        Analisi completa con confronto settoriale e segnale finale
    """
    try:
        # Ottieni dati aziendali
        company_data = await get_company_data(ticker)
        sector = company_data["sector"]
        
        # Ottieni benchmark settoriale
        benchmark_data = await get_sector_benchmark(sector)
        
        # Calcola scoring e segnali
        analysis_result = scoring_system.analyze_company(
            company_data["fundamentals"],
            benchmark_data["benchmark"]
        )
        
        # Prepara risposta completa
        response = {
            "ticker": ticker.upper(),
            "sector": sector,
            "fundamentals": company_data["fundamentals"],
            "benchmark": benchmark_data["benchmark"],
            "indicators": analysis_result["indicators"],
            "score": analysis_result["score"],
            "final_signal": analysis_result["final_signal"]
        }
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore nell'analisi: {str(e)}")

@app.get("/api/search/{company_name}")
async def search_company_by_name(company_name: str):
    """
    Cerca un'azienda per nome e restituisce il ticker
    Prima cerca nella cache Fortune 500, poi nell'API se necessario
    
    Args:
        company_name: Nome dell'azienda da cercare (es. "Apple", "Microsoft")
    
    Returns:
        Dizionario con ticker trovato e informazioni sulla fonte
    """
    try:
        # Usa il sistema di cache Fortune 500 che abbiamo implementato
        ticker = fmp_client.find_ticker_by_name(company_name)
        
        if ticker:
            # Verifica se è stata trovata nella cache o tramite API
            cached_company = fmp_client.search_cached_company(company_name)
            source = "cache" if cached_company else "api"
            
            return {
                "company_name": company_name,
                "ticker": ticker,
                "found": True,
                "source": source,
                "company_info": {
                    "name": cached_company.name if cached_company else company_name,
                    "exchange": cached_company.exchange if cached_company else None,
                    "sector": cached_company.sector if cached_company else None
                } if cached_company else None
            }
        else:
            return {
                "company_name": company_name,
                "ticker": None,
                "found": False,
                "error": "Azienda non trovata",
                "suggestions": [
                    "Verifica l'ortografia del nome",
                    "Prova con il nome completo dell'azienda",
                    "Assicurati che l'azienda sia quotata in borsa"
                ]
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore nella ricerca: {str(e)}")

@app.get("/api/search/suggestions/{partial_name}")
async def get_search_suggestions(partial_name: str):
    """
    Fornisce suggerimenti di ricerca basati su aziende Fortune 500 in cache
    
    Args:
        partial_name: Nome parziale dell'azienda (es. "App" per "Apple")
    
    Returns:
        Lista di suggerimenti con nomi e ticker
    """
    try:
        suggestions = []
        
        # Cerca nella cache Fortune 500 per suggerimenti
        if fmp_client.use_cache and fmp_client.cache:
            for key, company in fmp_client.cache.cache.items():
                # Filtra solo le aziende reali (non le chiavi per nome)
                if not key.startswith("name_") and company.name.lower().startswith(partial_name.lower()):
                    suggestions.append({
                        "name": company.name,
                        "ticker": company.symbol,
                        "exchange": company.exchange,
                        "sector": company.sector
                    })
        
        # Limita a 10 suggerimenti
        suggestions = suggestions[:10]
        
        return {
            "partial_name": partial_name,
            "suggestions": suggestions,
            "count": len(suggestions)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore nei suggerimenti: {str(e)}")

@app.get("/api/analyst-recommendations/{ticker}")
async def get_analyst_recommendations(ticker: str):
    """
    Endpoint per ottenere i suggerimenti degli analisti per un ticker
    
    Args:
        ticker: Simbolo ticker dell'azienda (es. AAPL)
    
    Returns:
        Dizionario con i suggerimenti degli analisti (separato dal sistema di scoring)
    """
    try:
        ticker_upper = ticker.upper()
        
        # Recupera il consenso degli analisti
        consensus = analyst_client.get_analyst_consensus(ticker_upper)
        
        if not consensus:
            return {
                "ticker": ticker_upper,
                "analyst_recommendations": None,
                "message": "Nessun dato disponibile sui suggerimenti degli analisti"
            }
        
        # Prepara la risposta con i dati degli analisti
        response = {
            "ticker": ticker_upper,
            "analyst_recommendations": {
                "consensus": consensus.consensus,
                "total_analysts": consensus.total_analysts,
                "breakdown": {
                    "strong_buy": consensus.strong_buy,
                    "buy": consensus.buy,
                    "hold": consensus.hold,
                    "sell": consensus.sell,
                    "strong_sell": consensus.strong_sell
                },
                "percentages": {
                    "bullish": consensus.get_bullish_percentage(),
                    "neutral": consensus.get_neutral_percentage(),
                    "bearish": consensus.get_bearish_percentage()
                }
            },
            "note": "I suggerimenti degli analisti sono forniti come dati informativi separati e non influenzano il sistema di scoring"
        }
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore nel recupero suggerimenti analisti: {str(e)}")

@app.get("/api/analysis-complete/{ticker}")
async def get_complete_analysis(ticker: str):
    """
    Endpoint per analisi completa che include sia lo scoring che i suggerimenti degli analisti
    
    Args:
        ticker: Simbolo ticker dell'azienda
    
    Returns:
        Analisi completa con scoring e suggerimenti degli analisti separati
    """
    try:
        # Ottieni l'analisi con scoring
        analysis_data = await get_company_analysis(ticker)
        
        # Ottieni i suggerimenti degli analisti
        analyst_data = await get_analyst_recommendations(ticker)
        
        # Combina i dati mantenendo la separazione
        complete_response = {
            "ticker": ticker.upper(),
            "sector": analysis_data["sector"],
            "fundamentals": analysis_data["fundamentals"],
            "benchmark": analysis_data["benchmark"],
            "indicators": analysis_data["indicators"],
            "score": analysis_data["score"],
            "final_signal": analysis_data["final_signal"],
            "analyst_recommendations": analyst_data["analyst_recommendations"],
            "disclaimer": {
                "scoring_system": "Il sistema di scoring è basato esclusivamente su indicatori finanziari fondamentali",
                "analyst_recommendations": "I suggerimenti degli analisti sono forniti come dati informativi separati e non influenzano il calcolo dello score"
            }
        }
        
        return complete_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore nell'analisi completa: {str(e)}")

if __name__ == "__main__":
    import sys
    # Disabilita il reload se eseguito da Cursor per evitare doppi avvii
    reload_enabled = RELOAD and "--no-reload" not in sys.argv
    
    uvicorn.run(
        "main:app",
        host=get_host(),
        port=get_port(),
        reload=reload_enabled
    )
