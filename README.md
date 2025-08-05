# Advanced-ODU-Mapping-in-Optical-Networks-Communication-Network-Design-(with Nokia)

This repository contains the course project for **Communication Network Design** at Politecnico di Milano, developed in collaboration with **Nokia**.  
The project focuses on optimizing the assignment of Optical Data Units (ODUs) to multi-carrier transponder framers under capacity and operational constraints.

## 📡 Project Overview
Modern optical networks use **multi-carrier transponders** to efficiently map multiple service types. This project compares multiple optimization methods to assign ODUs to framers while:
- Balancing traffic across framers
- Maximizing capacity utilization
- Preventing overload and minimizing unassigned traffic

## 🔹 Problem Constraints
- **Framer Capacity:** 500 Gbit/s per framer
- **Framer ODU Limit:** 200 ODUs per framer
- **ODU Types:**  
  - ODU0 → 1.25 Gbit/s  
  - ODU2 → 10 Gbit/s  
  - ODU4 → 100 Gbit/s  
  - ODUC4 → 400 Gbit/s  
- **Traffic Source:** Port 2 (up to 1000 Gbit/s)

## ⚙ Optimization Methods Implemented
1. **Integer Linear Programming (ILP)** – optimal for small-scale problems  
2. **Brute Force** – exhaustive search for benchmarking  
3. **Greedy Algorithm** – fast but suboptimal  
4. **Genetic Algorithm (GA)** – near-optimal with evolutionary strategies  
5. **Simulated Annealing (SA)** – probabilistic refinement  
6. **Particle Swarm Optimization (PSO)** – swarm intelligence-based search  
7. **Ant Colony Optimization (ACO)** – pheromone-based iterative improvement

## 📊 Simulation Setup
- 30 random traffic scenarios generated  
- Each method evaluated for:
  - Load distribution
  - Execution time
  - Unassigned traffic

## 📈 Key Results
- ILP and Brute Force achieve optimal solutions but have scalability limits
- Metaheuristics (GA, SA, PSO, ACO) achieve near-optimal results with better scalability
- Greedy method is fastest but results in higher unassigned traffic
