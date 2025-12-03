"""
BioRoute Builder - Backend API
FastAPI application for biogas route calculation and scenario management
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime

from app.models.schemas import (
    NodeInput,
    EdgeInput,
    CalculationRequest,
    CalculationResponse,
    ScenarioCreate,
    ScenarioResponse
)
from app.services.calculation_engine import CalculationEngine
from data.technologies import TECH_DATABASE
from data.templates import SCENARIO_TEMPLATES

# Initialize FastAPI app
app = FastAPI(
    title="BioRoute Builder API",
    version="1.0.0",
    description="API for designing and analyzing biogas technological routes"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for scenarios (for MVP - replace with database later)
scenarios_storage = {}


# ==================== HEALTH CHECK ====================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "BioRoute Builder API is running",
        "version": "1.0.0",
        "status": "healthy"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "technologies_count": len(TECH_DATABASE),
        "templates_count": len(SCENARIO_TEMPLATES)
    }


# ==================== TECHNOLOGIES ====================

@app.get("/api/technologies")
async def get_technologies():
    """
    Get all available technologies
    Returns complete catalog of feedstocks, digesters, upgrading, and end-use technologies
    """
    return {
        "success": True,
        "count": len(TECH_DATABASE),
        "technologies": TECH_DATABASE
    }


@app.get("/api/technologies/{category}")
async def get_technologies_by_category(category: str):
    """
    Get technologies filtered by category
    Categories: feedstock, pretreatment, digester, upgrading, enduse, byproduct
    """
    filtered = {
        k: v for k, v in TECH_DATABASE.items()
        if v['category'] == category
    }

    if not filtered:
        raise HTTPException(
            status_code=404,
            detail=f"No technologies found for category '{category}'"
        )

    return {
        "success": True,
        "category": category,
        "count": len(filtered),
        "technologies": filtered
    }


@app.get("/api/technologies/detail/{tech_id}")
async def get_technology_detail(tech_id: str):
    """Get detailed information about a specific technology"""
    if tech_id not in TECH_DATABASE:
        raise HTTPException(
            status_code=404,
            detail=f"Technology '{tech_id}' not found"
        )

    return {
        "success": True,
        "technology": TECH_DATABASE[tech_id]
    }


# ==================== CALCULATIONS ====================

@app.post("/api/calculate")
async def calculate_route(request: CalculationRequest):
    """
    Calculate mass/energy balance for a biogas route
    Accepts nodes and edges, returns complete calculation results
    """
    try:
        # Initialize calculation engine
        engine = CalculationEngine(TECH_DATABASE)

        # Convert Pydantic models to dicts
        nodes_data = [n.model_dump() for n in request.nodes]
        edges_data = [e.model_dump() for e in request.edges]

        # Perform calculation
        results = engine.calculate_route(nodes_data, edges_data)

        return results

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Calculation error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.post("/api/validate")
async def validate_route(request: CalculationRequest):
    """
    Validate a route configuration without running full calculations
    Checks for cycles, connection compatibility, and graph validity
    """
    try:
        engine = CalculationEngine(TECH_DATABASE)

        nodes_data = [n.model_dump() for n in request.nodes]
        edges_data = [e.model_dump() for e in request.edges]

        # Build graph (this validates structure)
        engine.build_graph(nodes_data, edges_data)

        # Check connection compatibility
        errors = []
        for edge in edges_data:
            source_node = next(n for n in nodes_data if n['node_id'] == edge['source'])
            target_node = next(n for n in nodes_data if n['node_id'] == edge['target'])

            source_tech = TECH_DATABASE[source_node['tech_id']]
            target_tech = TECH_DATABASE[target_node['tech_id']]

            # Check if source outputs are compatible with target inputs
            source_outputs = set(source_tech['outputs'])
            target_accepts = set(target_tech['accepts'])

            if not target_accepts:  # Target accepts anything
                continue

            if not source_outputs.intersection(target_accepts):
                errors.append({
                    "edge": f"{edge['source']} -> {edge['target']}",
                    "error": "Incompatible connection",
                    "details": f"{source_tech['name']} outputs {source_outputs} but {target_tech['name']} accepts {target_accepts}"
                })

        if errors:
            return {
                "success": False,
                "valid": False,
                "errors": errors
            }

        return {
            "success": True,
            "valid": True,
            "message": "Route configuration is valid"
        }

    except ValueError as e:
        return {
            "success": False,
            "valid": False,
            "errors": [{"error": str(e)}]
        }


# ==================== TEMPLATES ====================

@app.get("/api/templates")
async def get_templates():
    """
    Get pre-built scenario templates
    Returns 4 typical configurations for sugarcane mills
    """
    return {
        "success": True,
        "count": len(SCENARIO_TEMPLATES),
        "templates": SCENARIO_TEMPLATES
    }


@app.get("/api/templates/{template_id}")
async def get_template(template_id: str):
    """Get a specific template by ID"""
    template = next((t for t in SCENARIO_TEMPLATES if t['id'] == template_id), None)

    if not template:
        raise HTTPException(
            status_code=404,
            detail=f"Template '{template_id}' not found"
        )

    return {
        "success": True,
        "template": template
    }


# ==================== SCENARIOS ====================

@app.post("/api/scenarios")
async def create_scenario(scenario: ScenarioCreate):
    """
    Save a scenario configuration
    Returns scenario ID and share URL
    """
    try:
        scenario_id = str(uuid.uuid4())
        share_token = uuid.uuid4().hex[:8]

        # Store scenario (in-memory for MVP)
        scenarios_storage[scenario_id] = {
            "id": scenario_id,
            "name": scenario.name,
            "description": scenario.description,
            "nodes": [n.model_dump() for n in scenario.nodes],
            "edges": [e.model_dump() for e in scenario.edges],
            "share_token": share_token,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }

        return {
            "success": True,
            "id": scenario_id,
            "share_token": share_token,
            "share_url": f"/s/{share_token}"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save scenario: {str(e)}"
        )


@app.get("/api/scenarios/{scenario_id}")
async def get_scenario(scenario_id: str):
    """Get a saved scenario by ID"""
    if scenario_id not in scenarios_storage:
        raise HTTPException(
            status_code=404,
            detail=f"Scenario '{scenario_id}' not found"
        )

    return {
        "success": True,
        "scenario": scenarios_storage[scenario_id]
    }


@app.get("/api/scenarios/shared/{share_token}")
async def get_shared_scenario(share_token: str):
    """Get a scenario by share token (public access)"""
    scenario = next(
        (s for s in scenarios_storage.values() if s['share_token'] == share_token),
        None
    )

    if not scenario:
        raise HTTPException(
            status_code=404,
            detail=f"Shared scenario not found"
        )

    return {
        "success": True,
        "scenario": scenario
    }


@app.get("/api/scenarios")
async def list_scenarios():
    """List all saved scenarios (for MVP - add user filtering later)"""
    return {
        "success": True,
        "count": len(scenarios_storage),
        "scenarios": list(scenarios_storage.values())
    }


@app.delete("/api/scenarios/{scenario_id}")
async def delete_scenario(scenario_id: str):
    """Delete a scenario"""
    if scenario_id not in scenarios_storage:
        raise HTTPException(
            status_code=404,
            detail=f"Scenario '{scenario_id}' not found"
        )

    del scenarios_storage[scenario_id]

    return {
        "success": True,
        "message": "Scenario deleted successfully"
    }


# ==================== COMPARISON ====================

@app.post("/api/compare")
async def compare_scenarios(scenario_ids: List[str]):
    """
    Compare multiple scenarios side by side
    Returns aggregated results for easy comparison
    """
    if len(scenario_ids) < 2:
        raise HTTPException(
            status_code=400,
            detail="At least 2 scenarios required for comparison"
        )

    comparison_results = []

    for scenario_id in scenario_ids:
        if scenario_id not in scenarios_storage:
            raise HTTPException(
                status_code=404,
                detail=f"Scenario '{scenario_id}' not found"
            )

        scenario = scenarios_storage[scenario_id]

        # Calculate results for this scenario
        try:
            engine = CalculationEngine(TECH_DATABASE)
            results = engine.calculate_route(scenario['nodes'], scenario['edges'])

            comparison_results.append({
                "scenario_id": scenario_id,
                "scenario_name": scenario['name'],
                "summary": results['summary']
            })

        except Exception as e:
            comparison_results.append({
                "scenario_id": scenario_id,
                "scenario_name": scenario['name'],
                "error": str(e)
            })

    return {
        "success": True,
        "scenarios_compared": len(scenario_ids),
        "results": comparison_results
    }


# ==================== RUN SERVER ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
