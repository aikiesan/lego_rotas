/**
 * Results Dashboard - displays calculation results
 */

import React from 'react';
import { TrendingUp, Zap, Flame, DollarSign, Leaf } from 'lucide-react';
import { useRouteStore } from '../../store/useRouteStore';
import { formatNumber, formatCurrency, formatEnergy, formatVolume, formatEmissions } from '../../utils/formatters';

const ResultsDashboard: React.FC = () => {
  const { results, isCalculating } = useRouteStore();

  if (isCalculating) {
    return (
      <div className="p-6 bg-white rounded-lg shadow-lg">
        <div className="flex items-center justify-center h-40">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
            <p className="text-gray-600">Calculando...</p>
          </div>
        </div>
      </div>
    );
  }

  if (!results || !results.success) {
    return (
      <div className="p-6 bg-white rounded-lg shadow-lg">
        <div className="text-center text-gray-500">
          <TrendingUp className="w-12 h-12 mx-auto mb-3 text-gray-300" />
          <p className="text-sm">
            Adicione tecnologias e clique em "Calcular" para ver os resultados
          </p>
        </div>
      </div>
    );
  }

  const { summary } = results;

  return (
    <div className="space-y-4">
      {/* Summary Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Biogas/Biomethane Production */}
        {(summary.biogas_nm3_day > 0 || summary.biomethane_nm3_day > 0) && (
          <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg shadow-lg p-4 text-white">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm opacity-90">Biogás/Biometano</span>
              <TrendingUp className="w-5 h-5" />
            </div>
            <div className="text-2xl font-bold">
              {formatVolume(summary.biogas_nm3_day + summary.biomethane_nm3_day)}
            </div>
            <div className="text-xs opacity-75 mt-1">por dia</div>
          </div>
        )}

        {/* Electricity */}
        {summary.electricity_mwh_year > 0 && (
          <div className="bg-gradient-to-br from-yellow-500 to-yellow-600 rounded-lg shadow-lg p-4 text-white">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm opacity-90">Eletricidade</span>
              <Zap className="w-5 h-5" />
            </div>
            <div className="text-2xl font-bold">
              {formatNumber(summary.electricity_mwh_year, 0)} MWh
            </div>
            <div className="text-xs opacity-75 mt-1">por ano</div>
          </div>
        )}

        {/* Thermal Energy */}
        {summary.thermal_kwh_day > 0 && (
          <div className="bg-gradient-to-br from-orange-500 to-orange-600 rounded-lg shadow-lg p-4 text-white">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm opacity-90">Energia Térmica</span>
              <Flame className="w-5 h-5" />
            </div>
            <div className="text-2xl font-bold">
              {formatEnergy(summary.thermal_kwh_day)}
            </div>
            <div className="text-xs opacity-75 mt-1">por dia</div>
          </div>
        )}

        {/* Revenue */}
        {summary.annual_revenue_brl > 0 && (
          <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-lg shadow-lg p-4 text-white">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm opacity-90">Receita Anual</span>
              <DollarSign className="w-5 h-5" />
            </div>
            <div className="text-2xl font-bold">
              {formatCurrency(summary.annual_revenue_brl)}
            </div>
            <div className="text-xs opacity-75 mt-1">por ano</div>
          </div>
        )}

        {/* Emissions Avoided */}
        {summary.emissions_avoided_ton_year > 0 && (
          <div className="bg-gradient-to-br from-emerald-500 to-emerald-600 rounded-lg shadow-lg p-4 text-white">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm opacity-90">Emissões Evitadas</span>
              <Leaf className="w-5 h-5" />
            </div>
            <div className="text-2xl font-bold">
              {formatNumber(summary.emissions_avoided_ton_year, 1)} t
            </div>
            <div className="text-xs opacity-75 mt-1">CO₂eq por ano</div>
          </div>
        )}
      </div>

      {/* Detailed Results Table */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-lg font-bold text-gray-900 mb-4">
          Detalhes por Tecnologia
        </h3>

        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Tecnologia
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Categoria
                </th>
                <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Produção Principal
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {Object.entries(results.node_details).map(([nodeId, details]) => (
                <tr key={nodeId} className="hover:bg-gray-50">
                  <td className="px-4 py-3 text-sm font-medium text-gray-900">
                    {details.tech_name}
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-500 capitalize">
                    {details.category}
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-900 text-right">
                    {details.biogas_nm3_day && (
                      <div>{formatVolume(details.biogas_nm3_day)}/dia</div>
                    )}
                    {details.biomethane_nm3_day && (
                      <div>{formatVolume(details.biomethane_nm3_day)}/dia</div>
                    )}
                    {details.electricity_kwh_day && (
                      <div>{formatEnergy(details.electricity_kwh_day)}/dia</div>
                    )}
                    {details.thermal_kwh_day && (
                      <div>{formatEnergy(details.thermal_kwh_day)}/dia</div>
                    )}
                    {!details.biogas_nm3_day && !details.biomethane_nm3_day &&
                     !details.electricity_kwh_day && !details.thermal_kwh_day && (
                      <span className="text-gray-400">-</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default ResultsDashboard;
