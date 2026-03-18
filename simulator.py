import random
import time

class AgriSimulator:
    """Simulates agricultural hardware and environmental conditions."""
    
    def __init__(self):
        self.inventory = {
            "Pesticide-A": 500, # Liters
            "Nutrient-B": 300,
            "Water": 10000
        }
        self.weather = {
            "wind_speed": 12, # km/h
            "is_raining": False
        }
    
    def get_field_data(self, field_id: str):
        """Simulates drone scouting data."""
        time.sleep(1)
        health = random.uniform(0.4, 0.9)
        anomalies = []
        if health < 0.7:
            anomalies.append("Yellowing leaves detected")
        if health < 0.6:
            anomalies.append("Pest clusters found in Sector 7G")
        return {"health_score": health, "anomalies": anomalies}

    def check_inventory(self, item: str, amount: float) -> bool:
        """Reserve inventory (Phase 1: Prepare)."""
        time.sleep(0.5)
        if self.inventory.get(item, 0) >= amount:
            # self.inventory[item] -= amount # Transactional decrement happens in commit
            return True
        return False

    def check_safety_conditions(self) -> dict:
        """Check weather and hardware status."""
        time.sleep(0.5)
        # Randomly fluctuate weather for testing
        current_wind = self.weather["wind_speed"] + random.uniform(-5, 15)
        is_safe = current_wind < 20 # Safety threshold for spraying
        return {"wind_speed": round(current_wind, 2), "is_safe": is_safe}

    def execute_spraying(self, agent_id: str, field_id: str) -> bool:
        """Commit phase: Actual hardware execution."""
        time.sleep(2)
        # Simulate a 10% hardware failure rate
        if random.random() < 0.1:
            return False
        return True

    def rollback(self, reservation_id: str):
        """Rollback logic for inventory and hardware state."""
        time.sleep(1)
        # Reset reservations or stop hardware
        return True
