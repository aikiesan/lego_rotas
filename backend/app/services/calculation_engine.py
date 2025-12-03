"""
Calculation Engine for BioRoute Builder
Handles mass/energy balance calculations using NetworkX for graph processing
"""

import networkx as nx
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple
import numpy as np


@dataclass
class StreamProperties:
    """Properties of a material/energy stream between nodes"""
    mass_flow: float = 0.0        # kg/day or t/day
    volume_flow: float = 0.0      # m³/day or Nm³/day
    energy_content: float = 0.0   # MJ/day or kWh/day
    methane_content: float = 0.0  # Nm³ CH4/day
    cod: float = 0.0              # kg COD/day
    vs_content: float = 0.0       # kg VS/day
    temperature: float = 35.0     # °C
    pressure: float = 1.0         # bar

    def __add__(self, other):
        """Allow summing of StreamProperties"""
        return StreamProperties(
            mass_flow=self.mass_flow + other.mass_flow,
            volume_flow=self.volume_flow + other.volume_flow,
            energy_content=self.energy_content + other.energy_content,
            methane_content=self.methane_content + other.methane_content,
            cod=self.cod + other.cod,
            vs_content=self.vs_content + other.vs_content,
            temperature=(self.temperature + other.temperature) / 2,  # Average
            pressure=min(self.pressure, other.pressure)  # Minimum pressure
        )


class CalculationEngine:
    def __init__(self, tech_database: Dict):
        self.tech_db = tech_database
        self.graph = nx.DiGraph()

    def build_graph(self, nodes: List[dict], edges: List[dict]):
        """Build NetworkX graph from scenario nodes and edges"""
        self.graph.clear()

        # Add nodes with their technology and parameters
        for node in nodes:
            self.graph.add_node(
                node['node_id'],
                tech_id=node['tech_id'],
                parameters=node.get('parameters', {})
            )

        # Add edges (connections between nodes)
        for edge in edges:
            self.graph.add_edge(edge['source'], edge['target'])

        # Validate graph is DAG (Directed Acyclic Graph - no cycles)
        if not nx.is_directed_acyclic_graph(self.graph):
            raise ValueError("Route contains cycles - invalid configuration")

        return self.graph

    def calculate_route(self, nodes: List[dict], edges: List[dict]) -> Dict:
        """
        Main calculation function
        Processes the graph in topological order and calculates all streams
        """
        self.build_graph(nodes, edges)

        # Get topological order for calculation sequence
        # This ensures we calculate upstream nodes before downstream
        try:
            calc_order = list(nx.topological_sort(self.graph))
        except nx.NetworkXError as e:
            raise ValueError(f"Cannot determine calculation order: {str(e)}")

        # Initialize streams dictionary {edge_key: StreamProperties}
        streams: Dict[str, StreamProperties] = {}
        node_results: Dict[str, Dict] = {}

        # Process each node in topological order
        for node_id in calc_order:
            node_data = self.graph.nodes[node_id]
            tech_id = node_data['tech_id']

            # Check if technology exists
            if tech_id not in self.tech_db:
                raise ValueError(f"Technology '{tech_id}' not found in database")

            tech = self.tech_db[tech_id]
            params = node_data['parameters']

            # Get incoming streams from predecessor nodes
            predecessors = list(self.graph.predecessors(node_id))
            input_streams = [
                streams.get(f"{p}->{node_id}", StreamProperties())
                for p in predecessors
            ]

            # Calculate based on technology type
            output_stream, results = self._calculate_node(
                tech, params, input_streams
            )

            # Store results for this node
            node_results[node_id] = {
                **results,
                'tech_id': tech_id,
                'tech_name': tech['name'],
                'category': tech['category']
            }

            # Propagate output stream to all successor nodes
            for successor in self.graph.successors(node_id):
                streams[f"{node_id}->{successor}"] = output_stream

        # Aggregate all results into summary
        return self._aggregate_results(node_results, streams)

    def _calculate_node(
        self,
        tech: dict,
        params: dict,
        inputs: List[StreamProperties]
    ) -> Tuple[StreamProperties, dict]:
        """Calculate output for a single node based on its technology type"""

        category = tech['category']

        if category == 'feedstock':
            return self._calc_feedstock(tech, params)
        elif category == 'pretreatment':
            return self._calc_pretreatment(tech, params, inputs)
        elif category == 'digester':
            return self._calc_digester(tech, params, inputs)
        elif category == 'upgrading':
            return self._calc_upgrading(tech, params, inputs)
        elif category == 'enduse':
            return self._calc_enduse(tech, params, inputs)
        elif category == 'byproduct':
            return self._calc_byproduct(tech, params, inputs)
        else:
            # Pass-through for unknown types
            return self._sum_inputs(inputs), {}

    def _calc_feedstock(self, tech: dict, params: dict) -> Tuple[StreamProperties, dict]:
        """Calculate feedstock properties"""
        quantity = params.get('quantity', tech['parameters'][0]['default_value'] if tech['parameters'] else 100)

        defaults = tech['defaults']

        if tech['id'] in ['vinasse', 'wash_water']:
            # Liquid feedstock (m³/day)
            cod = quantity * defaults.get('cod', 25)  # kg COD/day
            stream = StreamProperties(
                volume_flow=quantity,
                cod=cod,
                vs_content=cod * 0.7  # Approximate VS from COD
            )
            results = {
                'input_quantity': quantity,
                'input_unit': 'm³/day',
                'cod_total': cod,
                'vs_available': stream.vs_content
            }
        else:
            # Solid feedstock (t/day)
            moisture = defaults.get('moisture', 50) / 100
            vs_fraction = defaults.get('vs', 85) / 100
            lhv = defaults.get('lhv', 7.5)  # MJ/kg

            dry_mass = quantity * (1 - moisture)  # t/day
            vs_mass = dry_mass * vs_fraction * 1000  # kg VS/day
            energy = quantity * 1000 * (1 - moisture) * lhv  # MJ/day

            stream = StreamProperties(
                mass_flow=quantity * 1000,  # kg/day
                vs_content=vs_mass,
                energy_content=energy
            )
            results = {
                'input_quantity': quantity,
                'input_unit': 't/day',
                'dry_mass': dry_mass,
                'vs_available': vs_mass,
                'energy_available_mj': energy
            }

        return stream, results

    def _calc_pretreatment(
        self, tech: dict, params: dict, inputs: List[StreamProperties]
    ) -> Tuple[StreamProperties, dict]:
        """Calculate pretreatment effects"""
        combined = self._sum_inputs(inputs)

        # Pretreatment increases digestibility
        biogas_increase = tech['defaults'].get('biogas_increase', 15) / 100  # Convert % to decimal
        energy_use = tech['defaults'].get('energy_use', 0.3)  # kWh/kg VS or kWh/t

        # Output stream is similar to input, but flag the increased potential
        output_stream = combined
        output_stream.vs_content *= (1 + biogas_increase)  # Effective VS increase

        parasitic_energy = 0
        if tech['id'] == 'thermal_hydrolysis':
            parasitic_energy = combined.vs_content * energy_use  # kWh
        elif tech['id'] == 'mechanical_prep':
            parasitic_energy = (combined.mass_flow / 1000) * energy_use  # kWh

        results = {
            'biogas_increase_percent': biogas_increase * 100,
            'parasitic_energy_kwh': parasitic_energy,
            'effective_vs_output': output_stream.vs_content
        }

        return output_stream, results

    def _calc_digester(
        self, tech: dict, params: dict, inputs: List[StreamProperties]
    ) -> Tuple[StreamProperties, dict]:
        """Calculate biogas production from digester"""
        combined = self._sum_inputs(inputs)

        # Get efficiency from parameters or defaults
        efficiency = params.get('efficiency', tech['defaults'].get('efficiency', 0.70))
        if efficiency > 1:  # If passed as percentage
            efficiency = efficiency / 100

        ch4_content = tech['defaults'].get('ch4_content', 0.60)

        # Biogas yield calculation
        if combined.cod > 0:
            # Liquid pathway (COD-based)
            # Theoretical: 0.35 Nm³ CH4/kg COD removed
            ch4_production = combined.cod * 0.35 * efficiency  # Nm³ CH4/day
            biogas_production = ch4_production / ch4_content  # Total biogas
        else:
            # Solid pathway (VS-based)
            # Theoretical: 0.40 Nm³ biogas/kg VS
            biogas_production = combined.vs_content * 0.40 * efficiency  # Nm³/day
            ch4_production = biogas_production * ch4_content  # Nm³ CH4/day

        # Energy content of methane (LHV)
        energy_output_mj = ch4_production * 35.8  # MJ/day (35.8 MJ/Nm³ CH4)
        energy_output_kwh = energy_output_mj / 3.6  # kWh/day

        # Output stream is biogas
        stream = StreamProperties(
            volume_flow=biogas_production,
            methane_content=ch4_production,
            energy_content=energy_output_mj
        )

        results = {
            'biogas_nm3_day': round(biogas_production, 1),
            'methane_nm3_day': round(ch4_production, 1),
            'methane_content_percent': round(ch4_content * 100, 1),
            'conversion_efficiency': round(efficiency * 100, 1),
            'energy_output_mj_day': round(energy_output_mj, 0),
            'energy_output_kwh_day': round(energy_output_kwh, 0),
            'hrt_days': tech['defaults'].get('hrt', 20),
            'olr': tech['defaults'].get('olr', 3)
        }

        return stream, results

    def _calc_upgrading(
        self, tech: dict, params: dict, inputs: List[StreamProperties]
    ) -> Tuple[StreamProperties, dict]:
        """Calculate biomethane production from upgrading"""
        combined = self._sum_inputs(inputs)

        defaults = tech['defaults']
        recovery = params.get('recovery', defaults.get('recovery', 0.96))
        if recovery > 1:  # If passed as percentage
            recovery = recovery / 100

        energy_use = defaults.get('energy_use', 0.25)  # kWh/Nm³ biogas

        # Biomethane output
        biomethane = combined.methane_content * recovery  # Nm³/day
        ch4_purity = defaults.get('ch4_purity', 0.97)

        # Parasitic energy consumption
        parasitic_load = combined.volume_flow * energy_use  # kWh/day

        # CO2 separated
        co2_flow = combined.volume_flow * (1 - defaults.get('ch4_content', 0.60))  # Nm³/day

        # Output stream is purified biomethane
        stream = StreamProperties(
            volume_flow=biomethane,
            methane_content=biomethane,
            energy_content=biomethane * 35.8  # MJ/day
        )

        results = {
            'biogas_input_nm3_day': round(combined.volume_flow, 1),
            'biomethane_nm3_day': round(biomethane, 1),
            'methane_purity_percent': round(ch4_purity * 100, 1),
            'methane_recovery_percent': round(recovery * 100, 1),
            'methane_loss_nm3_day': round(combined.methane_content - biomethane, 1),
            'parasitic_energy_kwh_day': round(parasitic_load, 0),
            'co2_separated_nm3_day': round(co2_flow, 1)
        }

        return stream, results

    def _calc_enduse(
        self, tech: dict, params: dict, inputs: List[StreamProperties]
    ) -> Tuple[StreamProperties, dict]:
        """Calculate energy output and revenue from end-use technology"""
        combined = self._sum_inputs(inputs)

        defaults = tech['defaults']
        results = {}

        if tech['id'] in ['ice_cogen', 'gas_turbine', 'microturbine', 'fuel_cell']:
            # CHP (Combined Heat and Power) calculation
            elec_eff = params.get('elec_efficiency', defaults.get('elec_eff', 0.38))
            therm_eff = params.get('therm_efficiency', defaults.get('therm_eff', 0.45))

            if elec_eff > 1:  # If passed as percentage
                elec_eff = elec_eff / 100
            if therm_eff > 1:
                therm_eff = therm_eff / 100

            # Energy input from methane (9.97 kWh/Nm³ CH4)
            energy_input_kwh = combined.methane_content * 9.97  # kWh/day

            # Outputs
            electricity_kwh = energy_input_kwh * elec_eff  # kWh/day
            thermal_kwh = energy_input_kwh * therm_eff  # kWh/day

            # Revenue calculation (Brazilian prices)
            elec_price = params.get('elec_price', 350)  # R$/MWh
            daily_revenue = (electricity_kwh / 1000) * elec_price  # R$/day
            annual_revenue = daily_revenue * 330  # 330 operating days/year

            results = {
                'methane_input_nm3_day': round(combined.methane_content, 1),
                'energy_input_kwh_day': round(energy_input_kwh, 0),
                'electricity_kwh_day': round(electricity_kwh, 0),
                'electricity_mwh_year': round(electricity_kwh * 330 / 1000, 0),
                'thermal_kwh_day': round(thermal_kwh, 0),
                'electrical_efficiency_percent': round(elec_eff * 100, 1),
                'thermal_efficiency_percent': round(therm_eff * 100, 1),
                'total_efficiency_percent': round((elec_eff + therm_eff) * 100, 1),
                'daily_revenue_brl': round(daily_revenue, 2),
                'annual_revenue_brl': round(annual_revenue, 0)
            }

        elif tech['id'] in ['biomethane_gnv', 'biomethane_grid']:
            # Biomethane sale
            price = params.get('price', defaults.get('price', 3.50))  # R$/Nm³
            daily_revenue = combined.methane_content * price  # R$/day
            annual_revenue = daily_revenue * 330

            results = {
                'biomethane_nm3_day': round(combined.methane_content, 1),
                'biomethane_nm3_year': round(combined.methane_content * 330, 0),
                'price_per_nm3': price,
                'daily_revenue_brl': round(daily_revenue, 2),
                'annual_revenue_brl': round(annual_revenue, 0)
            }

        elif tech['id'] == 'boiler':
            # Thermal only
            therm_eff = params.get('therm_efficiency', defaults.get('therm_eff', 0.85))
            if therm_eff > 1:
                therm_eff = therm_eff / 100

            thermal_kwh = (combined.energy_content / 3.6) * therm_eff  # kWh/day

            results = {
                'methane_input_nm3_day': round(combined.methane_content, 1),
                'thermal_kwh_day': round(thermal_kwh, 0),
                'thermal_efficiency_percent': round(therm_eff * 100, 1)
            }

        elif tech['id'] == 'flare':
            # Flaring (emergency only)
            destruction_eff = defaults.get('destruction_efficiency', 0.99)
            co2_reduction = combined.methane_content * 21 * destruction_eff  # kg CO2eq avoided

            results = {
                'methane_flared_nm3_day': round(combined.methane_content, 1),
                'destruction_efficiency_percent': round(destruction_eff * 100, 1),
                'co2eq_avoided_kg_day': round(co2_reduction, 0)
            }

        # End-use nodes don't have output streams (terminal nodes)
        stream = StreamProperties()

        return stream, results

    def _calc_byproduct(
        self, tech: dict, params: dict, inputs: List[StreamProperties]
    ) -> Tuple[StreamProperties, dict]:
        """Calculate byproduct values"""
        combined = self._sum_inputs(inputs)
        defaults = tech['defaults']

        results = {
            'tech_name': tech['name'],
            'value_per_unit': defaults.get('value', 0)
        }

        return StreamProperties(), results

    def _sum_inputs(self, inputs: List[StreamProperties]) -> StreamProperties:
        """Sum multiple input streams"""
        if not inputs:
            return StreamProperties()

        result = inputs[0]
        for inp in inputs[1:]:
            result = result + inp

        return result

    def _aggregate_results(self, node_results: Dict, streams: Dict) -> Dict:
        """Aggregate all node results into summary statistics"""

        # Initialize totals
        total_biogas = 0
        total_methane = 0
        total_biomethane = 0
        total_electricity = 0
        total_thermal = 0
        total_revenue = 0

        # Sum up key metrics from all nodes
        for node_id, results in node_results.items():
            total_biogas += results.get('biogas_nm3_day', 0)
            total_methane += results.get('methane_nm3_day', 0)
            total_biomethane += results.get('biomethane_nm3_day', 0)
            total_electricity += results.get('electricity_kwh_day', 0)
            total_thermal += results.get('thermal_kwh_day', 0)
            total_revenue += results.get('annual_revenue_brl', 0)

        # Environmental metrics (simplified)
        # Each Nm³ of CH4 used avoids ~2.75 kg CO2eq (methane GWP + fossil fuel displacement)
        emissions_avoided_daily = (total_methane + total_biomethane) * 2.75  # kg CO2eq/day
        emissions_avoided_annual = emissions_avoided_daily * 330  # tons CO2eq/year

        return {
            'success': True,
            'summary': {
                'biogas_nm3_day': round(total_biogas, 0),
                'methane_nm3_day': round(total_methane, 0),
                'biomethane_nm3_day': round(total_biomethane, 0),
                'electricity_kwh_day': round(total_electricity, 0),
                'electricity_mwh_year': round(total_electricity * 330 / 1000, 0),
                'thermal_kwh_day': round(total_thermal, 0),
                'annual_revenue_brl': round(total_revenue, 0),
                'emissions_avoided_kg_day': round(emissions_avoided_daily, 0),
                'emissions_avoided_ton_year': round(emissions_avoided_annual / 1000, 1)
            },
            'node_details': node_results,
            'streams': {k: asdict(v) for k, v in streams.items()}
        }
