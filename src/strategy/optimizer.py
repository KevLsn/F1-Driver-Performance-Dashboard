# Author: Loussouarn Kévin
# Date: 25/02/2026
# Description: Strategy optimizer for race simulation engine

from typing import List, Dict
from .race_engine import RaceEngine

# Optimizer for race strategies.
class StrategyOptimizer:

    # Constructor
    # Input: engine (RaceEngine object)
    # Output: StrategyOptimizer object
    # Precondition: engine is initialized
    # Postcondition: Optimizer ready to search strategies
    def __init__(self, engine: RaceEngine):
        self.engine = engine

    # Generate 1-Stop Combinations
    # Input: available_compounds (list of str)
    # Output: list of compound sequences
    # Precondition: at least 2 compounds available
    # Postcondition: returns all possible 2-compound sequences
    def generate_1stop_combinations(self, available_compounds: List[str]) -> List[List[str]]:
        combinations = []
        for c1 in available_compounds:
            for c2 in available_compounds:
                if c1 != c2:
                    combinations.append([c1, c2])
        return combinations

    # Compute and rank all 1-stop strategies
    # Input: available_compounds (list of str), min_pit_lap (int), max_pit_lap (int)
    # Output: list of strategies sorted by total_time
    # Precondition: min_pit_lap < max_pit_lap
    # Postcondition: returns ranked strategy list
    def optimize_1stop(
        self,
        available_compounds: List[str],
        min_pit_lap: int,
        max_pit_lap: int
    ) -> List[Dict]:

        all_results = []

        combinations = self.generate_1stop_combinations(available_compounds)

        for compounds in combinations:
            for pit_lap in range(min_pit_lap, max_pit_lap + 1):

                total_time = self.engine.simulate_strategy(
                    compounds=compounds,
                    pit_laps=[pit_lap]
                )

                all_results.append({
                    "compounds": compounds,
                    "pit_lap": pit_lap,
                    "total_time": total_time
                })

        all_results = sorted(all_results, key=lambda x: x["total_time"])

        return all_results