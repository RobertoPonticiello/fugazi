import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { AnalystRecommendations as AnalystRecommendationsType } from '@/types/financial';

interface AnalystRecommendationsProps {
  recommendations: AnalystRecommendationsType | null;
  ticker: string;
}

const AnalystRecommendations: React.FC<AnalystRecommendationsProps> = ({ 
  recommendations, 
  ticker 
}) => {
  if (!recommendations) {
    return (
      <Card className="w-full">
        <CardHeader>
          <CardTitle className="text-lg font-semibold text-gray-700">
            Suggerimenti degli Analisti
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-gray-500 text-sm">
            Nessun dato disponibile sui suggerimenti degli analisti per {ticker}
          </p>
        </CardContent>
      </Card>
    );
  }

  const getConsensusColor = (consensus: string) => {
    switch (consensus.toLowerCase()) {
      case 'strong buy':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'buy':
        return 'bg-green-50 text-green-700 border-green-100';
      case 'hold':
        return 'bg-yellow-50 text-yellow-700 border-yellow-100';
      case 'sell':
        return 'bg-red-50 text-red-700 border-red-100';
      case 'strong sell':
        return 'bg-red-100 text-red-800 border-red-200';
      default:
        return 'bg-gray-50 text-gray-700 border-gray-100';
    }
  };

  const getRecommendationColor = (type: string) => {
    switch (type) {
      case 'strong_buy':
        return 'text-green-600';
      case 'buy':
        return 'text-green-500';
      case 'hold':
        return 'text-yellow-500';
      case 'sell':
        return 'text-red-500';
      case 'strong_sell':
        return 'text-red-600';
      default:
        return 'text-gray-500';
    }
  };

  const getRecommendationLabel = (type: string) => {
    switch (type) {
      case 'strong_buy':
        return 'Strong Buy';
      case 'buy':
        return 'Buy';
      case 'hold':
        return 'Hold';
      case 'sell':
        return 'Sell';
      case 'strong_sell':
        return 'Strong Sell';
      default:
        return type;
    }
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="text-lg font-semibold text-gray-700">
          Suggerimenti degli Analisti
        </CardTitle>
        <div className="flex items-center gap-2">
          <Badge 
            variant="outline" 
            className={`${getConsensusColor(recommendations.consensus)} font-medium`}
          >
            {recommendations.consensus}
          </Badge>
          <span className="text-sm text-gray-500">
            {recommendations.total_analysts} analisti
          </span>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Breakdown delle raccomandazioni */}
        <div className="space-y-3">
          <h4 className="text-sm font-medium text-gray-700">Distribuzione delle Raccomandazioni</h4>
          <div className="space-y-2">
            {Object.entries(recommendations.breakdown).map(([type, count]) => (
              <div key={type} className="flex items-center justify-between">
                <span className={`text-sm font-medium ${getRecommendationColor(type)}`}>
                  {getRecommendationLabel(type)}
                </span>
                <div className="flex items-center gap-2">
                  <Progress 
                    value={(count / recommendations.total_analysts) * 100} 
                    className="w-20 h-2"
                  />
                  <span className="text-sm text-gray-600 w-8 text-right">
                    {count}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Percentuali aggregate */}
        <div className="grid grid-cols-3 gap-4 pt-4 border-t">
          <div className="text-center">
            <div className="text-lg font-semibold text-green-600">
              {recommendations.percentages.bullish}%
            </div>
            <div className="text-xs text-gray-500">Bullish</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-semibold text-yellow-600">
              {recommendations.percentages.neutral}%
            </div>
            <div className="text-xs text-gray-500">Neutral</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-semibold text-red-600">
              {recommendations.percentages.bearish}%
            </div>
            <div className="text-xs text-gray-500">Bearish</div>
          </div>
        </div>

        {/* Disclaimer */}
        <div className="pt-4 border-t">
          <p className="text-xs text-gray-500 italic">
            I suggerimenti degli analisti sono forniti come dati informativi separati 
            e non influenzano il sistema di scoring basato su indicatori finanziari fondamentali.
          </p>
        </div>
      </CardContent>
    </Card>
  );
};

export default AnalystRecommendations;
