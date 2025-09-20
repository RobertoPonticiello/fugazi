"""
Analyst Recommendations Module

Modulo per recuperare e gestire i suggerimenti degli analisti tramite Financial Modeling Prep API.
I dati vengono mantenuti separati dal sistema di scoring per non influenzare i calcoli.
"""

import requests
import os
from typing import Optional, Dict, List
from dataclasses import dataclass


@dataclass
class AnalystConsensus:
    """Struttura dati per il consenso degli analisti"""
    symbol: str
    strong_buy: int
    buy: int
    hold: int
    sell: int
    strong_sell: int
    consensus: str
    total_analysts: int = 0
    
    def __post_init__(self):
        """Calcola il totale degli analisti dopo l'inizializzazione"""
        self.total_analysts = self.strong_buy + self.buy + self.hold + self.sell + self.strong_sell
    
    def get_bullish_percentage(self) -> float:
        """Calcola la percentuale di analisti bullish (Strong Buy + Buy)"""
        if self.total_analysts == 0:
            return 0.0
        return round(((self.strong_buy + self.buy) / self.total_analysts) * 100, 2)
    
    def get_bearish_percentage(self) -> float:
        """Calcola la percentuale di analisti bearish (Strong Sell + Sell)"""
        if self.total_analysts == 0:
            return 0.0
        return round(((self.strong_sell + self.sell) / self.total_analysts) * 100, 2)
    
    def get_neutral_percentage(self) -> float:
        """Calcola la percentuale di analisti neutral (Hold)"""
        if self.total_analysts == 0:
            return 0.0
        return round((self.hold / self.total_analysts) * 100, 2)


class AnalystRecommendationsClient:
    """Client per recuperare i suggerimenti degli analisti"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inizializza il client con la chiave API
        
        Args:
            api_key: Chiave API di Financial Modeling Prep
        """
        self.api_key = api_key or os.getenv('FMP_API_KEY')
        if not self.api_key:
            raise ValueError(
                "API key non trovata. Forniscila come parametro o imposta la "
                "variabile d'ambiente FMP_API_KEY"
            )
        
        self.base_url = "https://financialmodelingprep.com/stable"
        self.session = requests.Session()
    
    def get_analyst_consensus(self, symbol: str) -> Optional[AnalystConsensus]:
        """
        Recupera il consenso degli analisti per un simbolo
        
        Args:
            symbol: Simbolo del titolo (es. AAPL)
            
        Returns:
            Oggetto AnalystConsensus con i dati del consenso o None se non disponibile
        """
        try:
            url = f"{self.base_url}/grades-consensus"
            params = {
                'symbol': symbol.upper(),
                'apikey': self.api_key
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if not data or len(data) == 0:
                return None
            
            # Prendi il primo elemento (dovrebbe essere l'unico)
            consensus_data = data[0]
            
            return AnalystConsensus(
                symbol=consensus_data['symbol'],
                strong_buy=consensus_data['strongBuy'],
                buy=consensus_data['buy'],
                hold=consensus_data['hold'],
                sell=consensus_data['sell'],
                strong_sell=consensus_data['strongSell'],
                consensus=consensus_data['consensus']
            )
            
        except requests.exceptions.RequestException as e:
            print(f"Errore nella richiesta API per {symbol}: {e}")
            return None
        except (KeyError, ValueError) as e:
            print(f"Errore nel parsing dei dati per {symbol}: {e}")
            return None
        except Exception as e:
            print(f"Errore imprevisto per {symbol}: {e}")
            return None
    
    def get_multiple_consensus(self, symbols: List[str]) -> Dict[str, Optional[AnalystConsensus]]:
        """
        Recupera il consenso degli analisti per più simboli
        
        Args:
            symbols: Lista di simboli
            
        Returns:
            Dizionario con simbolo come chiave e AnalystConsensus come valore
        """
        results = {}
        for symbol in symbols:
            results[symbol] = self.get_analyst_consensus(symbol)
        return results


def test_analyst_recommendations():
    """Funzione di test per verificare il funzionamento del modulo"""
    try:
        client = AnalystRecommendationsClient()
        
        # Test con AAPL
        consensus = client.get_analyst_consensus("AAPL")
        
        if consensus:
            print(f"Consenso per {consensus.symbol}:")
            print(f"  Consenso: {consensus.consensus}")
            print(f"  Strong Buy: {consensus.strong_buy}")
            print(f"  Buy: {consensus.buy}")
            print(f"  Hold: {consensus.hold}")
            print(f"  Sell: {consensus.sell}")
            print(f"  Strong Sell: {consensus.strong_sell}")
            print(f"  Totale analisti: {consensus.total_analysts}")
            print(f"  % Bullish: {consensus.get_bullish_percentage()}%")
            print(f"  % Bearish: {consensus.get_bearish_percentage()}%")
            print(f"  % Neutral: {consensus.get_neutral_percentage()}%")
        else:
            print("Nessun dato disponibile per AAPL")
            
    except Exception as e:
        print(f"Errore nel test: {e}")


if __name__ == "__main__":
    test_analyst_recommendations()
