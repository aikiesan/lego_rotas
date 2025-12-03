/**
 * Custom hooks for API calls using TanStack Query
 */

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../api/client';
import { CalculationRequest } from '../types';

// Technologies hooks
export function useTechnologies() {
  return useQuery({
    queryKey: ['technologies'],
    queryFn: api.getTechnologies,
    staleTime: 1000 * 60 * 60, // 1 hour - technologies don't change often
  });
}

export function useTechnologiesByCategory(category: string) {
  return useQuery({
    queryKey: ['technologies', category],
    queryFn: () => api.getTechnologiesByCategory(category),
    enabled: !!category,
  });
}

// Templates hooks
export function useTemplates() {
  return useQuery({
    queryKey: ['templates'],
    queryFn: api.getTemplates,
    staleTime: 1000 * 60 * 60, // 1 hour
  });
}

export function useTemplate(templateId: string) {
  return useQuery({
    queryKey: ['template', templateId],
    queryFn: () => api.getTemplate(templateId),
    enabled: !!templateId,
  });
}

// Calculation hook
export function useCalculation() {
  return useMutation({
    mutationFn: (request: CalculationRequest) => api.calculateRoute(request),
  });
}

// Validation hook
export function useValidation() {
  return useMutation({
    mutationFn: (request: CalculationRequest) => api.validateRoute(request),
  });
}

// Scenarios hooks
export function useScenarios() {
  return useQuery({
    queryKey: ['scenarios'],
    queryFn: api.listScenarios,
  });
}

export function useScenario(scenarioId: string) {
  return useQuery({
    queryKey: ['scenario', scenarioId],
    queryFn: () => api.getScenario(scenarioId),
    enabled: !!scenarioId,
  });
}

export function useCreateScenario() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: api.createScenario,
    onSuccess: () => {
      // Invalidate scenarios list to refetch
      queryClient.invalidateQueries({ queryKey: ['scenarios'] });
    },
  });
}

export function useDeleteScenario() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (scenarioId: string) => api.deleteScenario(scenarioId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['scenarios'] });
    },
  });
}

// Comparison hook
export function useCompareScenarios() {
  return useMutation({
    mutationFn: (scenarioIds: string[]) => api.compareScenarios(scenarioIds),
  });
}
