# BioRoute Builder - Technical Development Specification

## Project Overview

**BioRoute Builder** is a web-based visual platform for designing and analyzing biogas technological routes, inspired by Node-RED's modular approach. The platform enables users to drag-and-drop technology blocks representing different processes (feedstocks, digesters, upgrading, end-use) and automatically calculates mass/energy balances, economic viability, and environmental impacts.

**Target Users:** Researchers, engineers, consultants, and decision-makers in the bioenergy sector.

**Initial Focus:** Sugarcane residues (bagasse, straw, vinasse, filter cake) - expandable to other feedstocks.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React)                         │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Visual      │  │  Results     │  │  Scenario    │          │
│  │  Canvas      │  │  Dashboard   │  │  Manager     │          │
│  │  (React Flow)│  │  (Recharts)  │  │              │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
├─────────────────────────────────────────────────────────────────┤
│                      STATE MANAGEMENT (Zustand)                 │
├─────────────────────────────────────────────────────────────────┤
│                        API LAYER (Axios/TanStack Query)         │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        BACKEND (FastAPI)                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Calculation │  │  Technology  │  │  Scenario    │          │
│  │  Engine      │  │  Database    │  │  Storage     │          │
│  │  (NetworkX)  │  │  API         │  │  API         │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
├─────────────────────────────────────────────────────────────────┤
│                        DATABASE (PostgreSQL)                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

### Frontend
- **Framework:** React 18 + TypeScript
- **Visual Canvas:** React Flow (https://reactflow.dev/) - node-based graph editor
- **Styling:** Tailwind CSS
- **State Management:** Zustand (lightweight, scalable)
- **Data Fetching:** TanStack Query (React Query)
- **Charts:** Recharts or Plotly.js
- **Icons:** Lucide React
- **Build Tool:** Vite

### Backend
- **Framework:** FastAPI (Python)
- **Graph Processing:** NetworkX (route validation, topological sorting)
- **Calculations:** NumPy, Pandas
- **Database ORM:** SQLAlchemy + Alembic (migrations)
- **Validation:** Pydantic v2
- **Authentication:** JWT (optional, for saved scenarios)

### Database
- **Primary:** PostgreSQL
- **Cache:** Redis (optional, for heavy calculations)

### DevOps
- **Containerization:** Docker + Docker Compose
- **CI/CD:** GitHub Actions
- **Hosting:** Vercel (frontend) + Railway/Render (backend)

---

## Data Models

### 1. Technology Block Schema

```typescript
// Frontend TypeScript
interface TechnologyBlock {
  id: string;
  category: 'feedstock' | 'pretreatment' | 'digester' | 'upgrading' | 'enduse' | 'byproduct';
  name: string;
  nameEN: string;
  description: string;
  icon: string;
  color: string;
  
  // Connection rules
  accepts: string[];      // Input types it can receive
  outputs: string[];      // Output types it produces
  
  // Technical parameters (editable by user)
  parameters: Parameter[];
  
  // Default values for calculations
  defaults: Record<string, number>;
  
  // Data sources/references
  references: string[];
}

interface Parameter {
  key: string;
  label: string;
  unit: string;
  defaultValue: number;
  min: number;
  max: number;
  step: number;
  tooltip: string;
}
```

```python
# Backend Python (Pydantic)
from pydantic import BaseModel
from typing import Literal, Optional
from enum import Enum

class TechCategory(str, Enum):
    FEEDSTOCK = "feedstock"
    PRETREATMENT = "pretreatment"
    DIGESTER = "digester"
    UPGRADING = "upgrading"
    ENDUSE = "enduse"
    BYPRODUCT = "byproduct"

class TechnologyBlock(BaseModel):
    id: str
    category: TechCategory
    name: str
    name_en: str
    description: str
    
    accepts: list[str]
    outputs: list[str]
    
    parameters: list[dict]
    defaults: dict[str, float]
    references: list[str]

class ScenarioNode(BaseModel):
    node_id: str
    tech_id: str
    position: dict[str, float]  # {x, y}
    parameters: dict[str, float]  # User-defined values

class ScenarioEdge(BaseModel):
    source: str
    target: str
    source_handle: Optional[str] = None
    target_handle: Optional[str] = None

class Scenario(BaseModel):
    id: str
    name: str
    description: str
    nodes: list[ScenarioNode]
    edges: list[ScenarioEdge]
    created_at: str
    updated_at: str
    author: Optional[str] = None
```

### 2. Database Schema (PostgreSQL)

```sql
-- Technologies table (reference data)
CREATE TABLE technologies (
    id VARCHAR(50) PRIMARY KEY,
    category VARCHAR(20) NOT NULL,
    name_pt VARCHAR(100) NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    description TEXT,
    accepts JSONB DEFAULT '[]',
    outputs JSONB DEFAULT '[]',
    parameters JSONB DEFAULT '[]',
    defaults JSONB DEFAULT '{}',
    references JSONB DEFAULT '[]',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Scenarios table (user-created routes)
CREATE TABLE scenarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    nodes JSONB NOT NULL,
    edges JSONB NOT NULL,
    results JSONB,  -- Cached calculation results
    share_token VARCHAR(50) UNIQUE,  -- For public sharing
    author_id UUID REFERENCES users(id),
    is_template BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Calculation history (for comparison)
CREATE TABLE calculations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scenario_id UUID REFERENCES scenarios(id),
    input_params JSONB NOT NULL,
    results JSONB NOT NULL,
    calculated_at TIMESTAMP DEFAULT NOW()
);

-- Users (optional, for authentication)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100),
    organization VARCHAR(200),
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## Technology Database (Initial Data)

### Feedstocks

| ID | Name | Unit | Key Parameters |
|----|------|------|----------------|
| `bagasse` | Bagaço de Cana | t/day | LHV: 7.5 MJ/kg, Moisture: 50%, VS: 85% |
| `straw` | Palha de Cana | t/day | LHV: 12.5 MJ/kg, Moisture: 15%, VS: 80% |
| `vinasse` | Vinhaça | m³/day | COD: 25 kg/m³, BOD: 15 kg/m³, pH: 4.5 |
| `filter_cake` | Torta de Filtro | t/day | LHV: 3.2 MJ/kg, Moisture: 75%, VS: 70% |
| `wash_water` | Água de Lavagem | m³/day | COD: 5 kg/m³ |

### Pretreatment

| ID | Name | Efficiency | Energy Use |
|----|------|------------|------------|
| `thermal_hydrolysis` | Hidrólise Térmica | +25% biogas | 0.5 kWh/kg VS |
| `mechanical_prep` | Preparo Mecânico | +15% biogas | 0.3 kWh/t |
| `alkaline_pretreat` | Pré-tratamento Alcalino | +20% biogas | 0.1 kg NaOH/kg VS |

### Digesters

| ID | Name | HRT (days) | OLR (kg VS/m³.d) | Efficiency |
|----|------|------------|------------------|------------|
| `cstr` | CSTR | 20-30 | 2-4 | 60-70% |
| `uasb` | UASB | 0.5-2 | 10-20 | 75-85% |
| `pfr` | PFR (Plug Flow) | 15-25 | 3-5 | 65-75% |
| `ic_reactor` | IC Reactor | 0.2-0.5 | 20-35 | 80-90% |
| `lagoon` | Lagoa Coberta | 30-60 | 0.5-1.5 | 50-60% |

### Upgrading Technologies

| ID | Name | CH₄ Recovery | Energy Use | CH₄ Purity |
|----|------|--------------|------------|------------|
| `psa` | PSA | 98% | 0.25 kWh/Nm³ | 97-99% |
| `membrane` | Membrana | 96% | 0.20 kWh/Nm³ | 95-98% |
| `water_scrubbing` | Water Scrubbing | 95% | 0.30 kWh/Nm³ | 96-98% |
| `amine_scrubbing` | Amine Scrubbing | 99% | 0.15 kWh/Nm³ | 99%+ |
| `cryogenic` | Criogênico | 99% | 0.40 kWh/Nm³ | 99.9% |

### End Use Technologies

| ID | Name | Elec. Eff. | Thermal Eff. | Notes |
|----|------|------------|--------------|-------|
| `ice_cogen` | Motor Ciclo Otto | 38-42% | 40-45% | Most common |
| `gas_turbine` | Turbina a Gás | 30-35% | 45-50% | >5 MW |
| `microturbine` | Microturbina | 25-30% | 50-55% | <500 kW |
| `fuel_cell` | Célula Combustível | 45-55% | 30-35% | SOFC/MCFC |
| `boiler` | Caldeira | - | 85-90% | Thermal only |
| `biomethane_gnv` | Biometano GNV | - | - | R$ 3.50/Nm³ |
| `biomethane_grid` | Injeção na Rede | - | - | R$ 2.80/Nm³ |
| `flare` | Flare | - | - | Emergency only |

### Byproducts

| ID | Name | Value | Application |
|----|------|-------|-------------|
| `digestite_liquid` | Digestato Líquido | N, P, K | Fertigation |
| `digestate_solid` | Digestato Sólido | Organic matter | Soil conditioner |
| `co2_capture` | CO₂ Capturado | Food grade | Beverages, greenhouses |

---

## Calculation Engine

### Core Calculations (Python)

```python
# calculation_engine.py

import networkx as nx
from dataclasses import dataclass
from typing import Dict, List, Optional
import numpy as np

@dataclass
class StreamProperties:
    """Properties of a material/energy stream between nodes"""
    mass_flow: float = 0.0        # kg/h or t/day
    volume_flow: float = 0.0      # m³/h or Nm³/h
    energy_content: float = 0.0   # MJ/h or kW
    methane_content: float = 0.0  # Nm³ CH4/h
    cod: float = 0.0              # kg COD/h
    vs_content: float = 0.0       # kg VS/h
    temperature: float = 35.0     # °C
    pressure: float = 1.0         # bar

class CalculationEngine:
    def __init__(self, tech_database: Dict):
        self.tech_db = tech_database
        self.graph = nx.DiGraph()
        
    def build_graph(self, nodes: List[dict], edges: List[dict]):
        """Build NetworkX graph from scenario nodes and edges"""
        self.graph.clear()
        
        for node in nodes:
            self.graph.add_node(
                node['node_id'],
                tech_id=node['tech_id'],
                parameters=node['parameters']
            )
        
        for edge in edges:
            self.graph.add_edge(edge['source'], edge['target'])
        
        # Validate graph is DAG (no cycles)
        if not nx.is_directed_acyclic_graph(self.graph):
            raise ValueError("Route contains cycles - invalid configuration")
        
        return self.graph
    
    def calculate_route(self, nodes: List[dict], edges: List[dict]) -> Dict:
        """Main calculation function"""
        self.build_graph(nodes, edges)
        
        # Get topological order for calculation sequence
        calc_order = list(nx.topological_sort(self.graph))
        
        # Initialize streams dictionary
        streams: Dict[str, StreamProperties] = {}
        node_results: Dict[str, Dict] = {}
        
        for node_id in calc_order:
            node_data = self.graph.nodes[node_id]
            tech = self.tech_db[node_data['tech_id']]
            params = node_data['parameters']
            
            # Get incoming streams
            predecessors = list(self.graph.predecessors(node_id))
            input_streams = [streams.get(f"{p}->{node_id}", StreamProperties()) 
                           for p in predecessors]
            
            # Calculate based on technology type
            output_stream, results = self._calculate_node(
                tech, params, input_streams
            )
            
            node_results[node_id] = results
            
            # Propagate to successors
            for successor in self.graph.successors(node_id):
                streams[f"{node_id}->{successor}"] = output_stream
        
        # Aggregate results
        return self._aggregate_results(node_results, streams)
    
    def _calculate_node(
        self, 
        tech: dict, 
        params: dict, 
        inputs: List[StreamProperties]
    ) -> tuple[StreamProperties, dict]:
        """Calculate output for a single node based on its type"""
        
        category = tech['category']
        
        if category == 'feedstock':
            return self._calc_feedstock(tech, params)
        elif category == 'digester':
            return self._calc_digester(tech, params, inputs)
        elif category == 'upgrading':
            return self._calc_upgrading(tech, params, inputs)
        elif category == 'enduse':
            return self._calc_enduse(tech, params, inputs)
        else:
            # Pass-through for unknown types
            return self._sum_inputs(inputs), {}
    
    def _calc_feedstock(self, tech: dict, params: dict) -> tuple:
        """Calculate feedstock properties"""
        quantity = params.get('quantity', 100)  # t/day or m³/day
        
        defaults = tech['defaults']
        
        if tech['id'] in ['vinasse', 'wash_water']:
            # Liquid feedstock
            cod = quantity * defaults.get('cod', 25)  # kg COD/day
            stream = StreamProperties(
                volume_flow=quantity,
                cod=cod,
                vs_content=cod * 0.7  # Approximate VS from COD
            )
        else:
            # Solid feedstock
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
            'vs_available': stream.vs_content,
            'energy_available': stream.energy_content
        }
        
        return stream, results
    
    def _calc_digester(self, tech: dict, params: dict, inputs: List[StreamProperties]) -> tuple:
        """Calculate biogas production from digester"""
        combined = self._sum_inputs(inputs)
        
        efficiency = params.get('efficiency', tech['defaults'].get('efficiency', 0.70))
        
        # Biogas yield: ~0.4 Nm³/kg VS for solid, ~0.35 Nm³ CH4/kg COD for liquid
        if combined.cod > 0:
            # Liquid pathway (COD-based)
            ch4_production = combined.cod * 0.35 * efficiency  # Nm³ CH4/day
            biogas_production = ch4_production / 0.60  # Assuming 60% CH4
        else:
            # Solid pathway (VS-based)
            biogas_production = combined.vs_content * 0.40 * efficiency  # Nm³/day
            ch4_production = biogas_production * 0.60  # 60% CH4
        
        # Energy content of biogas
        energy_output = ch4_production * 35.8  # MJ/Nm³ CH4 (LHV)
        
        stream = StreamProperties(
            volume_flow=biogas_production,
            methane_content=ch4_production,
            energy_content=energy_output
        )
        
        results = {
            'biogas_production': biogas_production,
            'methane_production': ch4_production,
            'conversion_efficiency': efficiency,
            'energy_output_mj': energy_output
        }
        
        return stream, results
    
    def _calc_upgrading(self, tech: dict, params: dict, inputs: List[StreamProperties]) -> tuple:
        """Calculate biomethane production from upgrading"""
        combined = self._sum_inputs(inputs)
        
        defaults = tech['defaults']
        recovery = params.get('recovery', defaults.get('recovery', 0.96))
        energy_use = defaults.get('energy_use', 0.25)  # kWh/Nm³
        
        biomethane = combined.methane_content * recovery
        parasitic_load = combined.volume_flow * energy_use  # kWh/day
        
        stream = StreamProperties(
            volume_flow=biomethane,
            methane_content=biomethane,
            energy_content=biomethane * 35.8  # MJ/day
        )
        
        results = {
            'biomethane_production': biomethane,
            'methane_recovery': recovery * 100,
            'parasitic_energy': parasitic_load,
            'methane_loss': combined.methane_content - biomethane
        }
        
        return stream, results
    
    def _calc_enduse(self, tech: dict, params: dict, inputs: List[StreamProperties]) -> tuple:
        """Calculate energy output and revenue"""
        combined = self._sum_inputs(inputs)
        
        defaults = tech['defaults']
        
        if tech['id'] in ['ice_cogen', 'gas_turbine', 'microturbine', 'fuel_cell']:
            # CHP calculation
            elec_eff = params.get('elec_efficiency', defaults.get('elec_eff', 0.38))
            therm_eff = params.get('therm_efficiency', defaults.get('therm_eff', 0.45))
            
            energy_input = combined.methane_content * 9.97  # kWh/Nm³ CH4
            electricity = energy_input * elec_eff  # kWh/day
            thermal = energy_input * therm_eff  # kWh/day
            
            # Revenue (Brazilian prices)
            elec_price = params.get('elec_price', 350)  # R$/MWh
            revenue = (electricity / 1000) * elec_price  # R$/day
            
            results = {
                'electricity_kwh': electricity,
                'thermal_kwh': thermal,
                'daily_revenue': revenue,
                'annual_revenue': revenue * 330  # 330 operating days
            }
            
        elif tech['id'] in ['biomethane_gnv', 'biomethane_grid']:
            # Biomethane sale
            price = defaults.get('price', 3.50)  # R$/Nm³
            revenue = combined.methane_content * price
            
            results = {
                'biomethane_sold': combined.methane_content,
                'daily_revenue': revenue,
                'annual_revenue': revenue * 330
            }
            
        else:
            # Boiler or other thermal
            therm_eff = defaults.get('therm_eff', 0.85)
            thermal = combined.energy_content * therm_eff / 3.6  # kWh/day
            
            results = {
                'thermal_kwh': thermal
            }
        
        stream = StreamProperties()  # End node, no output
        return stream, results
    
    def _sum_inputs(self, inputs: List[StreamProperties]) -> StreamProperties:
        """Sum multiple input streams"""
        return StreamProperties(
            mass_flow=sum(i.mass_flow for i in inputs),
            volume_flow=sum(i.volume_flow for i in inputs),
            energy_content=sum(i.energy_content for i in inputs),
            methane_content=sum(i.methane_content for i in inputs),
            cod=sum(i.cod for i in inputs),
            vs_content=sum(i.vs_content for i in inputs)
        )
    
    def _aggregate_results(self, node_results: Dict, streams: Dict) -> Dict:
        """Aggregate all node results into summary"""
        
        # Find totals
        total_biogas = sum(
            r.get('biogas_production', 0) 
            for r in node_results.values()
        )
        total_methane = sum(
            r.get('methane_production', 0) 
            for r in node_results.values()
        )
        total_electricity = sum(
            r.get('electricity_kwh', 0) 
            for r in node_results.values()
        )
        total_thermal = sum(
            r.get('thermal_kwh', 0) 
            for r in node_results.values()
        )
        total_revenue = sum(
            r.get('annual_revenue', 0) 
            for r in node_results.values()
        )
        
        # Environmental metrics
        emissions_avoided = total_methane * 0.0019  # tCO2eq/Nm³ CH4 (simplified)
        
        return {
            'summary': {
                'biogas_nm3_day': round(total_biogas, 0),
                'methane_nm3_day': round(total_methane, 0),
                'electricity_mwh_day': round(total_electricity / 1000, 2),
                'thermal_mwh_day': round(total_thermal / 1000, 2),
                'annual_revenue_brl': round(total_revenue, 0),
                'emissions_avoided_tco2_day': round(emissions_avoided, 2)
            },
            'node_details': node_results,
            'streams': {k: vars(v) for k, v in streams.items()}
        }
```

---

## API Endpoints

### FastAPI Routes

```python
# main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uuid

app = FastAPI(title="BioRoute API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Models ---

class NodeInput(BaseModel):
    node_id: str
    tech_id: str
    position: dict
    parameters: dict

class EdgeInput(BaseModel):
    source: str
    target: str

class CalculationRequest(BaseModel):
    nodes: List[NodeInput]
    edges: List[EdgeInput]

class ScenarioCreate(BaseModel):
    name: str
    description: Optional[str] = ""
    nodes: List[NodeInput]
    edges: List[EdgeInput]

# --- Endpoints ---

@app.get("/api/technologies")
async def get_technologies():
    """Get all available technologies"""
    return {"technologies": TECH_DATABASE}

@app.get("/api/technologies/{category}")
async def get_technologies_by_category(category: str):
    """Get technologies by category"""
    filtered = {k: v for k, v in TECH_DATABASE.items() 
                if v['category'] == category}
    return {"technologies": filtered}

@app.post("/api/calculate")
async def calculate_route(request: CalculationRequest):
    """Calculate mass/energy balance for a route"""
    try:
        engine = CalculationEngine(TECH_DATABASE)
        results = engine.calculate_route(
            [n.dict() for n in request.nodes],
            [e.dict() for e in request.edges]
        )
        return {"success": True, "results": results}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/scenarios")
async def create_scenario(scenario: ScenarioCreate):
    """Save a scenario"""
    scenario_id = str(uuid.uuid4())
    share_token = uuid.uuid4().hex[:8]
    # Save to database...
    return {
        "id": scenario_id,
        "share_url": f"/s/{share_token}"
    }

@app.get("/api/scenarios/{scenario_id}")
async def get_scenario(scenario_id: str):
    """Get a saved scenario"""
    # Fetch from database...
    pass

@app.get("/api/scenarios/shared/{share_token}")
async def get_shared_scenario(share_token: str):
    """Get a scenario by share token (public access)"""
    pass

@app.get("/api/templates")
async def get_templates():
    """Get pre-built scenario templates"""
    return {"templates": SCENARIO_TEMPLATES}

@app.post("/api/compare")
async def compare_scenarios(scenario_ids: List[str]):
    """Compare multiple scenarios side by side"""
    pass
```

---

## Frontend Structure

```
src/
├── components/
│   ├── canvas/
│   │   ├── BioRouteCanvas.tsx      # Main React Flow canvas
│   │   ├── TechNode.tsx            # Custom node component
│   │   ├── ConnectionLine.tsx      # Custom edge component
│   │   └── NodeConfigPanel.tsx     # Parameter editing panel
│   ├── palette/
│   │   ├── TechPalette.tsx         # Draggable tech blocks
│   │   └── CategorySection.tsx     # Collapsible category
│   ├── results/
│   │   ├── ResultsDashboard.tsx    # Main results view
│   │   ├── SankeyDiagram.tsx       # Energy flow visualization
│   │   ├── MetricsCards.tsx        # KPI cards
│   │   └── ComparisonTable.tsx     # Side-by-side comparison
│   ├── scenarios/
│   │   ├── ScenarioManager.tsx     # Save/load/share
│   │   ├── TemplateGallery.tsx     # Pre-built templates
│   │   └── ShareDialog.tsx         # Share URL dialog
│   └── common/
│       ├── Header.tsx
│       ├── Tooltip.tsx
│       └── LoadingSpinner.tsx
├── hooks/
│   ├── useCalculation.ts           # API call for calculations
│   ├── useScenarios.ts             # Scenario CRUD
│   └── useTechnologies.ts          # Tech database fetch
├── store/
│   └── useRouteStore.ts            # Zustand store
├── types/
│   └── index.ts                    # TypeScript interfaces
├── utils/
│   ├── graphValidation.ts          # Connection validation
│   └── formatters.ts               # Number formatting
├── api/
│   └── client.ts                   # Axios instance
├── App.tsx
└── main.tsx
```

### Zustand Store

```typescript
// store/useRouteStore.ts

import { create } from 'zustand';
import { Node, Edge } from 'reactflow';

interface RouteState {
  nodes: Node[];
  edges: Edge[];
  selectedNode: string | null;
  results: CalculationResults | null;
  isCalculating: boolean;
  scenarioName: string;
  
  // Actions
  addNode: (node: Node) => void;
  removeNode: (nodeId: string) => void;
  updateNodeParams: (nodeId: string, params: Record<string, number>) => void;
  addEdge: (edge: Edge) => void;
  removeEdge: (edgeId: string) => void;
  setSelectedNode: (nodeId: string | null) => void;
  setResults: (results: CalculationResults) => void;
  resetCanvas: () => void;
  loadScenario: (scenario: Scenario) => void;
}

export const useRouteStore = create<RouteState>((set, get) => ({
  nodes: [],
  edges: [],
  selectedNode: null,
  results: null,
  isCalculating: false,
  scenarioName: 'Novo Cenário',
  
  addNode: (node) => set((state) => ({ 
    nodes: [...state.nodes, node] 
  })),
  
  removeNode: (nodeId) => set((state) => ({
    nodes: state.nodes.filter(n => n.id !== nodeId),
    edges: state.edges.filter(e => e.source !== nodeId && e.target !== nodeId)
  })),
  
  updateNodeParams: (nodeId, params) => set((state) => ({
    nodes: state.nodes.map(n => 
      n.id === nodeId ? { ...n, data: { ...n.data, parameters: params } } : n
    )
  })),
  
  addEdge: (edge) => set((state) => ({ 
    edges: [...state.edges, edge] 
  })),
  
  removeEdge: (edgeId) => set((state) => ({
    edges: state.edges.filter(e => e.id !== edgeId)
  })),
  
  setSelectedNode: (nodeId) => set({ selectedNode: nodeId }),
  
  setResults: (results) => set({ results, isCalculating: false }),
  
  resetCanvas: () => set({ 
    nodes: [], 
    edges: [], 
    results: null, 
    selectedNode: null 
  }),
  
  loadScenario: (scenario) => set({
    nodes: scenario.nodes,
    edges: scenario.edges,
    scenarioName: scenario.name
  })
}));
```

---

## Pre-built Templates (Mock Data)

```typescript
// data/templates.ts

export const SCENARIO_TEMPLATES = [
  {
    id: 'usina-padrao',
    name: 'Usina Padrão - Vinhaça + Cogeração',
    description: 'Configuração típica de usina sucroalcooleira com biodigestão de vinhaça e cogeração',
    nodes: [
      { node_id: 'feed-1', tech_id: 'vinasse', position: { x: 50, y: 100 }, 
        parameters: { quantity: 1000 } },
      { node_id: 'dig-1', tech_id: 'uasb', position: { x: 300, y: 100 }, 
        parameters: { efficiency: 0.80 } },
      { node_id: 'end-1', tech_id: 'ice_cogen', position: { x: 550, y: 100 }, 
        parameters: { elec_efficiency: 0.40, therm_efficiency: 0.45 } }
    ],
    edges: [
      { source: 'feed-1', target: 'dig-1' },
      { source: 'dig-1', target: 'end-1' }
    ]
  },
  {
    id: 'biometano-gnv',
    name: 'Biometano para GNV',
    description: 'Rota para produção de biometano veicular a partir de vinhaça',
    nodes: [
      { node_id: 'feed-1', tech_id: 'vinasse', position: { x: 50, y: 100 }, 
        parameters: { quantity: 2000 } },
      { node_id: 'dig-1', tech_id: 'ic_reactor', position: { x: 250, y: 100 }, 
        parameters: { efficiency: 0.85 } },
      { node_id: 'upg-1', tech_id: 'membrane', position: { x: 450, y: 100 }, 
        parameters: { recovery: 0.96 } },
      { node_id: 'end-1', tech_id: 'biomethane_gnv', position: { x: 650, y: 100 }, 
        parameters: {} }
    ],
    edges: [
      { source: 'feed-1', target: 'dig-1' },
      { source: 'dig-1', target: 'upg-1' },
      { source: 'upg-1', target: 'end-1' }
    ]
  },
  {
    id: 'residuos-combinados',
    name: 'Resíduos Combinados - Máxima Energia',
    description: 'Aproveitamento de múltiplos resíduos: vinhaça + torta de filtro',
    nodes: [
      { node_id: 'feed-1', tech_id: 'vinasse', position: { x: 50, y: 50 }, 
        parameters: { quantity: 1500 } },
      { node_id: 'feed-2', tech_id: 'filter_cake', position: { x: 50, y: 200 }, 
        parameters: { quantity: 50 } },
      { node_id: 'dig-1', tech_id: 'cstr', position: { x: 300, y: 125 }, 
        parameters: { efficiency: 0.70 } },
      { node_id: 'end-1', tech_id: 'ice_cogen', position: { x: 550, y: 125 }, 
        parameters: { elec_efficiency: 0.38, therm_efficiency: 0.45 } }
    ],
    edges: [
      { source: 'feed-1', target: 'dig-1' },
      { source: 'feed-2', target: 'dig-1' },
      { source: 'dig-1', target: 'end-1' }
    ]
  },
  {
    id: 'palha-2g',
    name: 'Palha - Integração 2G',
    description: 'Biodigestão de palha com pré-tratamento para etanol 2G',
    nodes: [
      { node_id: 'feed-1', tech_id: 'straw', position: { x: 50, y: 100 }, 
        parameters: { quantity: 200 } },
      { node_id: 'pre-1', tech_id: 'thermal_hydrolysis', position: { x: 250, y: 100 }, 
        parameters: {} },
      { node_id: 'dig-1', tech_id: 'pfr', position: { x: 450, y: 100 }, 
        parameters: { efficiency: 0.75 } },
      { node_id: 'end-1', tech_id: 'boiler', position: { x: 650, y: 100 }, 
        parameters: { therm_efficiency: 0.85 } }
    ],
    edges: [
      { source: 'feed-1', target: 'pre-1' },
      { source: 'pre-1', target: 'dig-1' },
      { source: 'dig-1', target: 'end-1' }
    ]
  }
];
```

---

## Development Roadmap

### Phase 1: MVP (4-6 weeks)
- [ ] React Flow canvas with drag-drop
- [ ] Basic node types (feedstock, digester, end-use)
- [ ] Simple mass/energy balance calculations
- [ ] Results dashboard with key metrics
- [ ] 3-4 pre-built templates
- [ ] Local storage for scenarios

### Phase 2: Core Features (4-6 weeks)
- [ ] Full technology database (all categories)
- [ ] Connection validation rules
- [ ] Parameter editing panel
- [ ] Economic calculations (CAPEX/OPEX)
- [ ] Scenario comparison (2-way)
- [ ] Share via URL
- [ ] PostgreSQL + FastAPI backend

### Phase 3: Advanced Features (6-8 weeks)
- [ ] Sankey diagram for energy flows
- [ ] Sensitivity analysis
- [ ] Monte Carlo simulation
- [ ] PDF report generation
- [ ] User authentication
- [ ] Collaborative editing
- [ ] LCA integration (emissions calculation)

### Phase 4: Scale & Polish (ongoing)
- [ ] Mobile responsive
- [ ] Internationalization (PT/EN/ES)
- [ ] API for external integrations
- [ ] Plugin system for new technologies
- [ ] Machine learning for optimization suggestions

---

## Getting Started (Local Development)

```bash
# Clone and setup
git clone https://github.com/your-org/bioroute-builder.git
cd bioroute-builder

# Frontend
cd frontend
npm install
npm run dev

# Backend
cd ../backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
uvicorn main:app --reload

# Database (Docker)
docker-compose up -d postgres redis
```

### requirements.txt (Backend)
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
networkx==3.2.1
numpy==1.26.3
pandas==2.1.4
sqlalchemy==2.0.25
alembic==1.13.1
asyncpg==0.29.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
```

### package.json dependencies (Frontend)
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "reactflow": "^11.10.1",
    "zustand": "^4.4.7",
    "@tanstack/react-query": "^5.17.9",
    "axios": "^1.6.5",
    "recharts": "^2.10.3",
    "lucide-react": "^0.303.0",
    "tailwindcss": "^3.4.1"
  },
  "devDependencies": {
    "@types/react": "^18.2.47",
    "typescript": "^5.3.3",
    "vite": "^5.0.11"
  }
}
```

---

## References & Data Sources

1. **PROBIOGÁS** - Projeto Brasil-Alemanha de Fomento ao Aproveitamento Energético de Biogás
2. **CIBiogás** - Centro Internacional de Energias Renováveis
3. **EMBRAPA** - Empresa Brasileira de Pesquisa Agropecuária
4. **EPE** - Empresa de Pesquisa Energética (Balanço Energético Nacional)
5. **CETESB** - Companhia Ambiental do Estado de São Paulo
6. **ABiogás** - Associação Brasileira do Biogás
7. **IEA Bioenergy Task 37** - Energy from Biogas

---

## Contact & Support

For questions about this specification, contact the CP2B research team at UNICAMP/NIPE.

  