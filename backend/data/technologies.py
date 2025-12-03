"""
Technology Database for BioRoute Builder
Complete catalog of biogas technologies with parameters and default values
"""

TECH_DATABASE = {
    # ==================== FEEDSTOCKS ====================
    "bagasse": {
        "id": "bagasse",
        "category": "feedstock",
        "name": "Bagaço de Cana",
        "name_en": "Sugarcane Bagasse",
        "description": "Resíduo fibroso da moagem da cana-de-açúcar, utilizado principalmente para cogeração",
        "icon": "🌾",
        "color": "#C4A04A",
        "accepts": [],
        "outputs": ["solid_biomass"],
        "parameters": [
            {
                "key": "quantity",
                "label": "Quantidade Disponível",
                "unit": "t/dia",
                "default_value": 100,
                "min": 10,
                "max": 5000,
                "step": 10,
                "tooltip": "Quantidade diária de bagaço disponível"
            }
        ],
        "defaults": {
            "lhv": 7.5,  # MJ/kg (Lower Heating Value)
            "moisture": 50,  # %
            "vs": 85,  # % Volatile Solids
            "density": 150  # kg/m³
        },
        "references": [
            "EMBRAPA - Bagaço de Cana-de-Açúcar",
            "EPE - Balanço Energético Nacional"
        ]
    },

    "straw": {
        "id": "straw",
        "category": "feedstock",
        "name": "Palha de Cana",
        "name_en": "Sugarcane Straw",
        "description": "Resíduo da colheita mecanizada, com alto potencial energético",
        "icon": "🌾",
        "color": "#D4B96A",
        "accepts": [],
        "outputs": ["solid_biomass"],
        "parameters": [
            {
                "key": "quantity",
                "label": "Quantidade Disponível",
                "unit": "t/dia",
                "default_value": 150,
                "min": 10,
                "max": 3000,
                "step": 10,
                "tooltip": "Quantidade diária de palha recolhida"
            }
        ],
        "defaults": {
            "lhv": 12.5,  # MJ/kg
            "moisture": 15,  # %
            "vs": 80,  # %
            "density": 100  # kg/m³
        },
        "references": [
            "CTBE - Centro Nacional de Ciência e Tecnologia do Bioetanol"
        ]
    },

    "vinasse": {
        "id": "vinasse",
        "category": "feedstock",
        "name": "Vinhaça",
        "name_en": "Vinasse",
        "description": "Efluente da destilação de etanol, rico em matéria orgânica e nutrientes",
        "icon": "💧",
        "color": "#8B4513",
        "accepts": [],
        "outputs": ["liquid_organic"],
        "parameters": [
            {
                "key": "quantity",
                "label": "Vazão",
                "unit": "m³/dia",
                "default_value": 1000,
                "min": 100,
                "max": 10000,
                "step": 100,
                "tooltip": "Vazão diária de vinhaça"
            }
        ],
        "defaults": {
            "cod": 25,  # kg COD/m³
            "bod": 15,  # kg BOD/m³
            "ph": 4.5,
            "temperature": 80  # °C (saída da destilação)
        },
        "references": [
            "PROBIOGÁS - Manual de Vinhaça",
            "CETESB - Norma P4.231"
        ]
    },

    "filter_cake": {
        "id": "filter_cake",
        "category": "feedstock",
        "name": "Torta de Filtro",
        "name_en": "Filter Cake",
        "description": "Resíduo da filtração do caldo, rico em fósforo e matéria orgânica",
        "icon": "🍰",
        "color": "#654321",
        "accepts": [],
        "outputs": ["solid_biomass"],
        "parameters": [
            {
                "key": "quantity",
                "label": "Quantidade Disponível",
                "unit": "t/dia",
                "default_value": 50,
                "min": 5,
                "max": 500,
                "step": 5,
                "tooltip": "Quantidade diária de torta de filtro"
            }
        ],
        "defaults": {
            "lhv": 3.2,  # MJ/kg
            "moisture": 75,  # %
            "vs": 70,  # %
            "density": 800  # kg/m³
        },
        "references": [
            "EMBRAPA Meio Ambiente"
        ]
    },

    "wash_water": {
        "id": "wash_water",
        "category": "feedstock",
        "name": "Água de Lavagem de Cana",
        "name_en": "Cane Wash Water",
        "description": "Efluente da lavagem da cana antes da moagem",
        "icon": "💧",
        "color": "#87CEEB",
        "accepts": [],
        "outputs": ["liquid_organic"],
        "parameters": [
            {
                "key": "quantity",
                "label": "Vazão",
                "unit": "m³/dia",
                "default_value": 500,
                "min": 50,
                "max": 3000,
                "step": 50,
                "tooltip": "Vazão diária de água de lavagem"
            }
        ],
        "defaults": {
            "cod": 5,  # kg COD/m³
            "bod": 3,  # kg BOD/m³
            "ph": 6.5
        },
        "references": []
    },

    # ==================== PRETREATMENT ====================
    "thermal_hydrolysis": {
        "id": "thermal_hydrolysis",
        "category": "pretreatment",
        "name": "Hidrólise Térmica",
        "name_en": "Thermal Hydrolysis",
        "description": "Pré-tratamento a alta temperatura (160-180°C) para aumentar digestibilidade",
        "icon": "🔥",
        "color": "#FF6347",
        "accepts": ["solid_biomass"],
        "outputs": ["treated_solid"],
        "parameters": [
            {
                "key": "temperature",
                "label": "Temperatura",
                "unit": "°C",
                "default_value": 170,
                "min": 150,
                "max": 190,
                "step": 5,
                "tooltip": "Temperatura do processo de hidrólise"
            }
        ],
        "defaults": {
            "biogas_increase": 25,  # % increase in biogas production
            "energy_use": 0.5,  # kWh/kg VS
            "retention_time": 30  # minutes
        },
        "references": [
            "Cambi THP Technology"
        ]
    },

    "mechanical_prep": {
        "id": "mechanical_prep",
        "category": "pretreatment",
        "name": "Preparo Mecânico",
        "name_en": "Mechanical Preparation",
        "description": "Trituração e homogeneização para aumentar área superficial",
        "icon": "⚙️",
        "color": "#708090",
        "accepts": ["solid_biomass"],
        "outputs": ["treated_solid"],
        "parameters": [],
        "defaults": {
            "biogas_increase": 15,  # %
            "energy_use": 0.3,  # kWh/t
            "particle_size": 2  # mm
        },
        "references": []
    },

    "alkaline_pretreat": {
        "id": "alkaline_pretreat",
        "category": "pretreatment",
        "name": "Pré-tratamento Alcalino",
        "name_en": "Alkaline Pretreatment",
        "description": "Tratamento com NaOH para quebrar lignina e aumentar digestibilidade",
        "icon": "⚗️",
        "color": "#9370DB",
        "accepts": ["solid_biomass"],
        "outputs": ["treated_solid"],
        "parameters": [
            {
                "key": "naoh_dose",
                "label": "Dosagem NaOH",
                "unit": "kg/t",
                "default_value": 10,
                "min": 5,
                "max": 30,
                "step": 1,
                "tooltip": "Quantidade de hidróxido de sódio por tonelada"
            }
        ],
        "defaults": {
            "biogas_increase": 20,  # %
            "energy_use": 0.1,  # kWh/kg VS
            "retention_time": 24  # hours
        },
        "references": []
    },

    # ==================== DIGESTERS ====================
    "cstr": {
        "id": "cstr",
        "category": "digester",
        "name": "CSTR (Reator Contínuo de Mistura Completa)",
        "name_en": "CSTR (Continuous Stirred Tank Reactor)",
        "description": "Reator mais comum, ideal para resíduos sólidos e pastosos",
        "icon": "🏭",
        "color": "#4682B4",
        "accepts": ["solid_biomass", "treated_solid", "liquid_organic"],
        "outputs": ["biogas", "digestate"],
        "parameters": [
            {
                "key": "efficiency",
                "label": "Eficiência de Conversão",
                "unit": "%",
                "default_value": 70,
                "min": 50,
                "max": 80,
                "step": 1,
                "tooltip": "Eficiência de conversão de VS em biogás"
            },
            {
                "key": "hrt",
                "label": "Tempo de Retenção Hidráulica",
                "unit": "dias",
                "default_value": 25,
                "min": 20,
                "max": 30,
                "step": 1,
                "tooltip": "TRH do reator"
            }
        ],
        "defaults": {
            "efficiency": 0.70,
            "hrt": 25,  # days
            "olr": 3.0,  # kg VS/m³.day (Organic Loading Rate)
            "temperature": 35,  # °C (mesophilic)
            "ch4_content": 0.60  # 60% CH4 in biogas
        },
        "references": [
            "CIBiogás - Manual de Biodigestores CSTR"
        ]
    },

    "uasb": {
        "id": "uasb",
        "category": "digester",
        "name": "UASB (Reator Anaeróbio de Manta de Lodo)",
        "name_en": "UASB (Upflow Anaerobic Sludge Blanket)",
        "description": "Ideal para efluentes líquidos de alta carga, como vinhaça",
        "icon": "🏭",
        "color": "#2E8B57",
        "accepts": ["liquid_organic"],
        "outputs": ["biogas", "digestate"],
        "parameters": [
            {
                "key": "efficiency",
                "label": "Eficiência de Conversão",
                "unit": "%",
                "default_value": 80,
                "min": 70,
                "max": 90,
                "step": 1,
                "tooltip": "Eficiência de remoção de DQO"
            },
            {
                "key": "hrt",
                "label": "Tempo de Retenção Hidráulica",
                "unit": "dias",
                "default_value": 1.0,
                "min": 0.5,
                "max": 2.0,
                "step": 0.1,
                "tooltip": "TRH do reator"
            }
        ],
        "defaults": {
            "efficiency": 0.80,
            "hrt": 1.0,  # days
            "olr": 15.0,  # kg COD/m³.day
            "temperature": 35,  # °C
            "ch4_content": 0.65  # 65% CH4
        },
        "references": [
            "PROBIOGÁS - UASB para Vinhaça",
            "Lettinga et al. 1980"
        ]
    },

    "pfr": {
        "id": "pfr",
        "category": "digester",
        "name": "PFR (Plug Flow Reactor)",
        "name_en": "PFR (Plug Flow Reactor)",
        "description": "Reator horizontal para resíduos com alto teor de sólidos (10-15%)",
        "icon": "🏭",
        "color": "#CD853F",
        "accepts": ["solid_biomass", "treated_solid"],
        "outputs": ["biogas", "digestate"],
        "parameters": [
            {
                "key": "efficiency",
                "label": "Eficiência de Conversão",
                "unit": "%",
                "default_value": 70,
                "min": 60,
                "max": 80,
                "step": 1,
                "tooltip": "Eficiência de conversão de VS"
            }
        ],
        "defaults": {
            "efficiency": 0.70,
            "hrt": 20,  # days
            "olr": 4.0,  # kg VS/m³.day
            "temperature": 38,  # °C
            "ch4_content": 0.58
        },
        "references": [
            "GEA Farm Technologies"
        ]
    },

    "ic_reactor": {
        "id": "ic_reactor",
        "category": "digester",
        "name": "IC Reactor (Reator de Circulação Interna)",
        "name_en": "IC Reactor (Internal Circulation)",
        "description": "Reator de alta taxa para efluentes líquidos, até 35 kg COD/m³.dia",
        "icon": "🏭",
        "color": "#1E90FF",
        "accepts": ["liquid_organic"],
        "outputs": ["biogas", "digestate"],
        "parameters": [
            {
                "key": "efficiency",
                "label": "Eficiência de Conversão",
                "unit": "%",
                "default_value": 85,
                "min": 75,
                "max": 95,
                "step": 1,
                "tooltip": "Eficiência de remoção de DQO"
            }
        ],
        "defaults": {
            "efficiency": 0.85,
            "hrt": 0.3,  # days
            "olr": 25.0,  # kg COD/m³.day
            "temperature": 35,
            "ch4_content": 0.70
        },
        "references": [
            "Paques Technology"
        ]
    },

    "lagoon": {
        "id": "lagoon",
        "category": "digester",
        "name": "Lagoa Coberta",
        "name_en": "Covered Lagoon",
        "description": "Solução de baixo custo para grandes volumes, comum em usinas",
        "icon": "🏊",
        "color": "#20B2AA",
        "accepts": ["liquid_organic"],
        "outputs": ["biogas", "digestate"],
        "parameters": [
            {
                "key": "efficiency",
                "label": "Eficiência de Conversão",
                "unit": "%",
                "default_value": 55,
                "min": 40,
                "max": 65,
                "step": 1,
                "tooltip": "Eficiência típica de lagoas"
            }
        ],
        "defaults": {
            "efficiency": 0.55,
            "hrt": 45,  # days
            "olr": 1.0,  # kg COD/m³.day
            "temperature": 25,  # °C (ambient)
            "ch4_content": 0.55
        },
        "references": [
            "CETESB - Lagoas Anaeróbias"
        ]
    },

    # ==================== UPGRADING ====================
    "psa": {
        "id": "psa",
        "category": "upgrading",
        "name": "PSA (Pressure Swing Adsorption)",
        "name_en": "PSA (Pressure Swing Adsorption)",
        "description": "Remoção de CO2 por adsorção em zeólitas ou carvão ativado",
        "icon": "🔬",
        "color": "#FF1493",
        "accepts": ["biogas"],
        "outputs": ["biomethane", "co2"],
        "parameters": [
            {
                "key": "recovery",
                "label": "Recuperação de CH4",
                "unit": "%",
                "default_value": 98,
                "min": 95,
                "max": 99,
                "step": 0.5,
                "tooltip": "Taxa de recuperação de metano"
            }
        ],
        "defaults": {
            "recovery": 0.98,
            "energy_use": 0.25,  # kWh/Nm³
            "ch4_purity": 0.98,  # 98% CH4
            "capex": 1200  # USD/Nm³/h capacity
        },
        "references": [
            "Xebec Adsorption",
            "Guild Associates"
        ]
    },

    "membrane": {
        "id": "membrane",
        "category": "upgrading",
        "name": "Membrana",
        "name_en": "Membrane Separation",
        "description": "Separação seletiva através de membranas poliméricas",
        "icon": "🔬",
        "color": "#FF69B4",
        "accepts": ["biogas"],
        "outputs": ["biomethane", "co2"],
        "parameters": [
            {
                "key": "recovery",
                "label": "Recuperação de CH4",
                "unit": "%",
                "default_value": 96,
                "min": 93,
                "max": 98,
                "step": 0.5,
                "tooltip": "Taxa de recuperação de metano"
            }
        ],
        "defaults": {
            "recovery": 0.96,
            "energy_use": 0.20,  # kWh/Nm³
            "ch4_purity": 0.97,
            "capex": 1000
        },
        "references": [
            "DGE - DMT Environmental"
        ]
    },

    "water_scrubbing": {
        "id": "water_scrubbing",
        "category": "upgrading",
        "name": "Water Scrubbing",
        "name_en": "Water Scrubbing",
        "description": "Absorção de CO2 em água sob pressão",
        "icon": "🔬",
        "color": "#00CED1",
        "accepts": ["biogas"],
        "outputs": ["biomethane", "co2"],
        "parameters": [
            {
                "key": "recovery",
                "label": "Recuperação de CH4",
                "unit": "%",
                "default_value": 95,
                "min": 92,
                "max": 97,
                "step": 0.5,
                "tooltip": "Taxa de recuperação de metano"
            }
        ],
        "defaults": {
            "recovery": 0.95,
            "energy_use": 0.30,  # kWh/Nm³
            "ch4_purity": 0.97,
            "capex": 900
        },
        "references": [
            "Malmberg Water"
        ]
    },

    "amine_scrubbing": {
        "id": "amine_scrubbing",
        "category": "upgrading",
        "name": "Amine Scrubbing",
        "name_en": "Amine Scrubbing",
        "description": "Absorção química de CO2 com aminas (MEA, DEA)",
        "icon": "🔬",
        "color": "#9370DB",
        "accepts": ["biogas"],
        "outputs": ["biomethane", "co2"],
        "parameters": [
            {
                "key": "recovery",
                "label": "Recuperação de CH4",
                "unit": "%",
                "default_value": 99,
                "min": 97,
                "max": 99.5,
                "step": 0.25,
                "tooltip": "Alta recuperação com aminas"
            }
        ],
        "defaults": {
            "recovery": 0.99,
            "energy_use": 0.15,  # kWh/Nm³
            "ch4_purity": 0.995,
            "capex": 1500
        },
        "references": []
    },

    "cryogenic": {
        "id": "cryogenic",
        "category": "upgrading",
        "name": "Criogênico",
        "name_en": "Cryogenic Separation",
        "description": "Separação por condensação a baixas temperaturas (-100°C)",
        "icon": "❄️",
        "color": "#B0E0E6",
        "accepts": ["biogas"],
        "outputs": ["biomethane", "co2_liquid"],
        "parameters": [],
        "defaults": {
            "recovery": 0.99,
            "energy_use": 0.40,  # kWh/Nm³
            "ch4_purity": 0.999,
            "capex": 2000
        },
        "references": []
    },

    # ==================== END USE ====================
    "ice_cogen": {
        "id": "ice_cogen",
        "category": "enduse",
        "name": "Motor Ciclo Otto (Cogeração)",
        "name_en": "ICE Cogeneration",
        "description": "Motor a combustão interna para geração combinada de calor e eletricidade",
        "icon": "⚡",
        "color": "#FFD700",
        "accepts": ["biogas", "biomethane"],
        "outputs": ["electricity", "heat"],
        "parameters": [
            {
                "key": "elec_efficiency",
                "label": "Eficiência Elétrica",
                "unit": "%",
                "default_value": 40,
                "min": 35,
                "max": 43,
                "step": 1,
                "tooltip": "Eficiência de conversão em eletricidade"
            },
            {
                "key": "therm_efficiency",
                "label": "Eficiência Térmica",
                "unit": "%",
                "default_value": 45,
                "min": 40,
                "max": 50,
                "step": 1,
                "tooltip": "Eficiência de recuperação de calor"
            },
            {
                "key": "elec_price",
                "label": "Preço da Eletricidade",
                "unit": "R$/MWh",
                "default_value": 350,
                "min": 200,
                "max": 600,
                "step": 10,
                "tooltip": "Preço de venda ou economia"
            }
        ],
        "defaults": {
            "elec_eff": 0.40,
            "therm_eff": 0.45,
            "capex": 1500,  # USD/kW
            "opex": 0.015  # USD/kWh
        },
        "references": [
            "Jenbacher (INNIO)",
            "Caterpillar",
            "MWM"
        ]
    },

    "gas_turbine": {
        "id": "gas_turbine",
        "category": "enduse",
        "name": "Turbina a Gás",
        "name_en": "Gas Turbine",
        "description": "Para grandes potências (>5 MW), maior confiabilidade",
        "icon": "⚡",
        "color": "#FFA500",
        "accepts": ["biomethane"],
        "outputs": ["electricity", "heat"],
        "parameters": [
            {
                "key": "elec_efficiency",
                "label": "Eficiência Elétrica",
                "unit": "%",
                "default_value": 33,
                "min": 28,
                "max": 38,
                "step": 1,
                "tooltip": "Eficiência elétrica da turbina"
            }
        ],
        "defaults": {
            "elec_eff": 0.33,
            "therm_eff": 0.48,
            "capex": 2000,
            "min_capacity": 5000  # kW
        },
        "references": [
            "GE Gas Power",
            "Solar Turbines"
        ]
    },

    "microturbine": {
        "id": "microturbine",
        "category": "enduse",
        "name": "Microturbina",
        "name_en": "Microturbine",
        "description": "Pequena escala (<500 kW), alta confiabilidade",
        "icon": "⚡",
        "color": "#FF8C00",
        "accepts": ["biogas", "biomethane"],
        "outputs": ["electricity", "heat"],
        "parameters": [],
        "defaults": {
            "elec_eff": 0.28,
            "therm_eff": 0.52,
            "capex": 2500,
            "max_capacity": 500  # kW
        },
        "references": [
            "Capstone Turbine"
        ]
    },

    "fuel_cell": {
        "id": "fuel_cell",
        "category": "enduse",
        "name": "Célula a Combustível",
        "name_en": "Fuel Cell",
        "description": "Alta eficiência elétrica (SOFC/MCFC), tecnologia emergente",
        "icon": "🔋",
        "color": "#32CD32",
        "accepts": ["biomethane"],
        "outputs": ["electricity", "heat"],
        "parameters": [],
        "defaults": {
            "elec_eff": 0.50,
            "therm_eff": 0.35,
            "capex": 4000,
            "lifetime": 10  # years
        },
        "references": [
            "Bloom Energy",
            "FuelCell Energy"
        ]
    },

    "boiler": {
        "id": "boiler",
        "category": "enduse",
        "name": "Caldeira",
        "name_en": "Boiler",
        "description": "Uso térmico direto para vapor de processo",
        "icon": "🔥",
        "color": "#DC143C",
        "accepts": ["biogas", "biomethane"],
        "outputs": ["heat"],
        "parameters": [
            {
                "key": "therm_efficiency",
                "label": "Eficiência Térmica",
                "unit": "%",
                "default_value": 85,
                "min": 75,
                "max": 92,
                "step": 1,
                "tooltip": "Eficiência da caldeira"
            }
        ],
        "defaults": {
            "therm_eff": 0.85,
            "capex": 200,  # USD/kW thermal
            "steam_pressure": 21  # bar
        },
        "references": []
    },

    "biomethane_gnv": {
        "id": "biomethane_gnv",
        "category": "enduse",
        "name": "Biometano GNV",
        "name_en": "Biomethane CNG",
        "description": "Comercialização como combustível veicular comprimido",
        "icon": "🚛",
        "color": "#228B22",
        "accepts": ["biomethane"],
        "outputs": ["revenue"],
        "parameters": [
            {
                "key": "price",
                "label": "Preço de Venda",
                "unit": "R$/Nm³",
                "default_value": 3.50,
                "min": 2.50,
                "max": 5.00,
                "step": 0.10,
                "tooltip": "Preço de venda do biometano GNV"
            }
        ],
        "defaults": {
            "price": 3.50,  # R$/Nm³
            "compression_cost": 0.30,  # R$/Nm³
            "compression_energy": 0.10  # kWh/Nm³
        },
        "references": [
            "ANP - Resolução 685/2017"
        ]
    },

    "biomethane_grid": {
        "id": "biomethane_grid",
        "category": "enduse",
        "name": "Injeção na Rede de Gás",
        "name_en": "Grid Injection",
        "description": "Venda para distribuidora de gás natural",
        "icon": "🏭",
        "color": "#4169E1",
        "accepts": ["biomethane"],
        "outputs": ["revenue"],
        "parameters": [
            {
                "key": "price",
                "label": "Preço de Venda",
                "unit": "R$/Nm³",
                "default_value": 2.80,
                "min": 2.00,
                "max": 4.00,
                "step": 0.10,
                "tooltip": "Preço de venda para a rede"
            }
        ],
        "defaults": {
            "price": 2.80,  # R$/Nm³
            "min_quality": 0.96,  # 96% CH4 minimum
            "wobbe_index": 52  # MJ/Nm³
        },
        "references": [
            "ANP - Resolução 734/2018"
        ]
    },

    "flare": {
        "id": "flare",
        "category": "enduse",
        "name": "Flare (Queima)",
        "name_en": "Flare",
        "description": "Queima emergencial ou excedente, apenas redução de emissões",
        "icon": "🔥",
        "color": "#8B0000",
        "accepts": ["biogas", "biomethane"],
        "outputs": ["emissions_reduction"],
        "parameters": [],
        "defaults": {
            "destruction_efficiency": 0.99,
            "capex": 50,  # USD/Nm³/h
            "co2_reduction": 21  # kgCO2eq/Nm³ CH4 avoided
        },
        "references": []
    },

    # ==================== BYPRODUCTS ====================
    "digestate_liquid": {
        "id": "digestate_liquid",
        "category": "byproduct",
        "name": "Digestato Líquido",
        "name_en": "Liquid Digestate",
        "description": "Biofertilizante líquido rico em NPK",
        "icon": "💧",
        "color": "#6B8E23",
        "accepts": ["digestate"],
        "outputs": ["biofertilizer"],
        "parameters": [],
        "defaults": {
            "n_content": 2.5,  # kg N/m³
            "p_content": 0.8,  # kg P2O5/m³
            "k_content": 3.0,  # kg K2O/m³
            "value": 0.15  # R$/m³
        },
        "references": []
    },

    "digestate_solid": {
        "id": "digestate_solid",
        "category": "byproduct",
        "name": "Digestato Sólido",
        "name_en": "Solid Digestate",
        "description": "Condicionador de solo após separação sólido-líquido",
        "icon": "🌱",
        "color": "#8B4513",
        "accepts": ["digestate"],
        "outputs": ["soil_conditioner"],
        "parameters": [],
        "defaults": {
            "organic_matter": 50,  # %
            "moisture": 60,  # %
            "value": 30  # R$/t
        },
        "references": []
    },

    "co2_capture": {
        "id": "co2_capture",
        "category": "byproduct",
        "name": "CO2 Capturado",
        "name_en": "Captured CO2",
        "description": "CO2 de grau alimentício para venda",
        "icon": "💨",
        "color": "#B0C4DE",
        "accepts": ["co2"],
        "outputs": ["co2_product"],
        "parameters": [],
        "defaults": {
            "purity": 99.9,  # %
            "value": 200,  # R$/t CO2
            "purification_cost": 100  # R$/t
        },
        "references": [
            "Linde, Air Liquide"
        ]
    }
}
