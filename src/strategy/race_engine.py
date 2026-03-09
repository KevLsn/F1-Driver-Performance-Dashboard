# Author: Loussouarn Kévin
# Date: 25/02/2026
# Description: Race simulation engine using Predictor output

from typing import Dict, List
import numpy as np
from datetime import timedelta
import math

# Simulate a full race using predictive tyre parameters.
class RaceEngine:

    # Constructor
    # Input: parameters (dict from Predictor.get_parameters()), race_laps (int), fuel_coef (float), pit_delta (float), use_stochastic (bool)
    # Output: RaceEngine object
    # Precondition: parameters contains at least one compound
    # Postcondition: Engine ready to simulate strategies
    def __init__(self, parameters: Dict[str, Dict[str, float]], race_laps: int, fuel_coef: float = 0.035, pit_delta: float = 22.0, use_stochastic: bool = False):
        self.parameters = parameters
        self.race_laps = race_laps
        self.fuel_coef = fuel_coef
        self.pit_delta = pit_delta
        self.use_stochastic = use_stochastic

    # Compute predicted lap time for a given compound and stint lap number
    # Input: compound (str), stint_lap (int), current_lap (int)
    # Output: lap_time (float, seconds)
    # Precondition: compound exists in parameters
    # Postcondition: returns predicted lap time in seconds
    def compute_lap_time(self, compound: str, stint_lap: int, current_lap: int) -> float:

        # Extract parameters
        base = self.parameters[compound]["base_pace"].total_seconds()
        degradation = self.parameters[compound]["degradation"]
        variance = self.parameters[compound]["variance"]

        # Tyre degradation effect: time increases with each lap on the same stint
        tyre_time = base + degradation * (math.exp(0.08 * stint_lap) - 1)

        # Fuel effect: heavy at start, diminishes as race progresses
        fuel_time = -self.fuel_coef * (self.race_laps - current_lap)

        # Total lap time is base + degradation + fuel effect
        lap_time = tyre_time + fuel_time

        if self.use_stochastic:
            lap_time += np.random.normal(0, variance)

        return lap_time

    # Simulate a race strategy
    # Input: compounds (list of str), pit_laps (list of int)
    # Output: total_time (float, seconds)
    # Precondition: len(compounds) = len(pit_laps) + 1
    # Postcondition: returns total race time including pit loss
    def simulate_strategy(self, compounds: List[str], pit_laps: List[int]) -> float:

        # Verify that the strategy is valid (enough compounds for the number of pit stops)
        if len(compounds) < len(pit_laps) + 1:
            raise ValueError(
                f"Not enough compounds for the strategy: "
                f"{len(compounds)} compounds, {len(pit_laps)} pit stops "
                f"(need at least {len(pit_laps)+1} compounds)"
            )

        total_time = 0.0
        current_stint_index = 0
        stint_lap = 1
        pit_lap_set = set(pit_laps)

        # Simulate each lap of the race
        for lap in range(1, self.race_laps + 1):

            # Pit stop
            if lap in pit_lap_set:
                total_time += self.pit_delta
                current_stint_index += 1
                stint_lap = 1  # First lap on new tyre
            
            compound = compounds[current_stint_index]
            lap_time = self.compute_lap_time(compound=compound, stint_lap=stint_lap, current_lap=lap)
            total_time += lap_time
            stint_lap += 1

        return total_time

    # Monte Carlo Simulation, run stochastic simulation for a strategy
    # Input: compounds (list of str), pit_laps (list of int), n_simulations (int)
    # Output: dict with mean_time and std_time
    # Precondition: strategy valid
    # Postcondition: returns statistical race outcome
    def simulate_monte_carlo(self, compounds: List[str], pit_laps: List[int], n_simulations: int = 1000) -> Dict[str, float]:

        results = []
        self.use_stochastic = True  # Enable stochastic lap times

        # Run multiple simulations and collect total times
        for _ in range(n_simulations):
            total = self.simulate_strategy(compounds, pit_laps)
            results.append(total)

        self.use_stochastic = False # Reset to deterministic mode

        return {"mean_time": float(np.mean(results)), "std_time": float(np.std(results))}