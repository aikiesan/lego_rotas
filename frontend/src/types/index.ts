/**
 * TypeScript type definitions for BioRoute Builder
 */

import { Node, Edge } from 'reactflow';

// Technology Categories
export type TechCategory =
  | 'feedstock'
  | 'pretreatment'
  | 'digester'
  | 'upgrading'
  | 'enduse'
  | 'byproduct';

// Parameter definition for a technology
export interface Parameter {
  key: string;
  label: string;
  unit: string;
  default_value: number;
  min: number;
  max: number;
  step: number;
  tooltip: string;
}

// Technology Block (from database)
export interface TechnologyBlock {
  id: string;
  category: TechCategory;
  name: string;
  name_en: string;
  description: string;
  icon: string;
  color: string;

  accepts: string[];
  outputs: string[];

  parameters: Parameter[];
  defaults: Record<string, number>;
  references: string[];
}

// Custom node data for React Flow
export interface TechNodeData {
  tech_id: string;
  label: string;
  category: TechCategory;
  icon: string;
  color: string;
  parameters: Record<string, number>;
  isSelected?: boolean;
}

// Scenario node (for saving/loading)
export interface ScenarioNode {
  node_id: string;
  tech_id: string;
  position: { x: number; y: number };
  parameters: Record<string, number>;
}

// Scenario edge
export interface ScenarioEdge {
  source: string;
  target: string;
  source_handle?: string;
  target_handle?: string;
}

// Complete scenario
export interface Scenario {
  id: string;
  name: string;
  description: string;
  nodes: ScenarioNode[];
  edges: ScenarioEdge[];
  created_at: string;
  updated_at: string;
  author?: string;
}

// Calculation request
export interface CalculationRequest {
  nodes: ScenarioNode[];
  edges: ScenarioEdge[];
}

// Calculation results summary
export interface CalculationSummary {
  biogas_nm3_day: number;
  methane_nm3_day: number;
  biomethane_nm3_day: number;
  electricity_kwh_day: number;
  electricity_mwh_year: number;
  thermal_kwh_day: number;
  annual_revenue_brl: number;
  emissions_avoided_kg_day: number;
  emissions_avoided_ton_year: number;
}

// Node calculation result details
export interface NodeResult {
  tech_id: string;
  tech_name: string;
  category: TechCategory;
  [key: string]: any;
}

// Stream properties
export interface StreamProperties {
  mass_flow: number;
  volume_flow: number;
  energy_content: number;
  methane_content: number;
  cod: number;
  vs_content: number;
  temperature: number;
  pressure: number;
}

// Complete calculation response
export interface CalculationResults {
  success: boolean;
  summary: CalculationSummary;
  node_details: Record<string, NodeResult>;
  streams: Record<string, StreamProperties>;
}

// Template definition
export interface Template {
  id: string;
  name: string;
  name_en: string;
  description: string;
  description_en: string;
  nodes: ScenarioNode[];
  edges: ScenarioEdge[];
  expected_results?: Record<string, string>;
}

// API Response types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

export interface TechnologiesResponse {
  success: boolean;
  count: number;
  technologies: Record<string, TechnologyBlock>;
}

export interface TemplatesResponse {
  success: boolean;
  count: number;
  templates: Template[];
}

// React Flow types (re-export for convenience)
export type { Node, Edge };
export type TechNode = Node<TechNodeData>;
export type TechEdge = Edge;
