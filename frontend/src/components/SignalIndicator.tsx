import { TrendingUp, TrendingDown, Minus, Target } from 'lucide-react';
import { SignalType } from '@/types/financial';

interface SignalIndicatorProps {
  signal: SignalType;
  score: number;
  ticker: string;
}

export const SignalIndicator = ({ signal, score, ticker }: SignalIndicatorProps) => {
  const getSignalConfig = (signal: SignalType) => {
    switch (signal) {
      case 'Undervalued':
        return {
          icon: TrendingUp,
          bgClass: 'signal-bullish',
          textClass: 'text-bullish-foreground',
          description: 'Strong buy signal - potentially undervalued relative to sector',
          recommendation: 'BUY'
        };
      case 'Overvalued':
        return {
          icon: TrendingDown,
          bgClass: 'signal-bearish',
          textClass: 'text-bearish-foreground',
          description: 'Caution signal - potentially overvalued relative to sector',
          recommendation: 'SELL'
        };
      default:
        return {
          icon: Minus,
          bgClass: 'signal-neutral',
          textClass: 'text-neutral-foreground',
          description: 'Neutral signal - fairly valued relative to sector',
          recommendation: 'HOLD'
        };
    }
  };

  const config = getSignalConfig(signal);
  const Icon = config.icon;
  
  const getScoreColor = (score: number) => {
    if (score >= 0.2) return 'text-bullish';
    if (score <= -0.2) return 'text-bearish';
    return 'text-neutral';
  };

  return (
    <div className="financial-card">
      <div className="flex items-center gap-3 mb-6">
        <Target className="w-6 h-6 text-primary" />
        <h3 className="text-xl font-bold text-foreground">Investment Signal</h3>
      </div>

      <div className="space-y-6">
        {/* Main Signal */}
        <div className={`p-6 rounded-xl ${config.bgClass} text-center`}>
          <div className="flex items-center justify-center gap-3 mb-3">
            <Icon className={`w-8 h-8 ${config.textClass}`} />
            <span className={`text-3xl font-bold ${config.textClass}`}>
              {signal.toUpperCase()}
            </span>
          </div>
          <div className={`text-lg font-semibold ${config.textClass} mb-2`}>
            {config.recommendation}
          </div>
          <p className={`${config.textClass} opacity-90`}>
            {config.description}
          </p>
        </div>

        {/* Score Details */}
        <div className="grid grid-cols-2 gap-4">
          <div className="text-center p-4 bg-surface rounded-lg border border-border">
            <div className="text-sm text-muted-foreground mb-1">Composite Score</div>
            <div className={`text-2xl font-bold ${getScoreColor(score)}`}>
              {score > 0 ? '+' : ''}{score.toFixed(3)}
            </div>
          </div>
          <div className="text-center p-4 bg-surface rounded-lg border border-border">
            <div className="text-sm text-muted-foreground mb-1">Ticker</div>
            <div className="text-2xl font-bold text-foreground">{ticker}</div>
          </div>
        </div>

        {/* Score Explanation */}
        <div className="p-4 bg-muted/10 rounded-lg border border-border">
          <h4 className="font-semibold text-foreground mb-2">Scoring Methodology</h4>
          <div className="text-sm text-muted-foreground space-y-1">
            <p>• Score ≥ +0.2: <span className="text-bullish font-medium">Undervalued</span></p>
            <p>• Score -0.2 to +0.2: <span className="text-neutral font-medium">Fairly valued</span></p>
            <p>• Score ≤ -0.2: <span className="text-bearish font-medium">Overvalued</span></p>
          </div>
        </div>
      </div>
    </div>
  );
};