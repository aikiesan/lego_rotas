"""
Pre-built Scenario Templates for BioRoute Builder
Common configurations for sugarcane mills
"""

SCENARIO_TEMPLATES = [
    {
        "id": "usina-padrao",
        "name": "Usina Padrão - Vinhaça + Cogeração",
        "name_en": "Standard Mill - Vinasse + Cogeneration",
        "description": "Configuração típica de usina sucroalcooleira com biodigestão de vinhaça e cogeração",
        "description_en": "Typical sugarcane mill configuration with vinasse digestion and cogeneration",
        "nodes": [
            {
                "node_id": "feed-1",
                "tech_id": "vinasse",
                "position": {"x": 100, "y": 200},
                "parameters": {"quantity": 1000}
            },
            {
                "node_id": "dig-1",
                "tech_id": "uasb",
                "position": {"x": 350, "y": 200},
                "parameters": {"efficiency": 80, "hrt": 1.0}
            },
            {
                "node_id": "end-1",
                "tech_id": "ice_cogen",
                "position": {"x": 600, "y": 200},
                "parameters": {
                    "elec_efficiency": 40,
                    "therm_efficiency": 45,
                    "elec_price": 350
                }
            }
        ],
        "edges": [
            {"source": "feed-1", "target": "dig-1"},
            {"source": "dig-1", "target": "end-1"}
        ],
        "expected_results": {
            "biogas_nm3_day": "~17,500",
            "electricity_mwh_year": "~23,000",
            "annual_revenue_brl": "~8,000,000"
        }
    },
    {
        "id": "biometano-gnv",
        "name": "Biometano para GNV",
        "name_en": "Biomethane for CNG",
        "description": "Rota para produção de biometano veicular a partir de vinhaça",
        "description_en": "Route for vehicle-grade biomethane production from vinasse",
        "nodes": [
            {
                "node_id": "feed-1",
                "tech_id": "vinasse",
                "position": {"x": 80, "y": 200},
                "parameters": {"quantity": 2000}
            },
            {
                "node_id": "dig-1",
                "tech_id": "ic_reactor",
                "position": {"x": 280, "y": 200},
                "parameters": {"efficiency": 85}
            },
            {
                "node_id": "upg-1",
                "tech_id": "membrane",
                "position": {"x": 480, "y": 200},
                "parameters": {"recovery": 96}
            },
            {
                "node_id": "end-1",
                "tech_id": "biomethane_gnv",
                "position": {"x": 680, "y": 200},
                "parameters": {"price": 3.50}
            }
        ],
        "edges": [
            {"source": "feed-1", "target": "dig-1"},
            {"source": "dig-1", "target": "upg-1"},
            {"source": "upg-1", "target": "end-1"}
        ],
        "expected_results": {
            "biomethane_nm3_day": "~23,000",
            "annual_revenue_brl": "~26,500,000"
        }
    },
    {
        "id": "residuos-combinados",
        "name": "Resíduos Combinados - Máxima Energia",
        "name_en": "Combined Residues - Maximum Energy",
        "description": "Aproveitamento de múltiplos resíduos: vinhaça + torta de filtro",
        "description_en": "Multiple residue utilization: vinasse + filter cake",
        "nodes": [
            {
                "node_id": "feed-1",
                "tech_id": "vinasse",
                "position": {"x": 80, "y": 150},
                "parameters": {"quantity": 1500}
            },
            {
                "node_id": "feed-2",
                "tech_id": "filter_cake",
                "position": {"x": 80, "y": 280},
                "parameters": {"quantity": 50}
            },
            {
                "node_id": "dig-1",
                "tech_id": "cstr",
                "position": {"x": 350, "y": 215},
                "parameters": {"efficiency": 70, "hrt": 25}
            },
            {
                "node_id": "end-1",
                "tech_id": "ice_cogen",
                "position": {"x": 600, "y": 215},
                "parameters": {
                    "elec_efficiency": 38,
                    "therm_efficiency": 45,
                    "elec_price": 350
                }
            }
        ],
        "edges": [
            {"source": "feed-1", "target": "dig-1"},
            {"source": "feed-2", "target": "dig-1"},
            {"source": "dig-1", "target": "end-1"}
        ],
        "expected_results": {
            "biogas_nm3_day": "~15,000",
            "electricity_mwh_year": "~18,000",
            "annual_revenue_brl": "~6,300,000"
        }
    },
    {
        "id": "palha-2g",
        "name": "Palha - Integração 2G",
        "name_en": "Straw - 2G Integration",
        "description": "Biodigestão de palha com pré-tratamento para maximizar produção",
        "description_en": "Straw digestion with pretreatment for maximum production",
        "nodes": [
            {
                "node_id": "feed-1",
                "tech_id": "straw",
                "position": {"x": 80, "y": 200},
                "parameters": {"quantity": 200}
            },
            {
                "node_id": "pre-1",
                "tech_id": "thermal_hydrolysis",
                "position": {"x": 250, "y": 200},
                "parameters": {"temperature": 170}
            },
            {
                "node_id": "dig-1",
                "tech_id": "pfr",
                "position": {"x": 450, "y": 200},
                "parameters": {"efficiency": 75}
            },
            {
                "node_id": "end-1",
                "tech_id": "boiler",
                "position": {"x": 650, "y": 200},
                "parameters": {"therm_efficiency": 85}
            }
        ],
        "edges": [
            {"source": "feed-1", "target": "pre-1"},
            {"source": "pre-1", "target": "dig-1"},
            {"source": "dig-1", "target": "end-1"}
        ],
        "expected_results": {
            "biogas_nm3_day": "~7,700",
            "thermal_kwh_day": "~21,000"
        }
    }
]
