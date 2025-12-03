/**
 * Utility functions for formatting numbers and values
 */

/**
 * Format number with thousands separator
 */
export function formatNumber(value: number, decimals: number = 0): string {
  return new Intl.NumberFormat('pt-BR', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(value);
}

/**
 * Format currency in Brazilian Reais
 */
export function formatCurrency(value: number): string {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  }).format(value);
}

/**
 * Format energy value with unit
 */
export function formatEnergy(kwh: number): string {
  if (kwh >= 1000) {
    return `${formatNumber(kwh / 1000, 1)} MWh`;
  }
  return `${formatNumber(kwh, 0)} kWh`;
}

/**
 * Format volume with unit
 */
export function formatVolume(nm3: number): string {
  if (nm3 >= 1000) {
    return `${formatNumber(nm3 / 1000, 1)} mil Nm³`;
  }
  return `${formatNumber(nm3, 0)} Nm³`;
}

/**
 * Format percentage
 */
export function formatPercent(value: number, decimals: number = 1): string {
  return `${formatNumber(value, decimals)}%`;
}

/**
 * Shorten large numbers
 */
export function formatCompact(value: number): string {
  if (value >= 1000000) {
    return `${formatNumber(value / 1000000, 1)}M`;
  }
  if (value >= 1000) {
    return `${formatNumber(value / 1000, 1)}k`;
  }
  return formatNumber(value, 0);
}

/**
 * Format CO2 emissions
 */
export function formatEmissions(kg: number): string {
  if (kg >= 1000) {
    return `${formatNumber(kg / 1000, 1)} t CO₂eq`;
  }
  return `${formatNumber(kg, 0)} kg CO₂eq`;
}

/**
 * Combine class names (utility for Tailwind)
 */
export function cn(...classes: (string | undefined | null | false)[]): string {
  return classes.filter(Boolean).join(' ');
}
