/**
 * Custom node component for technology blocks in React Flow
 */

import React, { memo } from 'react';
import { Handle, Position, NodeProps } from 'reactflow';
import { TechNodeData } from '../../types';
import { Trash2 } from 'lucide-react';
import { useRouteStore } from '../../store/useRouteStore';

const TechNode: React.FC<NodeProps<TechNodeData>> = ({ id, data, selected }) => {
  const { setSelectedNode, removeNode } = useRouteStore();

  const handleClick = () => {
    setSelectedNode(id);
  };

  const handleDelete = (e: React.MouseEvent) => {
    e.stopPropagation();
    removeNode(id);
  };

  return (
    <div
      onClick={handleClick}
      className={`
        relative bg-white rounded-lg shadow-lg border-2 transition-all
        ${selected || data.isSelected ? 'border-blue-500 shadow-xl' : 'border-gray-200'}
        hover:shadow-xl cursor-pointer
        min-w-[180px] max-w-[220px]
      `}
      style={{
        borderLeftWidth: '6px',
        borderLeftColor: data.color || '#999',
      }}
    >
      {/* Input Handle (target) */}
      {data.category !== 'feedstock' && (
        <Handle
          type="target"
          position={Position.Left}
          className="w-3 h-3 bg-blue-500 border-2 border-white"
        />
      )}

      {/* Node Content */}
      <div className="p-3">
        {/* Header with icon and label */}
        <div className="flex items-center gap-2 mb-2">
          <span className="text-2xl">{data.icon}</span>
          <div className="flex-1 min-w-0">
            <div className="font-semibold text-sm text-gray-900 truncate">
              {data.label}
            </div>
            <div className="text-xs text-gray-500 capitalize">
              {data.category}
            </div>
          </div>

          {/* Delete button */}
          <button
            onClick={handleDelete}
            className="p-1 hover:bg-red-50 rounded transition-colors"
            title="Remover"
          >
            <Trash2 className="w-4 h-4 text-red-500" />
          </button>
        </div>

        {/* Parameters preview (if any) */}
        {Object.keys(data.parameters || {}).length > 0 && (
          <div className="mt-2 pt-2 border-t border-gray-100">
            <div className="text-xs text-gray-600 space-y-1">
              {Object.entries(data.parameters).slice(0, 2).map(([key, value]) => (
                <div key={key} className="flex justify-between">
                  <span className="truncate mr-2">{key}:</span>
                  <span className="font-medium">{value}</span>
                </div>
              ))}
              {Object.keys(data.parameters).length > 2 && (
                <div className="text-gray-400 italic">
                  +{Object.keys(data.parameters).length - 2} mais...
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Output Handle (source) */}
      {data.category !== 'enduse' && data.category !== 'byproduct' && (
        <Handle
          type="source"
          position={Position.Right}
          className="w-3 h-3 bg-green-500 border-2 border-white"
        />
      )}
    </div>
  );
};

export default memo(TechNode);
