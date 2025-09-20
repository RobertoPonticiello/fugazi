"""
Financial Ratios Calculator Module

Simple module to calculate P/E, P/B, and ROE ratios using Financial Modeling Prep API.

Usage:
    from financial_ratios import FinancialRatios
    
    ratios = FinancialRatios("AAPL", api_key="your_api_key")
    
    pe = ratios.get_pe_ratio()
    pb = ratios.get_pb_ratio()
    roe = ratios.get_roe()
    
    print(f"P/E: {pe}, P/B: {pb}, ROE: {roe}%")
"""

import requests
import os
from typing import Optional


class FinancialRatios:
    """Calculate P/E, P/B, and ROE ratios for a given ticker."""
    
    def __init__(self, ticker: str, api_key: Optional[str] = None):
        self.ticker = ticker.upper()
        self.api_key = api_key or os.getenv('FMP_API_KEY')
        
        if not self.api_key:
            raise ValueError("API key required")
        
        self._profile = None
        self._ratios = None
        self._income_statement = None
        self._balance_sheet = None
        self._loaded = False
    
    def _request(self, endpoint: str) -> Optional[dict]:
        """Make API request."""
        try:
            url = f"https://financialmodelingprep.com/stable/{endpoint}&apikey={self.api_key}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data if isinstance(data, list) and len(data) > 0 else None
            else:
                print(f"API request failed with status {response.status_code} for {endpoint}")
            return None
        except Exception as e:
            print(f"API request error for {endpoint}: {e}")
            return None
    
    def _load_data(self):
        """Load necessary data from API."""
        if self._loaded:
            return
        
        # Get company profile
        profile_data = self._request(f"profile?symbol={self.ticker}")
        if profile_data:
            self._profile = profile_data[0]
        
        # Get financial ratios
        ratios_data = self._request(f"ratios?symbol={self.ticker}&period=annual")
        if ratios_data:
            self._ratios = ratios_data[0]
        
        # Get income statement
        income_data = self._request(f"income-statement?symbol={self.ticker}&period=annual")
        if income_data:
            self._income_statement = income_data[0]
        
        # Get balance sheet
        balance_data = self._request(f"balance-sheet-statement?symbol={self.ticker}&period=annual")
        if balance_data:
            self._balance_sheet = balance_data[0]
        
        self._loaded = True
    
    def get_pe_ratio(self) -> Optional[float]:
        """Calculate P/E ratio."""
        self._load_data()
        
        # Try from ratios
        if self._ratios and 'priceEarningsRatio' in self._ratios:
            pe = self._ratios['priceEarningsRatio']
            if pe and pe > 0:
                return round(pe, 2)
        
        # Try from profile
        if self._profile and 'pe' in self._profile:
            pe = self._profile['pe']
            if pe and pe > 0:
                return round(pe, 2)
        
        # Calculate manually
        if self._profile and self._income_statement:
            price = self._profile.get('price')
            eps = self._income_statement.get('eps')
            
            if price and eps and eps > 0:
                return round(price / eps, 2)
        
        return None
    
    def get_pb_ratio(self) -> Optional[float]:
        """Calculate P/B ratio."""
        self._load_data()
        
        # Try from ratios
        if self._ratios and 'priceToBookRatio' in self._ratios:
            pb = self._ratios['priceToBookRatio']
            if pb and pb > 0:
                return round(pb, 2)
        
        # Calculate manually
        if self._profile and self._balance_sheet:
            price = self._profile.get('price')
            total_equity = self._balance_sheet.get('totalStockholdersEquity')
            shares = self._balance_sheet.get('commonStock') or self._income_statement.get('weightedAverageShsOut') if self._income_statement else None
            
            if price and total_equity and shares and shares > 0:
                book_value_per_share = total_equity / shares
                if book_value_per_share > 0:
                    return round(price / book_value_per_share, 2)
        
        return None
    
    def get_roe(self) -> Optional[float]:
        """Calculate ROE as percentage."""
        self._load_data()
        
        # Try from ratios
        if self._ratios and 'returnOnEquity' in self._ratios:
            roe = self._ratios['returnOnEquity']
            if roe is not None:
                return round(roe * 100, 2)
        
        # Calculate manually
        if self._income_statement and self._balance_sheet:
            net_income = self._income_statement.get('netIncome')
            equity = self._balance_sheet.get('totalStockholdersEquity')
            
            if net_income and equity and equity > 0:
                return round((net_income / equity) * 100, 2)
        
        return None
    
    def get_all_ratios(self) -> dict:
        """Get all three ratios."""
        return {
            'ticker': self.ticker,
            'pe_ratio': self.get_pe_ratio(),
            'pb_ratio': self.get_pb_ratio(),
            'roe_percent': self.get_roe()
        }


def calculate_ratios(ticker: str, api_key: Optional[str] = None) -> dict:
    """Convenience function to calculate all ratios."""
    ratios = FinancialRatios(ticker, api_key)
    return ratios.get_all_ratios()


# Example usage
if __name__ == "__main__":
    # Test with Apple
    api_key = os.getenv('FMP_API_KEY')
    if not api_key:
        print("Set FMP_API_KEY environment variable")
        exit(1)
    
    ratios = FinancialRatios("AAPL", api_key)
    
    pe = ratios.get_pe_ratio()
    pb = ratios.get_pb_ratio()
    roe = ratios.get_roe()
    
    print(f"AAPL - P/E: {pe}, P/B: {pb}, ROE: {roe}%")
    
    # Or get all at once
    all_ratios = ratios.get_all_ratios()
    print(all_ratios)
