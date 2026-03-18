import os
from typing import Literal
from langgraph.graph import StateGraph, END
from state import AgriState
from agents import (
    scout_node, planner_node, safety_verifer_node,
    execution_node, rollback_node
)

from langgraph.checkpoint.memory import MemorySaver

def build_agri_graph():
    workflow = StateGraph(AgriState)
    checkpointer = MemorySaver()

    # Add Nodes
    workflow.add_node("scout", scout_node)
    workflow.add_node("planner", planner_node)
    workflow.add_node("safety", safety_verifer_node)
    workflow.add_node("executor", execution_node)
    workflow.add_node("rollback", rollback_node)

    # Set Entry Point
    workflow.set_entry_point("scout")

    # Define Transitions
    workflow.add_edge("scout", "planner")

    def route_after_planner(state: AgriState) -> Literal["safety", "END"]:
        if state["treatment_required"] and state["inventory_reserved"]:
            return "safety"
        elif state["treatment_required"] and not state["inventory_reserved"]:
             return "END"
        else:
            return "END"

    workflow.add_conditional_edges("planner", route_after_planner, {"safety": "safety", "END": END})

    def route_after_safety(state: AgriState) -> Literal["executor", "rollback"]:
        if state["safe_to_proceed"]:
            return "executor"
        else:
            return "rollback"

    workflow.add_conditional_edges("safety", route_after_safety)
    
    workflow.add_edge("rollback", END)
    
    def route_after_execution(state: AgriState) -> Literal["END", "rollback"]:
        if state["phase"] == "completed":
            return "END"
        else:
            return "rollback"

    workflow.add_conditional_edges("executor", route_after_execution, {"END": END, "rollback": "rollback"})

    return workflow.compile(checkpointer=checkpointer, interrupt_before=["executor"])

if __name__ == "__main__":
    app = build_agri_graph()
    
    # Initialize State
    initial_state = {
        "field_id": "Corn-Field-001",
        "crop_type": "Corn",
        "health_score": 0.5, # Trigger treatment
        "anomalies": ["Manual override: Pests"],
        "treatment_required": False,
        "treatment_type": None,
        "agent_id": "Drone-X1",
        "phase": "scouting",
        "inventory_reserved": False,
        "hardware_ready": False,
        "safe_to_proceed": False,
        "user_approval": None,
        "rollback_reason": None,
        "logs": ["System: Starting Autonomous Remediation Workflow."]
    }

    # Run up to interrupt
    print("--- RUNNING AGENTS ---")
    config = {"configurable": {"thread_id": "1"}}
    for event in app.stream(initial_state, config):
        for name, data in event.items():
             print(f"\n[Node: {name}]")
             if name == "__interrupt__":
                 print("  Interrupt triggered. Waiting for approval.")
                 continue
             for log in data.get("logs", []):
                 print(f"  {log}")

    # Check if we are at the interrupt
    curr_state = app.get_state(config)
    if curr_state.next:
        print("\n--- HUMAN INTERRUPT ---")
        print("Planner proposes treatment. Safety verified. Proceed?")
        # Simulate human approval
        user_input = "yes" 
        if user_input.lower() == "yes":
            print("User approved. Resuming execution...")
            # We must pass None to resume from the interrupt
            for event in app.stream(None, config):
                 for name, data in event.items():
                     print(f"\n[Node: {name}]")
                     if name == "__interrupt__":
                         continue
                     for log in data.get("logs", []):
                         print(f"  {log}")
        else:
            print("User denied. Rolling back...")
            # Handled by rollback logic on user_approval=False in a more complex setup
            # Here we just stop or manually route to rollback
            app.update_state(config, {"rollback_reason": "User denied approval"})
            # In real scenario we'd resume and have logic to route to rollback
