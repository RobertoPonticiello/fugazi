import { useState, useEffect, useRef } from 'react';
import { Search, TrendingUp, Loader2 } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { api } from '@/services/api';
import { SearchSuggestion } from '@/types/financial';

interface SearchBarProps {
  onSearch: (ticker: string) => void;
  isLoading?: boolean;
}

export const SearchBar = ({ onSearch, isLoading = false }: SearchBarProps) => {
  const [companyName, setCompanyName] = useState('');
  const [suggestions, setSuggestions] = useState<SearchSuggestion[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [isSearching, setIsSearching] = useState(false);
  const [searchError, setSearchError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const suggestionsRef = useRef<HTMLDivElement>(null);

  // Fetch suggestions when user types
  useEffect(() => {
    const fetchSuggestions = async () => {
      if (companyName.trim().length >= 2) {
        try {
          const result = await api.getSearchSuggestions(companyName.trim());
          setSuggestions(result.suggestions);
          setShowSuggestions(true);
          setSearchError(null);
        } catch (error) {
          console.error('Error fetching suggestions:', error);
          setSuggestions([]);
          setShowSuggestions(false);
        }
      } else {
        setSuggestions([]);
        setShowSuggestions(false);
      }
    };

    const timeoutId = setTimeout(fetchSuggestions, 300); // Debounce
    return () => clearTimeout(timeoutId);
  }, [companyName]);

  // Handle click outside to close suggestions
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        suggestionsRef.current &&
        !suggestionsRef.current.contains(event.target as Node) &&
        inputRef.current &&
        !inputRef.current.contains(event.target as Node)
      ) {
        setShowSuggestions(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (companyName.trim()) {
      await searchCompany(companyName.trim());
    }
  };

  const searchCompany = async (name: string) => {
    setIsSearching(true);
    setSearchError(null);
    setShowSuggestions(false);

    try {
      const result = await api.searchCompany(name);
      
      if (result.found && result.ticker) {
        onSearch(result.ticker);
        setCompanyName(result.company_info?.name || name);
      } else {
        setSearchError(result.error || 'Azienda non trovata');
      }
    } catch (error) {
      setSearchError('Errore nella ricerca. Riprova.');
      console.error('Search error:', error);
    } finally {
      setIsSearching(false);
    }
  };

  const handleSuggestionClick = (suggestion: SearchSuggestion) => {
    setCompanyName(suggestion.name);
    setShowSuggestions(false);
    onSearch(suggestion.ticker);
  };

  const popularCompanies = [
    { name: 'Apple Inc.', ticker: 'AAPL' },
    { name: 'Microsoft Corporation', ticker: 'MSFT' },
    { name: 'NVIDIA Corporation', ticker: 'NVDA' },
    { name: 'Alphabet Inc.', ticker: 'GOOGL' },
    { name: 'Amazon.com Inc.', ticker: 'AMZN' },
    { name: 'Tesla Inc.', ticker: 'TSLA' }
  ];

  return (
    <div className="w-full max-w-2xl mx-auto space-y-6">
      <div className="text-center space-y-3">
        <div className="flex items-center justify-center gap-3">
          <TrendingUp className="w-8 h-8 text-primary" />
          <h1 className="text-4xl font-bold bg-gradient-primary bg-clip-text text-transparent">
            Finge Analytics
          </h1>
        </div>
        <p className="text-muted-foreground text-lg">
          Analyze stocks with dynamic sector benchmarking
        </p>
      </div>

      <form onSubmit={handleSubmit} className="relative">
        <div className="relative">
          <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-muted-foreground" />
          <Input
            ref={inputRef}
            type="text"
            placeholder="Enter company name (e.g., Apple, Microsoft)"
            value={companyName}
            onChange={(e) => setCompanyName(e.target.value)}
            onFocus={() => setShowSuggestions(suggestions.length > 0)}
            className="pl-12 pr-24 h-14 text-lg bg-surface border-border rounded-xl
                       focus:ring-2 focus:ring-primary/50 focus:border-primary
                       transition-all duration-200"
          />
          <Button
            type="submit"
            disabled={!companyName.trim() || isLoading || isSearching}
            className="absolute right-2 top-1/2 transform -translate-y-1/2 h-10
                       bg-primary hover:bg-primary/90 text-primary-foreground
                       disabled:opacity-50 disabled:cursor-not-allowed
                       transition-all duration-200"
          >
            {isLoading ? 'Analyzing...' : isSearching ? 'Searching...' : 'Analyze'}
          </Button>
        </div>

        {/* Suggestions Dropdown */}
        {showSuggestions && suggestions.length > 0 && (
          <div
            ref={suggestionsRef}
            className="absolute top-full left-0 right-0 mt-2 bg-surface border border-border
                       rounded-xl shadow-lg z-50 max-h-60 overflow-y-auto"
          >
            {suggestions.map((suggestion, index) => (
              <button
                key={index}
                onClick={() => handleSuggestionClick(suggestion)}
                className="w-full px-4 py-3 text-left hover:bg-accent transition-colors
                           first:rounded-t-xl last:rounded-b-xl border-b border-border last:border-b-0"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-medium text-foreground">{suggestion.name}</div>
                    <div className="text-sm text-muted-foreground">
                      {suggestion.ticker} • {suggestion.exchange} • {suggestion.sector}
                    </div>
                  </div>
                  <div className="text-xs text-muted-foreground bg-accent px-2 py-1 rounded">
                    {suggestion.ticker}
                  </div>
                </div>
              </button>
            ))}
          </div>
        )}

        {/* Search Error */}
        {searchError && (
          <div className="mt-2 p-3 bg-destructive/10 border border-destructive/20 rounded-lg">
            <p className="text-sm text-destructive">{searchError}</p>
          </div>
        )}
      </form>

      <div className="space-y-3">
        <p className="text-sm text-muted-foreground text-center">Popular companies:</p>
        <div className="flex flex-wrap justify-center gap-2">
          {popularCompanies.map((company) => (
            <button
              key={company.ticker}
              onClick={() => {
                setCompanyName(company.name);
                onSearch(company.ticker);
              }}
              disabled={isLoading || isSearching}
              className="px-4 py-2 text-sm bg-surface hover:bg-accent
                         text-foreground border border-border rounded-lg
                         transition-colors duration-200 hover:shadow-soft
                         disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {company.name}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};