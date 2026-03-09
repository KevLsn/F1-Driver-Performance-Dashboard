# Author: Loussouarn Kévin
# Date: 25/02/2026
# Description: Strategy optimizer for race simulation engine

from typing import List, Dict
from .race_engine import RaceEngine
from itertools import permutations

# Maximum realistic stint lengths per compound (laps)
MAX_STINT_LENGTH = {
    "SOFT": 30,   
    "MEDIUM": 50,  
    "HARD": 70,   
    "INTER": 40,   
    "WET": 25 
}

# Optimizer for race strategies.
class StrategyOptimizer:

    # Constructor
    # Input: engine (RaceEngine object)
    # Output: StrategyOptimizer object
    # Precondition: engine is initialized
    # Postcondition: Optimizer ready to search strategies
    def __init__(self, engine: RaceEngine):
        self.engine = engine

    # Check if a 1-stop strategy is physically realistic
    # Input: compounds (list of 2 str), pit_lap (int)
    # Output: bool (True if valid)
    # Precondition: compounds has 2 elements
    # Postcondition: returns True if both stints are within max lengths
    def is_valid_strategy(self, compounds: List[str], pit_lap: int) -> bool:

        # First stint: lap 1 to pit_lap
        stint1_length = pit_lap
        if compounds[0] not in MAX_STINT_LENGTH:
            raise ValueError(f"Unknown compound: {compounds[0]}")
        if stint1_length > MAX_STINT_LENGTH[compounds[0]]:
            return False
        
        # Second stint: lap (pit_lap + 1) to race_laps
        stint2_length = self.engine.race_laps - pit_lap
        if compounds[1] not in MAX_STINT_LENGTH:
            raise ValueError(f"Unknown compound: {compounds[1]}")
        if stint2_length > MAX_STINT_LENGTH[compounds[1]]:
            return False
        
        return True

    # Generate 1-Stop Combinations
    # Input: available_compounds (list of str)
    # Output: list of compound sequences
    # Precondition: at least 2 compounds available
    # Postcondition: returns all possible 2-compound sequences
    def generate_1stop_combinations(self, available_compounds: List[str]) -> List[List[str]]:
        if len(available_compounds) < 2:
            raise ValueError("At least 2 compounds required to generate 1-stop combinations")
        return [list(p) for p in permutations(available_compounds, 2)]

    # Compute and rank all 1-stop strategies
    # Input: available_compounds (list of str), min_pit_lap (int), max_pit_lap (int), monte_carlo (bool), n_simulations (int)
    # Output: list of strategies sorted by total_time
    # Precondition: min_pit_lap < max_pit_lap
    # Postcondition: returns ranked strategy list with realistic stints only
    def optimize_1stop(self, available_compounds: List[str], min_pit_lap: int, max_pit_lap: int, monte_carlo: bool = True, n_simulations: int = 100) -> List[Dict]:
        
        # If fewer than 2 compounds, return empty list (cannot do 1-stop)
        if len(available_compounds) < 2:
            return []
        
        all_results = []
        combinations = self.generate_1stop_combinations(available_compounds)

        for compounds in combinations:
            for pit_lap in range(min_pit_lap, max_pit_lap + 1):
                # Skip unrealistic strategies (stints too long for compound)
                if not self.is_valid_strategy(compounds, pit_lap):
                    continue

                if monte_carlo:
                    # Run Monte Carlo to get mean total time
                    sim_result = self.engine.simulate_monte_carlo(compounds, [pit_lap], n_simulations=n_simulations)
                    total_time = sim_result['mean_time']
                    std_time = sim_result['std_time']
                else:
                    total_time = self.engine.simulate_strategy(compounds, [pit_lap])
                    std_time = 0.0
                
                all_results.append({
                    "compounds": compounds,
                    "pit_lap": pit_lap,
                    "total_time": total_time,
                    "std_time": std_time
                })

        return sorted(all_results, key=lambda x: x["total_time"])