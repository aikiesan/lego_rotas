/**
 * Main App Component
 */

import React, { useEffect } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactFlowProvider } from 'reactflow';

import Header from './components/common/Header';
import TechPalette from './components/palette/TechPalette';
import BioRouteCanvas from './components/canvas/BioRouteCanvas';
import NodeConfigPanel from './components/canvas/NodeConfigPanel';
import ResultsDashboard from './components/results/ResultsDashboard';

import { useRouteStore } from './store/useRouteStore';
import { useTechnologies } from './hooks/useApi';

// Create QueryClient instance
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

const AppContent: React.FC = () => {
  const { setTechnologies } = useRouteStore();
  const { data: techData, isLoading, error } = useTechnologies();

  // Load technologies into store when fetched
  useEffect(() => {
    if (techData?.technologies) {
      setTechnologies(techData.technologies);
    }
  }, [techData, setTechnologies]);

  if (isLoading) {
    return (
      <div className="h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-600 font-medium">Carregando BioRoute Builder...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center text-red-600">
          <p className="text-xl font-bold mb-2">Erro ao carregar aplicação</p>
          <p className="text-sm">Verifique se o backend está rodando</p>
          <p className="text-xs text-gray-500 mt-2">
            {error instanceof Error ? error.message : 'Erro desconhecido'}
          </p>
        </div>
      </div>
    );
  }

  return (
    <ReactFlowProvider>
      <div className="h-screen flex flex-col bg-gray-50">
        {/* Header */}
        <Header />

        {/* Main Content Area */}
        <div className="flex-1 flex overflow-hidden">
          {/* Technology Palette */}
          <TechPalette technologies={techData?.technologies || {}} />

          {/* Canvas and Results */}
          <div className="flex-1 flex flex-col overflow-hidden">
            {/* Canvas Area */}
            <div className="flex-1 relative">
              <BioRouteCanvas />
              <NodeConfigPanel />
            </div>

            {/* Results Area */}
            <div className="h-80 border-t border-gray-200 overflow-y-auto bg-gray-50 p-4">
              <ResultsDashboard />
            </div>
          </div>
        </div>
      </div>
    </ReactFlowProvider>
  );
};

const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <AppContent />
    </QueryClientProvider>
  );
};

export default App;
