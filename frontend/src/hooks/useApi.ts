import { useState, useEffect } from 'react';
import { api } from '@/services/api';
import { CompanyFundamentals, SectorBenchmark, AnalysisResult } from '@/types/financial';

interface ApiState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
}

export function useApi() {
  const [health, setHealth] = useState<ApiState<{ status: string; api_key_valid: string }>>({
    data: null,
    loading: false,
    error: null
  });

  const checkHealth = async () => {
    setHealth(prev => ({ ...prev, loading: true, error: null }));
    try {
      const data = await api.healthCheck();
      setHealth({ data, loading: false, error: null });
    } catch (error) {
      setHealth({ 
        data: null, 
        loading: false, 
        error: error instanceof Error ? error.message : 'Unknown error' 
      });
    }
  };

  const useCompany = (ticker: string | null) => {
    const [state, setState] = useState<ApiState<CompanyFundamentals>>({
      data: null,
      loading: false,
      error: null
    });

    useEffect(() => {
      if (!ticker) return;

      setState(prev => ({ ...prev, loading: true, error: null }));
      api.getCompany(ticker)
        .then(data => setState({ data, loading: false, error: null }))
        .catch(error => setState({ 
          data: null, 
          loading: false, 
          error: error instanceof Error ? error.message : 'Unknown error' 
        }));
    }, [ticker]);

    return state;
  };

  const useSectorBenchmark = (sector: string | null) => {
    const [state, setState] = useState<ApiState<SectorBenchmark>>({
      data: null,
      loading: false,
      error: null
    });

    useEffect(() => {
      if (!sector) return;

      setState(prev => ({ ...prev, loading: true, error: null }));
      api.getSectorBenchmark(sector)
        .then(data => setState({ data, loading: false, error: null }))
        .catch(error => setState({ 
          data: null, 
          loading: false, 
          error: error instanceof Error ? error.message : 'Unknown error' 
        }));
    }, [sector]);

    return state;
  };

  const useAnalysis = (ticker: string | null) => {
    const [state, setState] = useState<ApiState<AnalysisResult>>({
      data: null,
      loading: false,
      error: null
    });

    useEffect(() => {
      if (!ticker) return;

      setState(prev => ({ ...prev, loading: true, error: null }));
      api.getAnalysis(ticker)
        .then(data => setState({ data, loading: false, error: null }))
        .catch(error => setState({ 
          data: null, 
          loading: false, 
          error: error instanceof Error ? error.message : 'Unknown error' 
        }));
    }, [ticker]);

    return state;
  };

  return {
    health,
    checkHealth,
    useCompany,
    useSectorBenchmark,
    useAnalysis
  };
}
