from simulator import AgriSimulator
from state import AgriState
import uuid

sim = AgriSimulator()

def scout_node(state: AgriState) -> dict:
    data = sim.get_field_data(state["field_id"])
    logs = [f"Scout: Found {len(data['anomalies'])} anomalies. Health score: {data['health_score']:.2f}"]
    return {
        "health_score": data["health_score"],
        "anomalies": data["anomalies"],
        "phase": "planning",
        "logs": logs
    }

def planner_node(state: AgriState) -> dict:
    if state["health_score"] < 0.7:
        treatment = "Pesticide-A"
        amount = 5.0
        inventory_reserved = sim.check_inventory(treatment, amount)
        logs = [f"Planner: {treatment} treatment proposed. Inventory reserved: {inventory_reserved}"]
        return {
            "treatment_required": True,
            "treatment_type": treatment,
            "inventory_reserved": inventory_reserved,
            "phase": "verifying",
            "logs": logs
        }
    return {
        "treatment_required": False,
        "phase": "completed",
        "logs": ["Planner: No treatment required. Field is healthy."]
    }

def safety_verifer_node(state: AgriState) -> dict:
    safety_data = sim.check_safety_conditions()
    logs = [f"Safety: Wind speed {safety_data['wind_speed']} km/h. Safe to proceed: {safety_data['is_safe']}"]
    return {
        "safe_to_proceed": safety_data["is_safe"],
        "phase": "approving",
        "logs": logs
    }

def execution_node(state: AgriState) -> dict:
    # Phase 2: Commit
    success = sim.execute_spraying(state["agent_id"], state["field_id"])
    if success:
        return {
            "phase": "completed",
            "logs": ["Executor: Treatment successfully applied to field."]
        }
    else:
        return {
            "phase": "failed",
            "rollback_reason": "Hardware failure during spraying",
            "logs": ["Executor: Hardware failure! Initiating rollback."]
        }

def rollback_node(state: AgriState) -> dict:
    sim.rollback(state["agent_id"])
    return {
        "phase": "failed",
        "inventory_reserved": False,
        "logs": [f"Rollback: All resources released. Reason: {state.get('rollback_reason', 'Unknown')}"]
    }
