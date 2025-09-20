import { Building2, TrendingUp, DollarSign } from 'lucide-react';
import { CompanyFundamentals } from '@/types/financial';

interface CompanyCardProps {
  company: CompanyFundamentals;
}

export const CompanyCard = ({ company }: CompanyCardProps) => {
  const formatMarketCap = (marketCap: number | null): string => {
    if (marketCap === null) return 'N/A';
    if (marketCap >= 1e12) {
      return `${(marketCap / 1e12).toFixed(2)}T`;
    } else if (marketCap >= 1e9) {
      return `${(marketCap / 1e9).toFixed(2)}B`;
    } else if (marketCap >= 1e6) {
      return `${(marketCap / 1e6).toFixed(2)}M`;
    }
    return `${marketCap.toLocaleString()}`;
  };

  const formatValue = (value: number | null, decimals: number = 2, suffix: string = ''): string => {
    if (value === null) return 'N/A';
    return `${value.toFixed(decimals)}${suffix}`;
  };

  return (
    <div className="financial-card">
      <div className="flex items-start justify-between mb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-primary/10 rounded-lg">
              <Building2 className="w-6 h-6 text-primary" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-foreground">{company.ticker}</h2>
              <p className="text-muted-foreground">{company.name}</p>
            </div>
          </div>
        </div>
        <div className="text-right space-y-1">
          <div className="flex items-center gap-2">
            <DollarSign className="w-4 h-4 text-muted-foreground" />
            <span className="text-lg font-semibold">{formatMarketCap(company.marketCap)}</span>
          </div>
          <p className="text-sm text-muted-foreground">Market Cap</p>
        </div>
      </div>

      <div className="space-y-4">
        <div className="flex items-center gap-2 mb-3">
          <TrendingUp className="w-5 h-5 text-primary" />
          <h3 className="font-semibold text-foreground">Fundamentals</h3>
          <span className="px-3 py-1 bg-primary/10 text-primary text-sm rounded-full">
            {company.sector}
          </span>
        </div>

        <div className="grid grid-cols-3 gap-4">
          <div className="text-center p-4 bg-surface rounded-lg border border-border">
            <div className="text-2xl font-bold text-foreground mb-1">
              {formatValue(company.fundamentals.PE, 2)}
            </div>
            <div className="text-sm text-muted-foreground">P/E Ratio</div>
          </div>
          <div className="text-center p-4 bg-surface rounded-lg border border-border">
            <div className="text-2xl font-bold text-foreground mb-1">
              {formatValue(company.fundamentals.PB, 2)}
            </div>
            <div className="text-sm text-muted-foreground">P/B Ratio</div>
          </div>
          <div className="text-center p-4 bg-surface rounded-lg border border-border">
            <div className="text-2xl font-bold text-foreground mb-1">
              {formatValue(company.fundamentals.ROE, 1, '%')}
            </div>
            <div className="text-sm text-muted-foreground">ROE</div>
          </div>
        </div>
      </div>
    </div>
  );
};