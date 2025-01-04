import React from 'react';
import { Building } from 'lucide-react';
import SearchForm from './components/SearchForm';
import ReportView from './components/ReportView';
import AgentInfoForm from './components/AgentInfoForm';
import { searchProperties } from './utils/homeHarvest';
import type { SearchCriteria, Property, AgentInfo } from './types';

export default function App() {
  const [searchResults, setSearchResults] = React.useState<Property[]>([]);
  const [isLoading, setIsLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const [agentInfo, setAgentInfo] = React.useState<AgentInfo>({
    name: 'Craig Harris',
    brokerage: 'Crown Reality',
    phone: '(727) 709-0985',
    email: 'craig@crownroyalty.com'
  });

  const handleSearch = async (criteria: SearchCriteria) => {
    setIsLoading(true);
    setError(null);
    try {
      const properties = await searchProperties(criteria);
      setSearchResults(properties);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred while searching properties');
      setSearchResults([]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <Building className="h-8 w-8 text-blue-600 mr-3" />
              <h1 className="text-2xl font-bold text-gray-900">Real Estate Search</h1>
            </div>
            <AgentInfoForm
              agentInfo={agentInfo}
              onUpdate={setAgentInfo}
            />
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <div className="grid gap-8 md:grid-cols-1">
          <SearchForm onSearch={handleSearch} />
          
          {isLoading && (
            <div className="text-center py-12">
              <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-blue-600 border-t-transparent"></div>
              <p className="mt-2 text-gray-600">Searching properties...</p>
            </div>
          )}

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-md p-4 text-red-700">
              {error}
            </div>
          )}

          {!isLoading && !error && searchResults.length > 0 && (
            <ReportView
              properties={searchResults}
              agentInfo={agentInfo}
            />
          )}

          {!isLoading && !error && searchResults.length === 0 && (
            <div className="text-center py-12 bg-white rounded-lg shadow">
              <p className="text-gray-500">No properties found matching your criteria.</p>
              <p className="text-gray-400 text-sm mt-2">Try adjusting your search parameters.</p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}