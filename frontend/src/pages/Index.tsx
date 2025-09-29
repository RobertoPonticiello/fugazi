import { useState, useEffect } from 'react';
import { SearchBar } from '@/components/SearchBar';
import { CompanyCard } from '@/components/CompanyCard';
import { BenchmarkChart } from '@/components/BenchmarkChart';
import { SignalIndicator } from '@/components/SignalIndicator';
import AnalystRecommendations from '@/components/AnalystRecommendations';
import { api } from '@/services/api';
import { CompanyFundamentals, AnalysisResult, CompleteAnalysisResult } from '@/types/financial';
import { useToast } from '@/hooks/use-toast';
import { AlertCircle } from 'lucide-react';

const Index = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [company, setCompany] = useState<CompanyFundamentals | null>(null);
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);
  const [completeAnalysis, setCompleteAnalysis] = useState<CompleteAnalysisResult | null>(null);
  const [backendStatus, setBackendStatus] = useState<'connected' | 'disconnected' | 'checking'>('checking');
  const { toast } = useToast();

  // Check backend connection on component mount
  useEffect(() => {
    const checkBackend = async () => {
      try {
        await api.healthCheck();
        setBackendStatus('connected');
      } catch (error) {
        setBackendStatus('disconnected');
      }
    };

    checkBackend();
  }, [toast]);

  const handleSearch = async (ticker: string) => {
    setIsLoading(true);
    setCompany(null);
    setAnalysis(null);
    setCompleteAnalysis(null);
    
    try {
      // Esegui in parallelo: analisi completa + info aziendali per market cap
      const [completeAnalysisData, companyDetails] = await Promise.all([
        api.getCompleteAnalysis(ticker),
        api.getCompany(ticker)
      ]);

      // Componi i dati compatibili con i componenti esistenti, usando market cap reale
      const companyData: CompanyFundamentals = {
        ticker: completeAnalysisData.ticker,
        name: companyDetails.name ?? `${completeAnalysisData.ticker} Inc.`,
        sector: completeAnalysisData.sector,
        marketCap: companyDetails.marketCap ?? null,
        fundamentals: completeAnalysisData.fundamentals
      };
      
      const analysisData: AnalysisResult = {
        ticker: completeAnalysisData.ticker,
        sector: completeAnalysisData.sector,
        fundamentals: completeAnalysisData.fundamentals,
        benchmark: completeAnalysisData.benchmark,
        indicators: completeAnalysisData.indicators,
        score: completeAnalysisData.score,
        finalSignal: completeAnalysisData.finalSignal
      };
      
      setCompany(companyData);
      setAnalysis(analysisData);
      setCompleteAnalysis(completeAnalysisData);
      
      toast({
        title: "Analysis Complete",
        description: `Successfully analyzed ${ticker} against ${companyData.sector} sector.`,
      });
    } catch (error) {
      toast({
        title: "Analysis Failed",
        description: error instanceof Error ? error.message : "Failed to analyze ticker",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-background to-background" />
        <div className="relative container mx-auto px-4 py-16">
          
          <SearchBar onSearch={handleSearch} isLoading={isLoading} />
        </div>
      </div>

      {/* Results Section */}
      {(company || analysis || isLoading) && (
        <div className="container mx-auto px-4 pb-16">
          {isLoading && (
            <div className="max-w-4xl mx-auto">
              <div className="text-center py-12">
                <div className="inline-flex items-center gap-3 px-6 py-3 bg-primary/10 rounded-full">
                  <div className="w-5 h-5 border-2 border-primary border-t-transparent rounded-full animate-spin" />
                  <span className="text-primary font-medium">Analyzing market data...</span>
                </div>
              </div>
            </div>
          )}

          {company && !isLoading && (
            <div className="max-w-4xl mx-auto space-y-8">
              <CompanyCard company={company} />
              
              {analysis && (
                <>
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    <BenchmarkChart analysis={analysis} />
                    <SignalIndicator 
                      signal={analysis.finalSignal} 
                      score={analysis.score} 
                      ticker={analysis.ticker}
                    />
                  </div>
                  
                  {/* Suggerimenti degli Analisti */}
                  {completeAnalysis && (
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                      <AnalystRecommendations 
                        recommendations={completeAnalysis.analyst_recommendations}
                        ticker={completeAnalysis.ticker}
                      />
                      
                      {/* Disclaimer separato per i suggerimenti degli analisti */}
                      <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                        <div className="flex items-start gap-3">
                          <AlertCircle className="w-5 h-5 text-blue-600 mt-0.5" />
                          <div className="space-y-1">
                            <h4 className="font-medium text-blue-900">Analyst Recommendations Disclaimer</h4>
                            <p className="text-sm text-blue-700">
                              {completeAnalysis.disclaimer.analyst_recommendations}
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}
                  
                  {/* Disclaimer generale */}
                  <div className="p-4 bg-muted/10 rounded-lg border border-border">
                    <div className="flex items-start gap-3">
                      <AlertCircle className="w-5 h-5 text-neutral mt-0.5" />
                      <div className="space-y-1">
                        <h4 className="font-medium text-foreground">Investment Disclaimer</h4>
                        <p className="text-sm text-muted-foreground">
                          This analysis is for informational purposes only and should not be considered as investment advice. 
                          Always conduct your own research and consult with a financial advisor before making investment decisions.
                          Past performance does not guarantee future results.
                        </p>
                      </div>
                    </div>
                  </div>
                </>
              )}
            </div>
          )}
        </div>
      )}

      {/* Footer */}
      <footer className="border-t border-border bg-card/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center text-muted-foreground">
            <p>&copy; 2024 Finge Analytics. Built with React & Tailwind CSS.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;