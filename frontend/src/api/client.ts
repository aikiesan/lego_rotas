/**
 * API client for BioRoute Builder backend
 */

import axios from 'axios';
import { CalculationRequest, CalculationResults, TechnologiesResponse, TemplatesResponse } from '../types';

// Create axios instance with base configuration
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 30000 // 30 seconds
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add any auth tokens here in the future
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// API endpoints
export const api = {
  // Technologies
  getTechnologies: async () => {
    const response = await apiClient.get<TechnologiesResponse>('/technologies');
    return response.data;
  },

  getTechnologiesByCategory: async (category: string) => {
    const response = await apiClient.get(`/technologies/${category}`);
    return response.data;
  },

  getTechnologyDetail: async (techId: string) => {
    const response = await apiClient.get(`/technologies/detail/${techId}`);
    return response.data;
  },

  // Calculations
  calculateRoute: async (request: CalculationRequest) => {
    const response = await apiClient.post<CalculationResults>('/calculate', request);
    return response.data;
  },

  validateRoute: async (request: CalculationRequest) => {
    const response = await apiClient.post('/validate', request);
    return response.data;
  },

  // Templates
  getTemplates: async () => {
    const response = await apiClient.get<TemplatesResponse>('/templates');
    return response.data;
  },

  getTemplate: async (templateId: string) => {
    const response = await apiClient.get(`/templates/${templateId}`);
    return response.data;
  },

  // Scenarios
  createScenario: async (scenario: any) => {
    const response = await apiClient.post('/scenarios', scenario);
    return response.data;
  },

  getScenario: async (scenarioId: string) => {
    const response = await apiClient.get(`/scenarios/${scenarioId}`);
    return response.data;
  },

  getSharedScenario: async (shareToken: string) => {
    const response = await apiClient.get(`/scenarios/shared/${shareToken}`);
    return response.data;
  },

  listScenarios: async () => {
    const response = await apiClient.get('/scenarios');
    return response.data;
  },

  deleteScenario: async (scenarioId: string) => {
    const response = await apiClient.delete(`/scenarios/${scenarioId}`);
    return response.data;
  },

  // Comparison
  compareScenarios: async (scenarioIds: string[]) => {
    const response = await apiClient.post('/compare', scenarioIds);
    return response.data;
  }
};

export default apiClient;
