/**
 * Technology Palette - Draggable technology blocks sidebar
 */

import React, { useState } from 'react';
import { ChevronDown, ChevronRight, Plus } from 'lucide-react';
import { TechnologyBlock, TechCategory } from '../../types';
import { useRouteStore } from '../../store/useRouteStore';

interface TechPaletteProps {
  technologies: Record<string, TechnologyBlock>;
}

const CATEGORY_LABELS: Record<TechCategory, string> = {
  feedstock: 'Matéria-Prima',
  pretreatment: 'Pré-tratamento',
  digester: 'Biodigestor',
  upgrading: 'Upgrading',
  enduse: 'Uso Final',
  byproduct: 'Subprodutos',
};

const CATEGORY_ORDER: TechCategory[] = [
  'feedstock',
  'pretreatment',
  'digester',
  'upgrading',
  'enduse',
  'byproduct',
];

const TechPalette: React.FC<TechPaletteProps> = ({ technologies }) => {
  const { addNode, nodes } = useRouteStore();
  const [expandedCategories, setExpandedCategories] = useState<Set<TechCategory>>(
    new Set(['feedstock', 'digester', 'enduse'])
  );

  const toggleCategory = (category: TechCategory) => {
    const newExpanded = new Set(expandedCategories);
    if (newExpanded.has(category)) {
      newExpanded.delete(category);
    } else {
      newExpanded.add(category);
    }
    setExpandedCategories(newExpanded);
  };

  const handleAddTechnology = (tech: TechnologyBlock) => {
    const nodeId = `node-${Date.now()}`;

    // Calculate position (stagger new nodes)
    const baseX = 100;
    const baseY = 100 + (nodes.length * 30);

    // Get default parameters
    const defaultParams: Record<string, number> = {};
    tech.parameters.forEach((param) => {
      defaultParams[param.key] = param.default_value;
    });

    addNode({
      id: nodeId,
      type: 'techNode',
      position: { x: baseX, y: baseY },
      data: {
        tech_id: tech.id,
        label: tech.name,
        category: tech.category,
        icon: tech.icon,
        color: tech.color,
        parameters: defaultParams,
      },
    });
  };

  // Group technologies by category
  const techsByCategory: Record<TechCategory, TechnologyBlock[]> = {
    feedstock: [],
    pretreatment: [],
    digester: [],
    upgrading: [],
    enduse: [],
    byproduct: [],
  };

  Object.values(technologies).forEach((tech) => {
    if (tech.category in techsByCategory) {
      techsByCategory[tech.category].push(tech);
    }
  });

  return (
    <div className="w-80 bg-gray-50 border-r border-gray-200 overflow-y-auto h-full">
      <div className="p-4">
        <h2 className="text-lg font-bold text-gray-900 mb-4">
          Tecnologias
        </h2>

        <div className="space-y-2">
          {CATEGORY_ORDER.map((category) => {
            const techs = techsByCategory[category];
            if (techs.length === 0) return null;

            const isExpanded = expandedCategories.has(category);

            return (
              <div key={category} className="bg-white rounded-lg shadow-sm">
                {/* Category Header */}
                <button
                  onClick={() => toggleCategory(category)}
                  className="w-full px-3 py-2 flex items-center justify-between hover:bg-gray-50 transition-colors rounded-lg"
                >
                  <span className="font-semibold text-sm text-gray-700">
                    {CATEGORY_LABELS[category]}
                  </span>
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-gray-500 bg-gray-100 px-2 py-0.5 rounded-full">
                      {techs.length}
                    </span>
                    {isExpanded ? (
                      <ChevronDown className="w-4 h-4 text-gray-500" />
                    ) : (
                      <ChevronRight className="w-4 h-4 text-gray-500" />
                    )}
                  </div>
                </button>

                {/* Technology List */}
                {isExpanded && (
                  <div className="px-2 pb-2 space-y-1">
                    {techs.map((tech) => (
                      <div
                        key={tech.id}
                        className="group relative"
                      >
                        <div
                          className="flex items-center gap-2 p-2 rounded hover:bg-gray-50 cursor-pointer transition-colors"
                          style={{
                            borderLeft: `3px solid ${tech.color}`,
                          }}
                        >
                          <span className="text-xl">{tech.icon}</span>
                          <div className="flex-1 min-w-0">
                            <div className="text-sm font-medium text-gray-900 truncate">
                              {tech.name}
                            </div>
                            <div className="text-xs text-gray-500 truncate">
                              {tech.name_en}
                            </div>
                          </div>

                          {/* Add button */}
                          <button
                            onClick={() => handleAddTechnology(tech)}
                            className="p-1 rounded bg-blue-500 text-white opacity-0 group-hover:opacity-100 transition-opacity hover:bg-blue-600"
                            title="Adicionar ao canvas"
                          >
                            <Plus className="w-4 h-4" />
                          </button>
                        </div>

                        {/* Tooltip on hover */}
                        <div className="hidden group-hover:block absolute left-full ml-2 top-0 z-50 w-64 p-3 bg-gray-900 text-white text-xs rounded-lg shadow-xl">
                          <div className="font-semibold mb-1">{tech.name}</div>
                          <div className="text-gray-300">{tech.description}</div>
                          {tech.parameters.length > 0 && (
                            <div className="mt-2 pt-2 border-t border-gray-700">
                              <div className="text-gray-400">Parâmetros configuráveis:</div>
                              <ul className="mt-1 space-y-0.5">
                                {tech.parameters.slice(0, 3).map((param) => (
                                  <li key={param.key} className="text-gray-300">
                                    • {param.label}
                                  </li>
                                ))}
                              </ul>
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default TechPalette;
