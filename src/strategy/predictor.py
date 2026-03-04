# Author: Loussouarn Kévin
# Date: 25/02/2026
# Description: Predictor module for practice-based F1 race strategy engine

# === Imports ===
from typing import Dict, List
from datetime import timedelta
import pandas as pd
import numpy as np
from fastf1.core import Session

# Extract predictive parameters from practice sessions for a single driver.
# This module builds a model that can predict race performance.
class Predictor:

    # Constructor
    # Input: sessions (dict of session_type -> Session), driver (driver code string)
    # Output: Predictor object
    # Precondition: sessions must contain at least one practice session
    # Postcondition: Predictor object is initialized with session selection
    def __init__(self, sessions: Dict[str, Session], driver: str):
        self.sessions = sessions
        self.driver = driver
        self.session = self.select_practice_session()
        self.parameters = {}

    # Select the most representative practice session
    # Input: none
    # Output: Session object
    # Precondition: sessions dict contains at least FP1 or FP2
    # Postcondition: Returns FP2 if available, else FP1
    def select_practice_session(self) -> Session:
        for key in ["Practice 2", "Practice 1"]:
            if key in self.sessions:
                return self.sessions[key]
        raise ValueError("No practice session available for prediction")

    # Extract long stints per tyre compound
    # Input: min_laps (int) – minimum number of laps to consider a stint
    # Output: Dict[compound -> list of DataFrames], each DataFrame = stint
    # Precondition: session contains laps with valid LapTime and TyreCompound
    # Postcondition: Only stints with at least min_laps laps are returned
    def extract_long_runs(self, min_laps: int = 3) -> Dict[str, List[pd.DataFrame]]:

        # Get laps for the driver
        laps = self.session.laps.pick_drivers(self.driver).reset_index()
        
        # Filter invalid laps
        laps = laps[laps['LapTime'].notna()]
        if 'TrackStatus' in laps.columns: # Filter out non-green laps
            laps = laps[laps['TrackStatus'] == '1']

        # Convert lap time to seconds
        laps["LapSeconds"] = laps["LapTime"].dt.total_seconds()

        # Remove outliers: keep laps within ±7% of median pace
        median_pace = laps["LapSeconds"].median()
        laps = laps[(laps["LapSeconds"] >= median_pace * 0.93) & (laps["LapSeconds"] <= median_pace * 1.07)]


        stints_dict = {}
        for compound in laps["Compound"].dropna().unique():

            compound_laps = laps[laps["Compound"] == compound]
            stints = []
            for stint_number, stint_df in compound_laps.groupby("Stint"):
                if len(stint_df) >= min_laps:
                    stints.append(stint_df.copy())

            if stints:
                stints_dict[compound] = stints

        print(laps[["LapNumber", "Stint", "Compound", "LapTime"]])

        return stints_dict

    # Estimate base pace, degradation, and variance per compound
    # Input: none
    # Output: Dict[compound -> dict with keys 'base_pace', 'degradation', 'variance']
    # Precondition: extract_long_runs must return at least one valid stint
    # Postcondition: self.parameters is populated and returned
    def estimate_parameters(self) -> Dict[str, Dict[str, float]]:
        stints = self.extract_long_runs()
        params = {}
        for compound, stint_list in stints.items():
            all_laps = []
            for stint in stint_list:
                all_laps.append(stint['LapTime'].dt.total_seconds().values)
            if not all_laps:
                continue
            lap_times = np.concatenate(all_laps)
            x = np.arange(len(lap_times))
            y = lap_times
            if len(x) < 2:
                continue
            A = np.vstack([x, np.ones(len(x))]).T
            slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]
            variance = float(np.std(y))
            params[compound] = {
                "base_pace": timedelta(seconds=float(intercept)),
                "degradation": float(slope),
                "variance": variance
            }
        self.parameters = params
        return params

    # Return estimated parameters, compute if not already done
    # Input: none
    # Output: Dict[compound -> dict with keys 'base_pace', 'degradation', 'variance']
    # Precondition: self.session is set
    # Postcondition: returns dict of predictive parameters per compound
    def get_parameters(self) -> Dict[str, Dict[str, float]]:
        if not self.parameters:
            self.estimate_parameters()
        return self.parameters