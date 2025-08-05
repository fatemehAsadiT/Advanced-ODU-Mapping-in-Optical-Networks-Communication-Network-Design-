import matplotlib.pyplot as plt
import numpy as np
from config import ODU_rates, Framer_capacity

def visualize_results(all_results, execution_times, traffic_scenarios, unassigned_traffic):
    methods = list(all_results.keys())

    # --- 1️⃣ Compute total traffic for each scenario ---
    total_traffic_per_scenario = []
    for scenario in traffic_scenarios:
        total_traffic = sum(ODU_rates[o] * scenario[o] for o in scenario)
        total_traffic_per_scenario.append(total_traffic)

    # ✅ FIGURE 1: Total ODU Traffic per Scenario
    plt.figure(figsize=(12, 6))
    plt.bar(range(len(traffic_scenarios)), total_traffic_per_scenario, color='blue', alpha=0.7)
    plt.xlabel("Traffic Scenario Index")
    plt.ylabel("Total Traffic (Gbit/s)")
    plt.title("Total ODU Traffic per Scenario (Summed ODUs)")
    plt.ylim(0, max(total_traffic_per_scenario) * 1.2)  # Scale based on max traffic
    plt.xticks(range(0, len(traffic_scenarios), 5))
    plt.show(block=False)

    # --- 2️⃣ Plot Framer Load Distribution for Each Method Across 30 Traffic Cases ---
    for method in methods:
        framer1_loads = [res["Framer1"] for res in all_results[method]]
        framer2_loads = [res["Framer2"] for res in all_results[method]]
        unassigned_loads = unassigned_traffic[method]  # Track unassigned traffic
        avg_framer1 = np.mean(framer1_loads)
        avg_framer2 = np.mean(framer2_loads)
        avg_unassigned = np.mean(unassigned_loads)

        plt.figure(figsize=(14, 6))
        x_labels = [f"T{i+1}" for i in range(len(framer1_loads))] + ["Avg"]
        framer1_loads.append(avg_framer1)
        framer2_loads.append(avg_framer2)
        unassigned_loads.append(avg_unassigned)

        # ✅ Dynamically adjust Y-axis based on each traffic scenario
        scenario_traffic = total_traffic_per_scenario + [np.mean(total_traffic_per_scenario)]  # Append average
        max_traffic_this_method = max(scenario_traffic) * 1.1  # Scale slightly above max scenario traffic

        # ✅ FIGURES 2-8: Framer Load Distribution + Unassigned Traffic
        plt.bar(x_labels, framer1_loads, label="Framer1 Load", color='blue')
        plt.bar(x_labels, framer2_loads, bottom=framer1_loads, label="Framer2 Load", color='orange')
        plt.bar(x_labels, unassigned_loads, bottom=np.array(framer1_loads) + np.array(framer2_loads), label="Unassigned Load", color='gray')

        plt.xlabel("Traffic Scenario (T1-T30) + Average")
        plt.ylabel("Load (Gbit/s)")
        plt.title(f"Framer Load Distribution for {method} Across 30 Traffic Scenarios")
        plt.legend()
        plt.xticks(rotation=45, fontsize=8)
        plt.ylim(0, max_traffic_this_method)  # ✅ Dynamically scale based on actual traffic
        plt.show(block=False)

    # --- 9️⃣ Compute Average Execution Time per Method ---
    avg_execution_time_values = [execution_times[m] for m in methods]

    # ✅ FIGURE 9: Execution Time Comparison
    plt.figure(figsize=(12, 6))
    plt.bar(methods, avg_execution_time_values, color='red')
    plt.xlabel("Optimization Methods")
    plt.ylabel("Average Execution Time (seconds)")
    plt.title("Average Execution Time Across Optimization Methods")
    plt.xticks(rotation=45)
    plt.show(block=False)

    # --- 🔟 Compute Average Unassigned Traffic per Method ---
    avg_unassigned_traffic = [np.mean(unassigned_traffic[m]) for m in methods]

    # ✅ FIGURE 🔟: Unassigned Traffic per Method
    plt.figure(figsize=(12, 6))
    plt.bar(methods, avg_unassigned_traffic, color='gray')
    plt.xlabel("Optimization Methods")
    plt.ylabel("Average Unassigned Traffic (Gbit/s)")
    plt.title("Average Unassigned Traffic Across Optimization Methods")
    plt.xticks(rotation=45)
    plt.show(block=False)

    # ✅ Keep all figures open
    plt.pause(5)
    plt.show()
