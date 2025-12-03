"""
Pydantic schemas for BioRoute Builder
"""

from pydantic import BaseModel
from typing import Literal, Optional
from enum import Enum
from datetime import datetime


class TechCategory(str, Enum):
    FEEDSTOCK = "feedstock"
    PRETREATMENT = "pretreatment"
    DIGESTER = "digester"
    UPGRADING = "upgrading"
    ENDUSE = "enduse"
    BYPRODUCT = "byproduct"


class Parameter(BaseModel):
    key: str
    label: str
    unit: str
    default_value: float
    min: float
    max: float
    step: float
    tooltip: str


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

    icon: Optional[str] = None
    color: Optional[str] = None


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


class NodeInput(BaseModel):
    node_id: str
    tech_id: str
    position: dict
    parameters: dict


class EdgeInput(BaseModel):
    source: str
    target: str
    source_handle: Optional[str] = None
    target_handle: Optional[str] = None


class CalculationRequest(BaseModel):
    nodes: list[NodeInput]
    edges: list[EdgeInput]


class CalculationResponse(BaseModel):
    success: bool
    results: Optional[dict] = None
    error: Optional[str] = None


class ScenarioCreate(BaseModel):
    name: str
    description: Optional[str] = ""
    nodes: list[NodeInput]
    edges: list[EdgeInput]


class ScenarioResponse(BaseModel):
    id: str
    share_url: str


class StreamProperties(BaseModel):
    """Properties of a material/energy stream between nodes"""
    mass_flow: float = 0.0        # kg/h or t/day
    volume_flow: float = 0.0      # m³/h or Nm³/h
    energy_content: float = 0.0   # MJ/h or kW
    methane_content: float = 0.0  # Nm³ CH4/h
    cod: float = 0.0              # kg COD/h
    vs_content: float = 0.0       # kg VS/h
    temperature: float = 35.0     # °C
    pressure: float = 1.0         # bar
