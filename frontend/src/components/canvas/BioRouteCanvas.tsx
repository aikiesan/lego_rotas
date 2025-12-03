/**
 * Main canvas component using React Flow
 */

import React, { useCallback, useMemo } from 'react';
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  BackgroundVariant,
  NodeTypes,
} from 'reactflow';
import 'reactflow/dist/style.css';

import { useRouteStore } from '../../store/useRouteStore';
import TechNode from './TechNode';

const BioRouteCanvas: React.FC = () => {
  const {
    nodes,
    edges,
    onNodesChange,
    onEdgesChange,
    onConnect,
  } = useRouteStore();

  // Define custom node types
  const nodeTypes: NodeTypes = useMemo(
    () => ({
      techNode: TechNode,
    }),
    []
  );

  // Node color function for minimap
  const nodeColor = useCallback((node: any) => {
    return node.data.color || '#999';
  }, []);

  return (
    <div className="w-full h-full bg-gray-50">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        nodeTypes={nodeTypes}
        fitView
        attributionPosition="bottom-right"
        defaultEdgeOptions={{
          type: 'smoothstep',
          animated: true,
          style: { stroke: '#93c5fd', strokeWidth: 2 },
        }}
        minZoom={0.1}
        maxZoom={2}
        snapToGrid
        snapGrid={[15, 15]}
      >
        <Background
          variant={BackgroundVariant.Dots}
          gap={20}
          size={1}
          color="#d1d5db"
        />
        <Controls />
        <MiniMap
          nodeColor={nodeColor}
          nodeStrokeWidth={3}
          pannable
          zoomable
          className="bg-white border border-gray-300 rounded"
        />
      </ReactFlow>
    </div>
  );
};

export default BioRouteCanvas;
