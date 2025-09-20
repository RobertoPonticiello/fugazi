import { CompanyFundamentals, SectorBenchmark, AnalysisResult } from '@/types/financial';

// Mock data for demonstration
const mockCompanies: Record<string, CompanyFundamentals> = {
  'AAPL': {
    ticker: 'AAPL',
    name: 'Apple Inc.',
    sector: 'Technology',
    marketCap: 2700000000000,
    fundamentals: { PE: 28.5, PB: 12.3, ROE: 18.7 }
  },
  'MSFT': {
    ticker: 'MSFT',
    name: 'Microsoft Corporation',
    sector: 'Technology',
    marketCap: 2400000000000,
    fundamentals: { PE: 26.8, PB: 8.9, ROE: 22.1 }
  },
  'GOOGL': {
    ticker: 'GOOGL',
    name: 'Alphabet Inc.',
    sector: 'Technology',
    marketCap: 1600000000000,
    fundamentals: { PE: 22.1, PB: 4.2, ROE: 15.8 }
  },
  'TSLA': {
    ticker: 'TSLA',
    name: 'Tesla Inc.',
    sector: 'Consumer Discretionary',
    marketCap: 800000000000,
    fundamentals: { PE: 65.2, PB: 14.8, ROE: 19.3 }
  },
  'NVDA': {
    ticker: 'NVDA',
    name: 'NVIDIA Corporation',
    sector: 'Technology',
    marketCap: 1800000000000,
    fundamentals: { PE: 45.2, PB: 18.9, ROE: 35.8 }
  },
  'AMZN': {
    ticker: 'AMZN',
    name: 'Amazon.com Inc.',
    sector: 'Consumer Discretionary',
    marketCap: 1500000000000,
    fundamentals: { PE: 42.8, PB: 8.1, ROE: 12.4 }
  }
};

const sectorBenchmarks: Record<string, SectorBenchmark> = {
  'Technology': {
    sector: 'Technology',
    companiesUsed: ['AAPL', 'MSFT', 'NVDA', 'GOOGL', 'ORCL', 'CRM', 'INTC', 'AMD', 'NFLX', 'ADBE'],
    benchmark: { PE: 25.2, PB: 10.1, ROE: 16.5 }
  },
  'Consumer Discretionary': {
    sector: 'Consumer Discretionary',
    companiesUsed: ['TSLA', 'AMZN', 'HD', 'MCD', 'NKE', 'SBUX', 'LOW', 'TJX', 'BKNG', 'CMG'],
    benchmark: { PE: 35.8, PB: 8.9, ROE: 14.2 }
  }
};

export const mockApi = {
  async getCompany(ticker: string): Promise<CompanyFundamentals> {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 800));
    
    const company = mockCompanies[ticker.toUpperCase()];
    if (!company) {
      throw new Error(`Company with ticker ${ticker} not found`);
    }
    return company;
  },

  async getSectorBenchmark(sector: string): Promise<SectorBenchmark> {
    await new Promise(resolve => setTimeout(resolve, 500));
    
    const benchmark = sectorBenchmarks[sector];
    if (!benchmark) {
      throw new Error(`Sector ${sector} not found`);
    }
    return benchmark;
  },

  async getAnalysis(ticker: string): Promise<AnalysisResult> {
    const company = await this.getCompany(ticker);
    const benchmark = await this.getSectorBenchmark(company.sector);

    // Calculate indicators based on thresholds
    const calculateIndicator = (companyValue: number, benchmarkValue: number): 'Overvalued' | 'Fairly valued' | 'Undervalued' => {
      const ratio = companyValue / benchmarkValue;
      if (ratio > 1.2) return 'Overvalued';
      if (ratio < 0.8) return 'Undervalued';
      return 'Fairly valued';
    };

    const indicators = {
      PE: calculateIndicator(company.fundamentals.PE, benchmark.benchmark.PE),
      PB: calculateIndicator(company.fundamentals.PB, benchmark.benchmark.PB),
      ROE: calculateIndicator(benchmark.benchmark.ROE, company.fundamentals.ROE), // ROE is inverted (higher is better)
    };

    // Calculate weighted score
    const peScore = company.fundamentals.PE > benchmark.benchmark.PE * 1.2 ? -1 : 
                   company.fundamentals.PE < benchmark.benchmark.PE * 0.8 ? 1 : 0;
    const pbScore = company.fundamentals.PB > benchmark.benchmark.PB * 1.2 ? -1 : 
                   company.fundamentals.PB < benchmark.benchmark.PB * 0.8 ? 1 : 0;
    const roeScore = company.fundamentals.ROE > benchmark.benchmark.ROE * 1.2 ? 1 : 
                    company.fundamentals.ROE < benchmark.benchmark.ROE * 0.8 ? -1 : 0;

    const score = (peScore * 0.5) + (pbScore * 0.3) + (roeScore * 0.2);
    
    const finalSignal = score >= 0.2 ? 'Undervalued' : 
                       score <= -0.2 ? 'Overvalued' : 'Fairly valued';

    return {
      ticker: company.ticker,
      sector: company.sector,
      fundamentals: company.fundamentals,
      benchmark: benchmark.benchmark,
      indicators,
      score,
      finalSignal
    };
  }
};