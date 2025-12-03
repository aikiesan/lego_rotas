# BioRoute Builder

A web-based visual platform for designing and analyzing biogas technological routes, inspired by Node-RED's modular approach. Design complete biogas production chains from feedstock to end-use, with automatic mass/energy balance calculations.

## Features

- **Visual Canvas**: Drag-and-drop interface powered by React Flow
- **Technology Database**: 30+ pre-configured technologies including:
  - Feedstocks (vinasse, bagasse, straw, filter cake)
  - Digesters (CSTR, UASB, PFR, IC Reactor, Covered Lagoons)
  - Upgrading (PSA, Membrane, Water Scrubbing, Amine, Cryogenic)
  - End-use (CHP, Gas Turbine, Boiler, Biomethane-CNG, Grid Injection)
- **Automatic Calculations**: Mass and energy balance using NetworkX
- **Real-time Results**: Production metrics, revenue, emissions avoided
- **Pre-built Templates**: 4 typical sugarcane mill configurations
- **Parameter Customization**: Adjust efficiency, capacity, prices

## Tech Stack

### Frontend
- React 18 + TypeScript
- React Flow (visual canvas)
- Zustand (state management)
- TanStack Query (data fetching)
- Tailwind CSS (styling)
- Vite (build tool)

### Backend
- FastAPI (Python)
- NetworkX (graph calculations)
- Pydantic (data validation)
- NumPy/Pandas (calculations)
- PostgreSQL (database - for future phases)

## Project Structure

```
bioroute-builder/
├── backend/
│   ├── app/
│   │   ├── models/         # Pydantic schemas
│   │   ├── routes/         # API endpoints
│   │   └── services/       # Calculation engine
│   ├── data/
│   │   ├── technologies.py # Technology database
│   │   └── templates.py    # Scenario templates
│   ├── main.py            # FastAPI app
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── canvas/    # React Flow canvas
│   │   │   ├── palette/   # Technology palette
│   │   │   ├── results/   # Results dashboard
│   │   │   └── common/    # Header, etc.
│   │   ├── hooks/         # API hooks
│   │   ├── store/         # Zustand store
│   │   ├── types/         # TypeScript types
│   │   ├── utils/         # Utilities
│   │   └── api/           # API client
│   ├── package.json
│   └── vite.config.ts
├── docker-compose.yml
└── README.md
```

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Python 3.10+
- Docker and Docker Compose (optional, for database)

### Installation

#### 1. Clone the repository

```bash
git clone https://github.com/aikiesan/lego_rotas.git
cd lego_rotas
```

#### 2. Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (optional for MVP)
cp .env.example .env
```

#### 3. Setup Frontend

```bash
cd ../frontend

# Install dependencies
npm install

# Create .env file (optional)
cp .env.example .env
```

#### 4. Start the Application

Open two terminal windows:

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python main.py
```

The backend will start at `http://localhost:8000`

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

The frontend will start at `http://localhost:3000`

### Using Docker (Optional)

Start PostgreSQL and Redis:

```bash
docker-compose up -d
```

## Usage

### Creating a Route

1. **Add Technologies**: Click the (+) button next to technologies in the left sidebar
2. **Connect Nodes**: Drag from green output handles to blue input handles
3. **Configure Parameters**: Click on nodes to adjust parameters in the right panel
4. **Calculate**: Click "Calcular" button in the header
5. **View Results**: See results in the bottom dashboard

### Using Templates

Click "Templates" in the header to load pre-built configurations:

- **Usina Padrão**: Vinasse digestion + cogeneration
- **Biometano GNV**: Biomethane production for vehicles
- **Resíduos Combinados**: Multiple feedstocks for maximum energy
- **Palha 2G**: Straw digestion with pretreatment

### Example Results

For 1000 m³/day vinasse → UASB → CHP:
- Biogas: ~17,500 Nm³/day
- Electricity: ~23,000 MWh/year
- Annual Revenue: ~R$ 8,000,000
- Emissions Avoided: ~11,000 t CO₂eq/year

## API Endpoints

### Technologies
- `GET /api/technologies` - Get all technologies
- `GET /api/technologies/{category}` - Get by category
- `GET /api/technologies/detail/{tech_id}` - Get details

### Calculations
- `POST /api/calculate` - Calculate route
- `POST /api/validate` - Validate route structure

### Templates
- `GET /api/templates` - Get all templates
- `GET /api/templates/{template_id}` - Get specific template

### Scenarios
- `POST /api/scenarios` - Save scenario
- `GET /api/scenarios/{scenario_id}` - Get scenario
- `DELETE /api/scenarios/{scenario_id}` - Delete scenario

Full API documentation: `http://localhost:8000/docs`

## Technology Categories

### Feedstocks
- Vinasse (vinhaça): Ethanol distillation effluent
- Sugarcane Bagasse: Fibrous residue from milling
- Sugarcane Straw: Harvest residue
- Filter Cake: Juice filtration residue
- Wash Water: Cane washing effluent

### Digesters
- CSTR: Most common, for solids/paste
- UASB: High-rate, for liquid effluents
- PFR: Horizontal, for high-solids content
- IC Reactor: Very high-rate, up to 35 kg COD/m³·day
- Covered Lagoon: Low-cost, large volumes

### Upgrading
- PSA: Pressure Swing Adsorption (98% recovery)
- Membrane: Selective separation (96% recovery)
- Water Scrubbing: CO₂ absorption in water (95% recovery)
- Amine Scrubbing: Chemical absorption (99% recovery)
- Cryogenic: Low-temperature separation (99% recovery)

### End-Use
- ICE Cogeneration: 40% electrical, 45% thermal efficiency
- Gas Turbine: For large-scale (>5 MW)
- Boiler: Thermal use only (85% efficiency)
- Biomethane-CNG: R$ 3.50/Nm³
- Grid Injection: R$ 2.80/Nm³

## Calculation Methodology

The calculation engine uses:

1. **Graph Theory** (NetworkX): Validates routes and determines calculation order
2. **Mass Balance**: Tracks COD, VS, biogas, biomethane flows
3. **Energy Balance**: Calculates energy content, efficiency, output
4. **Economic Analysis**: Revenue from electricity/biomethane sales
5. **Environmental Metrics**: CO₂eq emissions avoided

### Key Formulas

- **Biogas from Solids**: 0.40 Nm³/kg VS × Efficiency
- **Biogas from Liquids**: 0.35 Nm³ CH₄/kg COD × Efficiency
- **Methane Energy**: 35.8 MJ/Nm³ CH₄ (LHV) or 9.97 kWh/Nm³
- **Emissions Avoided**: 2.75 kg CO₂eq/Nm³ CH₄ used

## Development Roadmap

### Phase 1: MVP ✅
- [x] React Flow canvas with drag-drop
- [x] Technology database (30+ technologies)
- [x] Calculation engine with NetworkX
- [x] Results dashboard
- [x] 4 pre-built templates
- [x] FastAPI backend

### Phase 2: Core Features (Next)
- [ ] Connection validation rules
- [ ] Economic calculations (CAPEX/OPEX)
- [ ] Scenario comparison (side-by-side)
- [ ] Share via URL
- [ ] PostgreSQL persistence
- [ ] Scenario save/load

### Phase 3: Advanced Features
- [ ] Sankey diagram for energy flows
- [ ] Sensitivity analysis
- [ ] Monte Carlo simulation
- [ ] PDF report generation
- [ ] User authentication
- [ ] LCA integration

### Phase 4: Scale & Polish
- [ ] Mobile responsive
- [ ] Internationalization (PT/EN/ES)
- [ ] API for external integrations
- [ ] Plugin system for custom technologies

## Contributing

This project is part of research at UNICAMP/NIPE (Núcleo Interdisciplinar de Planejamento Energético).

## Data Sources

- PROBIOGÁS - German-Brazilian Biogas Project
- CIBiogás - International Center for Renewable Energy
- EMBRAPA - Brazilian Agricultural Research Corporation
- EPE - Energy Research Company (National Energy Balance)
- CETESB - Environmental Agency of São Paulo
- ABiogás - Brazilian Biogas Association
- IEA Bioenergy Task 37

## License

This project is intended for research and educational purposes.

## Contact

For questions about this project, contact the CP2B research team at UNICAMP/NIPE.

---

**BioRoute Builder** - Designing the future of biogas production
