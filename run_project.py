# run_project.py
import generator_traffic  # ✅ Import the module correctly
from optimization_methods import OptimizationMethods
from visualization import visualize_results
from config import ODU_rates  # ✅ Import ODU rates to avoid NameError

def main():
    """Run all optimizations on 30 traffic scenarios and compare"""
    traffic_generator = generator_traffic.TrafficMatrix()  # ✅ Correctly reference TrafficMatrix
    scenarios = traffic_generator.get_scenarios()  # Get 30 traffic samples

    all_results = {method: [] for method in ["ILP", "Brute-Force", "Greedy", "Genetic", "Simulated Annealing", "Particle Swarm", "Ant Colony"]}
    execution_times = {method: 0 for method in all_results.keys()}  # ✅ Track execution times
    unassigned_traffic = {method: [] for method in all_results.keys()}  # ✅ Track unassigned traffic

    for traffic in scenarios:
        optimizer = OptimizationMethods(traffic)
        results, times = optimizer.run_all()  # ✅ Now correctly returns results & times

        for method in results:
            all_results[method].append(results[method])
            execution_times[method] += times[method] / len(scenarios)  # ✅ Average time over scenarios

            # ✅ Compute Unassigned Traffic per Scenario
            total_assigned = results[method]["Framer1"] + results[method]["Framer2"]
            total_traffic = sum(ODU_rates[o] * traffic[o] for o in traffic)  # ✅ Now works correctly
            unassigned_traffic[method].append(total_traffic - total_assigned)

    # ✅ Correctly pass all arguments
    visualize_results(all_results, execution_times, scenarios, unassigned_traffic)

if __name__ == "__main__":
    main()
