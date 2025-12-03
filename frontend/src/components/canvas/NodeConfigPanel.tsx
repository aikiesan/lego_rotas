/**
 * Panel for editing node parameters
 */

import React from 'react';
import { X } from 'lucide-react';
import { useRouteStore } from '../../store/useRouteStore';

const NodeConfigPanel: React.FC = () => {
  const { nodes, selectedNode, setSelectedNode, updateNodeParams, technologies } = useRouteStore();

  const node = nodes.find((n) => n.id === selectedNode);

  if (!node || !selectedNode) {
    return null;
  }

  const tech = technologies[node.data.tech_id];

  if (!tech) {
    return null;
  }

  const handleParamChange = (key: string, value: number) => {
    updateNodeParams(selectedNode, { [key]: value });
  };

  const handleClose = () => {
    setSelectedNode(null);
  };

  return (
    <div className="absolute top-4 right-4 w-80 bg-white rounded-lg shadow-xl border border-gray-200 z-10 max-h-[calc(100vh-2rem)] overflow-y-auto">
      {/* Header */}
      <div
        className="p-4 border-b border-gray-200 flex items-center justify-between"
        style={{
          borderLeftWidth: '4px',
          borderLeftColor: node.data.color,
        }}
      >
        <div className="flex items-center gap-2">
          <span className="text-2xl">{node.data.icon}</span>
          <div>
            <h3 className="font-bold text-gray-900">{node.data.label}</h3>
            <p className="text-xs text-gray-500 capitalize">{node.data.category}</p>
          </div>
        </div>
        <button
          onClick={handleClose}
          className="p-1 hover:bg-gray-100 rounded transition-colors"
        >
          <X className="w-5 h-5 text-gray-500" />
        </button>
      </div>

      {/* Description */}
      <div className="p-4 border-b border-gray-100 bg-gray-50">
        <p className="text-sm text-gray-700">{tech.description}</p>
      </div>

      {/* Parameters */}
      <div className="p-4">
        <h4 className="font-semibold text-sm text-gray-900 mb-3">
          Parâmetros
        </h4>

        {tech.parameters.length === 0 ? (
          <p className="text-sm text-gray-500 italic">
            Esta tecnologia não possui parâmetros configuráveis.
          </p>
        ) : (
          <div className="space-y-4">
            {tech.parameters.map((param) => {
              const currentValue = node.data.parameters[param.key] ?? param.default_value;

              return (
                <div key={param.key} className="space-y-2">
                  <div className="flex justify-between items-center">
                    <label className="text-sm font-medium text-gray-700">
                      {param.label}
                    </label>
                    <span className="text-sm font-semibold text-blue-600">
                      {currentValue} {param.unit}
                    </span>
                  </div>

                  <input
                    type="range"
                    min={param.min}
                    max={param.max}
                    step={param.step}
                    value={currentValue}
                    onChange={(e) => handleParamChange(param.key, parseFloat(e.target.value))}
                    className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-500"
                  />

                  <div className="flex justify-between text-xs text-gray-500">
                    <span>{param.min}</span>
                    <span>{param.max}</span>
                  </div>

                  {param.tooltip && (
                    <p className="text-xs text-gray-500 italic">
                      {param.tooltip}
                    </p>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Default Values Info */}
      {Object.keys(tech.defaults).length > 0 && (
        <div className="p-4 border-t border-gray-100 bg-gray-50">
          <h4 className="font-semibold text-xs text-gray-700 mb-2">
            Valores Padrão
          </h4>
          <div className="grid grid-cols-2 gap-2 text-xs">
            {Object.entries(tech.defaults).slice(0, 6).map(([key, value]) => (
              <div key={key} className="flex flex-col">
                <span className="text-gray-500 capitalize">{key.replace(/_/g, ' ')}</span>
                <span className="font-medium text-gray-900">{value}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default NodeConfigPanel;
