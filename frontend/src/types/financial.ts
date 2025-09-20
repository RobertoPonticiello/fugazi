export interface CompanyFundamentals {
  ticker: string;
  name: string;
  sector: string;
  marketCap: number | null;
  fundamentals: {
    PE: number | null;
    PB: number | null;
    ROE: number | null;
  };
}

export interface SectorBenchmark {
  sector: string;
  companiesUsed: string[];
  benchmark: {
    PE: number | null;
    PB: number | null;
    ROE: number | null;
  };
}

export interface AnalysisResult {
  ticker: string;
  sector: string;
  fundamentals: {
    PE: number | null;
    PB: number | null;
    ROE: number | null;
  };
  benchmark: {
    PE: number | null;
    PB: number | null;
    ROE: number | null;
  };
  indicators: {
    PE: 'Overvalued' | 'Fairly valued' | 'Undervalued' | 'N/A';
    PB: 'Overvalued' | 'Fairly valued' | 'Undervalued' | 'N/A';
    ROE: 'Overvalued' | 'Fairly valued' | 'Undervalued' | 'N/A';
  };
  score: number;
  finalSignal: 'Overvalued' | 'Fairly valued' | 'Undervalued';
}

export type SignalType = 'Overvalued' | 'Fairly valued' | 'Undervalued' | 'N/A';

export interface CompanySearchResult {
  company_name: string;
  ticker: string | null;
  found: boolean;
  source: 'cache' | 'api' | null;
  company_info?: {
    name: string;
    exchange: string | null;
    sector: string | null;
  };
  error?: string;
  suggestions?: string[];
}

export interface SearchSuggestion {
  name: string;
  ticker: string;
  exchange: string;
  sector: string;
}

export interface SearchSuggestionsResult {
  partial_name: string;
  suggestions: SearchSuggestion[];
  count: number;
}

export interface AnalystRecommendations {
  consensus: string;
  total_analysts: number;
  breakdown: {
    strong_buy: number;
    buy: number;
    hold: number;
    sell: number;
    strong_sell: number;
  };
  percentages: {
    bullish: number;
    neutral: number;
    bearish: number;
  };
}

export interface AnalystRecommendationsResponse {
  ticker: string;
  analyst_recommendations: AnalystRecommendations | null;
  message?: string;
  note?: string;
}

export interface CompleteAnalysisResult extends AnalysisResult {
  analyst_recommendations: AnalystRecommendations | null;
  disclaimer: {
    scoring_system: string;
    analyst_recommendations: string;
  };
}