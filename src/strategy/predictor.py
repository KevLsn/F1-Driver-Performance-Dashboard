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
    # Input: sessions (dict of session_type -> Session), driver (str)
    # Output: Predictor object
    # Precondition: sessions must contain at least one practice session
    # Postcondition: Predictor object is initialized with session selection
    def __init__(self, sessions: Dict[str, Session], driver: str):
        self.sessions = sessions
        self.driver = driver
        self.parameters = {}

    # Extract long stints per tyre compound
    # Input: min_laps (int) – minimum number of laps to consider a stint
    # Output: Dict[compound -> list of DataFrames], each DataFrame = stint
    # Precondition: session contains laps with valid LapTime and Compound data
    # Postcondition: Only stints with at least min_laps laps are returned
    def extract_long_runs(self, min_laps: int = 3) -> Dict[str, List[pd.DataFrame]]:

        # Combine all laps from all sessions for the driver
        all_laps = pd.DataFrame()

        # Loop through all sessions
        for session_name, session in self.sessions.items():
            if not hasattr(session, 'laps') or session.laps is None:
                continue

            laps = session.laps.pick_drivers(self.driver).reset_index()
            laps['session'] = session_name  # optional: track which session each lap comes from
            all_laps = pd.concat([all_laps, laps], ignore_index=True)

        if all_laps.empty:
            raise ValueError(f"No laps found for driver {self.driver} in any session.")

        # Filter invalid laps
        laps = laps[laps['LapTime'].notna()]
        # Filter out non-green laps (e.g. yellow flags, safety car)
        if 'TrackStatus' in laps.columns: 
            laps = laps[laps['TrackStatus'] == '1']

        # Convert lap time to seconds for easier calculations
        laps["LapSeconds"] = laps["LapTime"].dt.total_seconds()

        # Remove extreme slow laps (likely pit / traffic)
        median_pace = laps["LapSeconds"].median()
        laps = laps[laps["LapSeconds"] < median_pace * 1.2]

        # Group by compound and stint, only keep stints with at least min_laps laps
        stints_dict = {}
        for compound in laps["Compound"].dropna().unique():

            compound_laps = laps[laps["Compound"] == compound]
            stints = []
            for stint_number, stint_df in compound_laps.groupby("Stint"):
                if len(stint_df) >= min_laps:
                    stints.append(stint_df.copy())

            if stints:
                stints_dict[compound] = stints

        return stints_dict

    # Estimate base pace, degradation, and variance per compound
    # Input: none
    # Output: Dict[compound -> dict with keys 'base_pace', 'degradation', 'variance']
    # Precondition: extract_long_runs must return at least one valid stint
    # Postcondition: self.parameters is populated and returned
    def estimate_parameters(self) -> Dict[str, Dict[str, float]]:

        # Extract stints
        stints = self.extract_long_runs()
        params = {}

        # For each compound, fit a linear model to lap times vs lap number to estimate degradation
        for compound, stint_list in stints.items():

            # Collect lap times and fit linear regression for each stint, then average results
            slopes = []
            intercepts = []
            all_times = []

            for stint in stint_list:
                lap_times = stint['LapTime'].dt.total_seconds().values
                if len(lap_times) < 2:
                    continue

                x = np.arange(len(lap_times))
                y = lap_times

                A = np.vstack([x, np.ones(len(x))]).T
                slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]

                slopes.append(slope)
                intercepts.append(intercept)
                all_times.extend(y)

            if not slopes:
                continue

            params[compound] = {
                "base_pace": timedelta(seconds=float(np.mean(intercepts))),      
                "degradation": float(np.mean(slopes)),                           
                "variance": float(np.std(all_times))                             
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