from typing import TypedDict, List, Optional, Annotated
import operator

class AgriState(TypedDict):
    # Field Data
    field_id: str
    crop_type: str
    health_score: float # 0.0 to 1.0
    anomalies: List[str]
    
    # Treatment Plan
    treatment_required: bool
    treatment_type: Optional[str] # e.g., "Pesticide", "Nutrient", "Irrigation"
    agent_id: str
    
    # Transactional Logic (Two-Phase Commit)
    phase: str # "scouting", "planning", "verifying", "executing", "completed", "failed"
    inventory_reserved: bool
    hardware_ready: bool
    safe_to_proceed: bool
    
    # Human Interrupt
    user_approval: Optional[bool]
    
    # Rollback Info
    rollback_reason: Optional[str]
    logs: Annotated[List[str], operator.add]
