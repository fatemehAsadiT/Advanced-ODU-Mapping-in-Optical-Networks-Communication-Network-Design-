# generator_traffic.py
import random
from config import ODUs, ODU_rates, TOTAL_CAPACITY, NUM_TRAFFIC_SCENARIOS, SEED

# ✅ Set fixed seed for reproducibility
random.seed(SEED)

class TrafficMatrix:
    def __init__(self):
        self.scenarios = []
        self.generate_traffic()

    def generate_traffic(self):
        """Generate multiple random traffic scenarios for ODU assignment"""
        for _ in range(NUM_TRAFFIC_SCENARIOS):
            scenario = {}
            total_capacity = 0
            while total_capacity < TOTAL_CAPACITY:
                odu_type = random.choice(ODUs)
                if total_capacity + ODU_rates[odu_type] > TOTAL_CAPACITY:
                    break
                scenario[odu_type] = scenario.get(odu_type, 0) + 1
                total_capacity += ODU_rates[odu_type]
            self.scenarios.append(scenario)

    def get_scenarios(self):
        """Return generated traffic scenarios"""
        return self.scenarios

# ✅ Test script
if __name__ == "__main__":
    traffic = TrafficMatrix()
    print("TrafficMatrix loaded successfully!")
