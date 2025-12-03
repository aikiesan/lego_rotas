/**
 * Application Header with actions
 */

import React, { useState } from 'react';
import { Play, RotateCcw, Download, Upload, Save } from 'lucide-react';
import { useRouteStore } from '../../store/useRouteStore';
import { useCalculation, useTemplates } from '../../hooks/useApi';
import { ScenarioNode } from '../../types';

const Header: React.FC = () => {
  const {
    nodes,
    edges,
    resetCanvas,
    setIsCalculating,
    setResults,
    loadScenario,
    scenarioName,
  } = useRouteStore();

  const calculationMutation = useCalculation();
  const { data: templatesData } = useTemplates();
  const [showTemplates, setShowTemplates] = useState(false);

  const handleCalculate = async () => {
    if (nodes.length === 0) {
      alert('Adicione pelo menos uma tecnologia ao canvas');
      return;
    }

    setIsCalculating(true);

    // Convert nodes to scenario format
    const scenarioNodes: ScenarioNode[] = nodes.map((node) => ({
      node_id: node.id,
      tech_id: node.data.tech_id,
      position: node.position,
      parameters: node.data.parameters,
    }));

    const scenarioEdges = edges.map((edge) => ({
      source: edge.source,
      target: edge.target,
    }));

    try {
      const results = await calculationMutation.mutateAsync({
        nodes: scenarioNodes,
        edges: scenarioEdges,
      });

      setResults(results);
    } catch (error: any) {
      console.error('Calculation error:', error);
      alert(`Erro no cálculo: ${error.response?.data?.detail || error.message}`);
      setResults(null);
    } finally {
      setIsCalculating(false);
    }
  };

  const handleReset = () => {
    if (confirm('Limpar o canvas? Esta ação não pode ser desfeita.')) {
      resetCanvas();
    }
  };

  const handleLoadTemplate = (template: any) => {
    loadScenario(template.nodes, template.edges);
    setShowTemplates(false);
  };

  return (
    <header className="bg-white border-b border-gray-200 px-6 py-4">
      <div className="flex items-center justify-between">
        {/* Logo and Title */}
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            BioRoute Builder
          </h1>
          <p className="text-sm text-gray-500">
            {scenarioName}
          </p>
        </div>

        {/* Actions */}
        <div className="flex items-center gap-3">
          {/* Templates Dropdown */}
          <div className="relative">
            <button
              onClick={() => setShowTemplates(!showTemplates)}
              className="flex items-center gap-2 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
            >
              <Upload className="w-4 h-4" />
              Templates
            </button>

            {showTemplates && templatesData && (
              <div className="absolute top-full mt-2 right-0 w-72 bg-white rounded-lg shadow-xl border border-gray-200 z-50">
                <div className="p-2 max-h-96 overflow-y-auto">
                  {templatesData.templates.map((template) => (
                    <button
                      key={template.id}
                      onClick={() => handleLoadTemplate(template)}
                      className="w-full text-left p-3 hover:bg-gray-50 rounded transition-colors"
                    >
                      <div className="font-medium text-sm text-gray-900">
                        {template.name}
                      </div>
                      <div className="text-xs text-gray-500 mt-1">
                        {template.description}
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Reset */}
          <button
            onClick={handleReset}
            className="flex items-center gap-2 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
            title="Limpar canvas"
          >
            <RotateCcw className="w-4 h-4" />
            Limpar
          </button>

          {/* Calculate */}
          <button
            onClick={handleCalculate}
            disabled={nodes.length === 0 || calculationMutation.isPending}
            className="flex items-center gap-2 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-medium"
          >
            <Play className="w-4 h-4" />
            {calculationMutation.isPending ? 'Calculando...' : 'Calcular'}
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;
