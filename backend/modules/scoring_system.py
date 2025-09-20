#!/usr/bin/env python3
"""
Scoring System Module
Sistema di scoring aggregato per indicatori finanziari con pesi configurabili
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import math


@dataclass
class IndicatorWeight:
    """Configurazione peso per un indicatore"""
    name: str
    weight: float
    description: str


class ScoringSystem:
    """Sistema di scoring aggregato per analisi finanziaria"""
    
    def __init__(self):
        """Inizializza il sistema di scoring con pesi predefiniti"""
        # Pesi per gli indicatori (devono sommare a 1.0)
        self.weights = {
            "PE": 0.5,   # Price-to-Earnings: 50% del peso
            "PB": 0.3,   # Price-to-Book: 30% del peso  
            "ROE": 0.2   # Return on Equity: 20% del peso
        }
        
        # Soglie per la classificazione (percentuali)
        self.thresholds = {
            "overvalued_threshold": 20,    # >20% sopra media = overvalued
            "fair_range": 20,              # ±20% dalla media = fair
            "undervalued_threshold": 20    # >20% sotto media = undervalued
        }
        
        # Soglie per il punteggio finale
        self.score_thresholds = {
            "overvalued": -0.2,
            "fairly_valued_low": -0.2,
            "fairly_valued_high": 0.2,
            "undervalued": 0.2
        }
    
    def calculate_individual_score(self, company_value: Optional[float], 
                                 benchmark_value: Optional[float], 
                                 indicator_type: str) -> Tuple[float, str]:
        """
        Calcola il punteggio individuale per un indicatore
        
        Args:
            company_value: Valore dell'azienda
            benchmark_value: Valore benchmark del settore
            indicator_type: Tipo di indicatore (PE, PB, ROE)
            
        Returns:
            Tupla (score, classification)
        """
        # Gestisce valori None
        if company_value is None or benchmark_value is None or benchmark_value == 0:
            return 0.0, "N/A"
        
        # Calcola la deviazione percentuale
        deviation_percent = ((company_value - benchmark_value) / benchmark_value) * 100
        
        # Per ROE, logica inversa: valori più alti sono meglio
        if indicator_type == "ROE":
            if deviation_percent > self.thresholds["overvalued_threshold"]:
                return 1.0, "Undervalued"  # ROE alto = buono
            elif deviation_percent < -self.thresholds["overvalued_threshold"]:
                return -1.0, "Overvalued"  # ROE basso = cattivo
            else:
                return 0.0, "Fair"
        
        # Per PE e PB, logica normale: valori più bassi sono meglio
        else:
            if deviation_percent > self.thresholds["overvalued_threshold"]:
                return -1.0, "Overvalued"  # Valore alto = cattivo
            elif deviation_percent < -self.thresholds["overvalued_threshold"]:
                return 1.0, "Undervalued"  # Valore basso = buono
            else:
                return 0.0, "Fair"
    
    def calculate_weighted_score(self, individual_scores: Dict[str, float]) -> float:
        """
        Calcola il punteggio pesato aggregato
        
        Args:
            individual_scores: Dizionario con punteggi individuali
            
        Returns:
            Punteggio pesato finale
        """
        weighted_sum = 0.0
        total_weight = 0.0
        
        for indicator, score in individual_scores.items():
            if indicator in self.weights:
                weight = self.weights[indicator]
                weighted_sum += score * weight
                total_weight += weight
        
        # Normalizza se i pesi non sommano esattamente a 1
        if total_weight > 0:
            return weighted_sum / total_weight
        
        return 0.0
    
    def classify_final_signal(self, final_score: float) -> str:
        """
        Classifica il segnale finale basato sul punteggio
        
        Args:
            final_score: Punteggio finale pesato
            
        Returns:
            Classificazione del segnale
        """
        if final_score <= self.score_thresholds["overvalued"]:
            return "Overvalued"
        elif (final_score > self.score_thresholds["fairly_valued_low"] and 
              final_score < self.score_thresholds["fairly_valued_high"]):
            return "Fairly valued"
        else:
            return "Undervalued"
    
    def analyze_company(self, company_fundamentals: Dict, 
                       sector_benchmark: Dict) -> Dict:
        """
        Esegue l'analisi completa di un'azienda
        
        Args:
            company_fundamentals: Dizionario con fondamentali aziendali
            sector_benchmark: Dizionario con benchmark settoriale
            
        Returns:
            Dizionario con analisi completa
        """
        individual_scores = {}
        indicators = {}
        
        # Analizza ogni indicatore
        for indicator in ["PE", "PB", "ROE"]:
            company_value = company_fundamentals.get(indicator)
            benchmark_value = sector_benchmark.get(indicator)
            
            score, classification = self.calculate_individual_score(
                company_value, benchmark_value, indicator
            )
            
            individual_scores[indicator] = score
            indicators[indicator] = classification
        
        # Calcola punteggio pesato finale
        final_score = self.calculate_weighted_score(individual_scores)
        
        # Classifica il segnale finale
        final_signal = self.classify_final_signal(final_score)
        
        return {
            "indicators": indicators,
            "individual_scores": individual_scores,
            "score": round(final_score, 3),
            "final_signal": final_signal
        }
    
    def update_weights(self, new_weights: Dict[str, float]) -> bool:
        """
        Aggiorna i pesi degli indicatori
        
        Args:
            new_weights: Nuovo dizionario dei pesi
            
        Returns:
            True se l'aggiornamento è riuscito, False altrimenti
        """
        # Verifica che i pesi siano validi
        if not isinstance(new_weights, dict):
            return False
        
        # Verifica che tutti i pesi siano numeri positivi
        for weight in new_weights.values():
            if not isinstance(weight, (int, float)) or weight < 0:
                return False
        
        # Verifica che la somma sia ragionevole (tra 0.9 e 1.1)
        total_weight = sum(new_weights.values())
        if total_weight < 0.9 or total_weight > 1.1:
            return False
        
        # Aggiorna i pesi
        self.weights.update(new_weights)
        return True
    
    def get_configuration(self) -> Dict:
        """
        Restituisce la configurazione attuale del sistema
        
        Returns:
            Dizionario con configurazione
        """
        return {
            "weights": self.weights,
            "thresholds": self.thresholds,
            "score_thresholds": self.score_thresholds
        }
    
    def explain_score(self, company_fundamentals: Dict, 
                     sector_benchmark: Dict) -> Dict:
        """
        Fornisce una spiegazione dettagliata del calcolo del punteggio
        
        Args:
            company_fundamentals: Dizionario con fondamentali aziendali
            sector_benchmark: Dizionario con benchmark settoriale
            
        Returns:
            Dizionario con spiegazione dettagliata
        """
        explanation = {
            "company_values": company_fundamentals,
            "benchmark_values": sector_benchmark,
            "calculation_details": {},
            "weights_used": self.weights
        }
        
        for indicator in ["PE", "PB", "ROE"]:
            company_value = company_fundamentals.get(indicator)
            benchmark_value = sector_benchmark.get(indicator)
            
            if company_value and benchmark_value and benchmark_value != 0:
                deviation_percent = ((company_value - benchmark_value) / benchmark_value) * 100
                score, classification = self.calculate_individual_score(
                    company_value, benchmark_value, indicator
                )
                
                explanation["calculation_details"][indicator] = {
                    "company_value": company_value,
                    "benchmark_value": benchmark_value,
                    "deviation_percent": round(deviation_percent, 2),
                    "individual_score": score,
                    "classification": classification,
                    "weight": self.weights.get(indicator, 0)
                }
            else:
                explanation["calculation_details"][indicator] = {
                    "company_value": company_value,
                    "benchmark_value": benchmark_value,
                    "deviation_percent": "N/A",
                    "individual_score": 0,
                    "classification": "N/A",
                    "weight": self.weights.get(indicator, 0)
                }
        
        return explanation
