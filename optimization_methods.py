# optimization_methods.py
import random
import itertools
import numpy as np
import time
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm  # Progress bar
from config import ODUs, ODU_rates, Framers, Framer_capacity, Max_ODUs, SEED

# ✅ Set fixed seed
random.seed(SEED)
np.random.seed(SEED)

# ✅ Try importing Gurobi for ILP
try:
    from gurobipy import Model, GRB
    GUROBI_AVAILABLE = True
except ImportError:
    print("⚠️ Warning: Gurobi is not installed! ILP optimization will be skipped.")
    GUROBI_AVAILABLE = False

from deap import base, creator, tools, algorithms
from scipy.optimize import dual_annealing
from pyswarm import pso

class OptimizationMethods:
    def __init__(self, traffic_scenario):
        self.traffic = traffic_scenario
        self.results = {}
        self.execution_times = {}

    def run_all(self):
        """Run all optimization algorithms and track execution time"""
        methods = [
            ("ILP", self.ilp_optimization),
            ("Brute-Force", self.brute_force),
            ("Greedy", self.greedy),
            ("Genetic", self.genetic_algorithm),
            ("Simulated Annealing", self.simulated_annealing),
            ("Particle Swarm", self.particle_swarm),
            ("Ant Colony", self.ant_colony),
        ]

        with tqdm(total=len(methods), desc="Running Optimization Methods") as progress_bar:
            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = {executor.submit(self.timed_execution, method, name): name for name, method in methods}
                for future in futures:
                    future.result()
                    progress_bar.update(1)

        return self.results, self.execution_times

    def timed_execution(self, func, name):
        start_time = time.time()
        func()
        self.execution_times[name] = time.time() - start_time

    def evaluate_assignment(self, assignment):
        """Evaluate ODU-to-Framer assignment while enforcing framer capacity constraint (500G)"""
        load = {f: 0 for f in Framers}  
        
        for i, o in enumerate(ODUs):
            f = Framers[int(assignment[i]) % len(Framers)]  
            odu_traffic = ODU_rates[o] * self.traffic.get(o, 0)

            if load[f] + odu_traffic <= Framer_capacity[f]:
                load[f] += odu_traffic
            else:
                other_framer = Framers[(Framers.index(f) + 1) % len(Framers)]
                if load[other_framer] + odu_traffic <= Framer_capacity[other_framer]:
                    load[other_framer] += odu_traffic
                else:
                    print(f"⚠️ WARNING: Traffic {odu_traffic}G could not be assigned (Framers Full).")

        return load

    def ilp_optimization(self):
        """ILP Optimization using Gurobi"""
        if not GUROBI_AVAILABLE:
            return
        model = Model("ILP_ODU_Framer")
        x = model.addVars(ODUs, Framers, vtype=GRB.INTEGER, name="x")

        for o in self.traffic:
            model.addConstr(sum(x[o, f] for f in Framers) == self.traffic[o])
        for f in Framers:
            model.addConstr(sum(x[o, f] * ODU_rates[o] for o in ODUs) <= Framer_capacity[f])

        model.setObjective(sum(x[o, f] for o in ODUs for f in Framers), GRB.MAXIMIZE)
        model.optimize()

        self.results["ILP"] = {f: sum(x[o, f].x * ODU_rates[o] for o in ODUs) for f in Framers}

    def brute_force(self):
        """Brute-Force Enumeration"""
        best_assignment = None
        best_value = 0
        best_load = None
        for assignment in itertools.product(range(len(Framers)), repeat=len(ODUs)):
            load = self.evaluate_assignment(assignment)
            value = sum(load.values())
            if value > best_value:
                best_value, best_assignment, best_load = value, assignment, load
        self.results["Brute-Force"] = best_load if best_load else {f: 0 for f in Framers}

    def greedy(self):
        """Greedy Algorithm"""
        greedy_load = {f: 0 for f in Framers}
        for o in ODUs:
            sorted_framers = sorted(Framers, key=lambda f: greedy_load[f])
            for f in sorted_framers:
                if greedy_load[f] + ODU_rates[o] <= Framer_capacity[f]:
                    greedy_load[f] += ODU_rates[o]
                    break
        self.results["Greedy"] = greedy_load

    def genetic_algorithm(self):
        """Genetic Algorithm (GA) Optimization"""
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)
        toolbox = base.Toolbox()

        toolbox.register("attr_int", random.randint, 0, len(Framers) - 1)
        toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_int, len(ODUs))
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        toolbox.register("evaluate", lambda ind: (sum(self.evaluate_assignment(ind).values()),))
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.2)
        toolbox.register("select", tools.selTournament, tournsize=3)

        population = toolbox.population(n=30)  
        algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=5, verbose=False)
        best_individual = tools.selBest(population, 1)[0]
        self.results["Genetic"] = self.evaluate_assignment(best_individual)

    def simulated_annealing(self):
        """Simulated Annealing Optimization"""
        def sa_objective(x):
            return -sum(self.evaluate_assignment(x).values())

        result = dual_annealing(sa_objective, bounds=[(0, len(Framers) - 1)] * len(ODUs), maxiter=200)
        self.results["Simulated Annealing"] = self.evaluate_assignment(result.x)

    def particle_swarm(self):
        """Particle Swarm Optimization (PSO)"""
        def pso_objective(x):
            return -sum(self.evaluate_assignment(x).values())

        best_x, _ = pso(pso_objective, [0] * len(ODUs), [len(Framers) - 1] * len(ODUs), swarmsize=20)
        self.results["Particle Swarm"] = self.evaluate_assignment(best_x)

    def ant_colony(self):
        """Ant Colony Optimization (ACO)"""
        pheromone = np.ones((len(ODUs), len(Framers)))

        for _ in range(50):
            path = [np.random.choice(range(len(Framers)), p=pheromone[i] / np.sum(pheromone[i])) for i in range(len(ODUs))]
            reward = sum(self.evaluate_assignment(path).values())
            pheromone += reward / 100

        self.results["Ant Colony"] = self.evaluate_assignment(path)
