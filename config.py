# config.py
import random
import numpy as np

# ✅ Fixed Seed for Reproducibility
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

# ✅ Define ODUs and their rates
ODUs = ["ODU0", "ODU2", "ODU4", "ODUC4"]
ODU_rates = {"ODU0": 1.25, "ODU2": 10, "ODU4": 100, "ODUC4": 400}

# ✅ Framers and their Constraints
Framers = ["Framer1", "Framer2"]
Framer_capacity = {"Framer1": 500, "Framer2": 500}
Max_ODUs = {"Framer1": 200, "Framer2": 200}

# ✅ Traffic Matrix Parameters
TOTAL_CAPACITY = 1000  # Max port 2 traffic
NUM_TRAFFIC_SCENARIOS = 30  # Generate 30 scenarios for comparison

# ✅ Optimization Parameters
POPULATION_SIZE = 50  # Genetic Algorithm
NUM_GENERATIONS = 100
SA_TEMPERATURE = 1000  # Simulated Annealing
PSO_PARTICLES = 30
ACO_ANTS = 20
