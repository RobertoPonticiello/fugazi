import { CompanyFundamentals, SectorBenchmark, AnalysisResult, CompanySearchResult, SearchSuggestionsResult, AnalystRecommendationsResponse, CompleteAnalysisResult } from '@/types/financial';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

class ApiError extends Error {
  constructor(message: string, public status?: number) {
    super(message);
    this.name = 'ApiError';
  }
}

async function apiRequest<T>(endpoint: string): Promise<T> {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`);
    
    if (!response.ok) {
      const errorText = await response.text();
      throw new ApiError(
        `API request failed: ${errorText}`,
        response.status
      );
    }
    
    return await response.json();
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    throw new ApiError(`Network error: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}

export const api = {
  async getCompany(ticker: string): Promise<CompanyFundamentals> {
    try {
      const data = await apiRequest<any>(`/company/${ticker.toUpperCase()}`);
      
      return {
        ticker: data.ticker,
        name: data.name,
        sector: data.sector,
        marketCap: data.market_cap,
        fundamentals: {
          PE: data.fundamentals.PE,
          PB: data.fundamentals.PB,
          ROE: data.fundamentals.ROE
        }
      };
    } catch (error) {
      console.error('Error fetching company data:', error);
      throw error;
    }
  },

  async getSectorBenchmark(sector: string): Promise<SectorBenchmark> {
    try {
      const data = await apiRequest<any>(`/sector/${sector}`);
      
      return {
        sector: data.sector,
        companiesUsed: data.companies_used,
        benchmark: {
          PE: data.benchmark.PE,
          PB: data.benchmark.PB,
          ROE: data.benchmark.ROE
        }
      };
    } catch (error) {
      console.error('Error fetching sector benchmark:', error);
      throw error;
    }
  },

  async getAnalysis(ticker: string): Promise<AnalysisResult> {
    try {
      const data = await apiRequest<any>(`/analysis/${ticker.toUpperCase()}`);
      
      return {
        ticker: data.ticker,
        sector: data.sector,
        fundamentals: {
          PE: data.fundamentals.PE,
          PB: data.fundamentals.PB,
          ROE: data.fundamentals.ROE
        },
        benchmark: {
          PE: data.benchmark.PE,
          PB: data.benchmark.PB,
          ROE: data.benchmark.ROE
        },
        indicators: {
          PE: data.indicators.PE,
          PB: data.indicators.PB,
          ROE: data.indicators.ROE
        },
        score: data.score,
        finalSignal: data.final_signal
      };
    } catch (error) {
      console.error('Error fetching analysis:', error);
      throw error;
    }
  },

  async searchCompany(companyName: string): Promise<CompanySearchResult> {
    try {
      const data = await apiRequest<CompanySearchResult>(`/search/${encodeURIComponent(companyName)}`);
      return data;
    } catch (error) {
      console.error('Error searching company:', error);
      throw error;
    }
  },

  async getSearchSuggestions(partialName: string): Promise<SearchSuggestionsResult> {
    try {
      const data = await apiRequest<SearchSuggestionsResult>(`/search/suggestions/${encodeURIComponent(partialName)}`);
      return data;
    } catch (error) {
      console.error('Error fetching search suggestions:', error);
      throw error;
    }
  },

  async getAnalystRecommendations(ticker: string): Promise<AnalystRecommendationsResponse> {
    try {
      const data = await apiRequest<AnalystRecommendationsResponse>(`/analyst-recommendations/${ticker.toUpperCase()}`);
      return data;
    } catch (error) {
      console.error('Error fetching analyst recommendations:', error);
      throw error;
    }
  },

  async getCompleteAnalysis(ticker: string): Promise<CompleteAnalysisResult> {
    try {
      const data = await apiRequest<any>(`/analysis-complete/${ticker.toUpperCase()}`);
      
      return {
        ticker: data.ticker,
        sector: data.sector,
        fundamentals: {
          PE: data.fundamentals.PE,
          PB: data.fundamentals.PB,
          ROE: data.fundamentals.ROE
        },
        benchmark: {
          PE: data.benchmark.PE,
          PB: data.benchmark.PB,
          ROE: data.benchmark.ROE
        },
        indicators: {
          PE: data.indicators.PE,
          PB: data.indicators.PB,
          ROE: data.indicators.ROE
        },
        score: data.score,
        finalSignal: data.final_signal,
        analyst_recommendations: data.analyst_recommendations,
        disclaimer: data.disclaimer
      };
    } catch (error) {
      console.error('Error fetching complete analysis:', error);
      throw error;
    }
  },

  async healthCheck(): Promise<{ status: string; api_key_valid: string }> {
    try {
      const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';
      const healthUrl = baseUrl.replace('/api', '/health');
      const response = await fetch(healthUrl);
      return await response.json();
    } catch (error) {
      console.error('Health check failed:', error);
      throw error;
    }
  }
};
