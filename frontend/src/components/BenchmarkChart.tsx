import { AnalysisResult } from '@/types/financial';
import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer, Cell } from 'recharts';

interface BenchmarkChartProps {
  analysis: AnalysisResult;
}

export const BenchmarkChart = ({ analysis }: BenchmarkChartProps) => {
  const chartData = [
    {
      metric: 'P/E',
      company: analysis.fundamentals.PE,
      sector: analysis.benchmark.PE,
      signal: analysis.indicators.PE,
    },
    {
      metric: 'P/B',
      company: analysis.fundamentals.PB,
      sector: analysis.benchmark.PB,
      signal: analysis.indicators.PB,
    },
    {
      metric: 'ROE',
      company: analysis.fundamentals.ROE,
      sector: analysis.benchmark.ROE,
      signal: analysis.indicators.ROE,
    },
  ];

  const getBarColor = (signal: string) => {
    switch (signal) {
      case 'Undervalued': return 'hsl(var(--bullish))';
      case 'Overvalued': return 'hsl(var(--bearish))';
      case 'N/A': return 'hsl(var(--muted))';
      default: return 'hsl(var(--neutral))';
    }
  };

  const formatValue = (value: number | null, isPercentage: boolean = false): string => {
    if (value === null) return 'N/A';
    return isPercentage ? `${value.toFixed(1)}%` : value.toFixed(2);
  };

  const canCalculatePercentage = (company: number | null, sector: number | null): boolean => {
    return company !== null && sector !== null && (company + sector) > 0;
  };

  return (
    <div className="financial-card">
      <div className="mb-6">
        <h3 className="text-xl font-bold text-foreground mb-2">
          Sector Comparison
        </h3>
        <p className="text-muted-foreground">
          {analysis.ticker} vs {analysis.sector} sector average
        </p>
      </div>

      <div className="space-y-6">
        {chartData.map((item, index) => {
          const canCalculate = canCalculatePercentage(item.company, item.sector);
          const companyPercentage = canCalculate ? (item.company! / (item.company! + item.sector!)) * 100 : 0;
          const sectorPercentage = canCalculate ? 100 - companyPercentage : 0;
          
          return (
            <div key={item.metric} className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="font-medium text-foreground">{item.metric}</span>
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                  item.signal === 'Undervalued' ? 'bg-bullish/20 text-bullish' :
                  item.signal === 'Overvalued' ? 'bg-bearish/20 text-bearish' :
                  item.signal === 'N/A' ? 'bg-muted/20 text-muted-foreground' :
                  'bg-neutral/20 text-neutral-foreground'
                }`}>
                  {item.signal}
                </span>
              </div>
              
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Company:</span>
                  <span className="font-medium text-foreground">
                    {formatValue(item.company, item.metric === 'ROE')}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Sector Avg:</span>
                  <span className="font-medium text-foreground">
                    {formatValue(item.sector, item.metric === 'ROE')}
                  </span>
                </div>
              </div>
              
              {canCalculate ? (
                <div className="relative h-2 bg-surface rounded-full overflow-hidden">
                  <div
                    className="absolute left-0 top-0 h-full rounded-full transition-all duration-500"
                    style={{
                      width: `${companyPercentage}%`,
                      backgroundColor: getBarColor(item.signal),
                    }}
                  />
                  <div
                    className="absolute right-0 top-0 h-full bg-muted rounded-full transition-all duration-500"
                    style={{
                      width: `${sectorPercentage}%`,
                    }}
                  />
                </div>
              ) : (
                <div className="relative h-2 bg-surface rounded-full overflow-hidden">
                  <div className="absolute inset-0 bg-muted rounded-full" />
                  <div className="absolute inset-0 flex items-center justify-center">
                    <span className="text-xs text-muted-foreground">Data not available</span>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};