/**
 * Zustand store for BioRoute Builder state management
 */

import { create } from 'zustand';
import { Node, Edge, Connection, addEdge, applyNodeChanges, applyEdgeChanges, NodeChange, EdgeChange } from 'reactflow';
import { TechNodeData, CalculationResults, TechnologyBlock, ScenarioNode } from '../types';

interface RouteState {
  // Canvas state
  nodes: Node<TechNodeData>[];
  edges: Edge[];
  selectedNode: string | null;

  // Calculation state
  results: CalculationResults | null;
  isCalculating: boolean;

  // Scenario state
  scenarioName: string;
  scenarioDescription: string;

  // Technologies database (loaded from API)
  technologies: Record<string, TechnologyBlock>;

  // Actions for nodes
  setNodes: (nodes: Node<TechNodeData>[]) => void;
  onNodesChange: (changes: NodeChange[]) => void;
  addNode: (node: Node<TechNodeData>) => void;
  removeNode: (nodeId: string) => void;
  updateNodeParams: (nodeId: string, params: Record<string, number>) => void;

  // Actions for edges
  setEdges: (edges: Edge[]) => void;
  onEdgesChange: (changes: EdgeChange[]) => void;
  onConnect: (connection: Connection) => void;
  removeEdge: (edgeId: string) => void;

  // Selection
  setSelectedNode: (nodeId: string | null) => void;

  // Calculation
  setResults: (results: CalculationResults | null) => void;
  setIsCalculating: (isCalculating: boolean) => void;

  // Scenario management
  setScenarioName: (name: string) => void;
  setScenarioDescription: (description: string) => void;
  resetCanvas: () => void;
  loadScenario: (nodes: ScenarioNode[], edges: any[]) => void;

  // Technologies
  setTechnologies: (technologies: Record<string, TechnologyBlock>) => void;
}

export const useRouteStore = create<RouteState>((set, get) => ({
  // Initial state
  nodes: [],
  edges: [],
  selectedNode: null,
  results: null,
  isCalculating: false,
  scenarioName: 'Novo Cenário',
  scenarioDescription: '',
  technologies: {},

  // Node actions
  setNodes: (nodes) => set({ nodes }),

  onNodesChange: (changes) => {
    set({
      nodes: applyNodeChanges(changes, get().nodes) as Node<TechNodeData>[]
    });
  },

  addNode: (node) => {
    set((state) => ({
      nodes: [...state.nodes, node]
    }));
  },

  removeNode: (nodeId) => {
    set((state) => ({
      nodes: state.nodes.filter((n) => n.id !== nodeId),
      edges: state.edges.filter((e) => e.source !== nodeId && e.target !== nodeId),
      selectedNode: state.selectedNode === nodeId ? null : state.selectedNode
    }));
  },

  updateNodeParams: (nodeId, params) => {
    set((state) => ({
      nodes: state.nodes.map((node) =>
        node.id === nodeId
          ? {
              ...node,
              data: {
                ...node.data,
                parameters: { ...node.data.parameters, ...params }
              }
            }
          : node
      )
    }));
  },

  // Edge actions
  setEdges: (edges) => set({ edges }),

  onEdgesChange: (changes) => {
    set({
      edges: applyEdgeChanges(changes, get().edges)
    });
  },

  onConnect: (connection) => {
    set((state) => ({
      edges: addEdge(connection, state.edges)
    }));
  },

  removeEdge: (edgeId) => {
    set((state) => ({
      edges: state.edges.filter((e) => e.id !== edgeId)
    }));
  },

  // Selection
  setSelectedNode: (nodeId) => {
    set({ selectedNode: nodeId });

    // Update node visual selection
    set((state) => ({
      nodes: state.nodes.map((node) => ({
        ...node,
        data: {
          ...node.data,
          isSelected: node.id === nodeId
        }
      }))
    }));
  },

  // Calculation
  setResults: (results) => set({ results }),
  setIsCalculating: (isCalculating) => set({ isCalculating }),

  // Scenario
  setScenarioName: (name) => set({ scenarioName: name }),
  setScenarioDescription: (description) => set({ scenarioDescription: description }),

  resetCanvas: () =>
    set({
      nodes: [],
      edges: [],
      results: null,
      selectedNode: null,
      scenarioName: 'Novo Cenário',
      scenarioDescription: ''
    }),

  loadScenario: (scenarioNodes, scenarioEdges) => {
    const { technologies } = get();

    // Convert scenario nodes to React Flow nodes
    const nodes: Node<TechNodeData>[] = scenarioNodes.map((sNode) => {
      const tech = technologies[sNode.tech_id];

      return {
        id: sNode.node_id,
        type: 'techNode',
        position: sNode.position,
        data: {
          tech_id: sNode.tech_id,
          label: tech?.name || sNode.tech_id,
          category: tech?.category || 'feedstock',
          icon: tech?.icon || '📦',
          color: tech?.color || '#999',
          parameters: sNode.parameters
        }
      };
    });

    // Convert scenario edges to React Flow edges
    const edges: Edge[] = scenarioEdges.map((sEdge, idx) => ({
      id: `e${idx}-${sEdge.source}-${sEdge.target}`,
      source: sEdge.source,
      target: sEdge.target,
      type: 'smoothstep',
      animated: true
    }));

    set({ nodes, edges, selectedNode: null });
  },

  // Technologies
  setTechnologies: (technologies) => set({ technologies })
}));
