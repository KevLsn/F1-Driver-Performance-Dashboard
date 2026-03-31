#Author : Loussouarn Kévin
#DATE : 19/03/2026
#DESCRIPTION : Lap performance metrics for F1 Driver Performance Dashboard

# === Imports ===
import pandas as pd

# Function to ensure time columns are in Timedelta format
# Input: series (pd.Series)
# Output: series in Timedelta format
# Precondition: series contains time data as strings or already in Timedelta format
# Postcondition: series is converted to Timedelta format if necessary
def _ensure_time_format(series: pd.Series) -> pd.Series:
    return pd.to_timedelta(series)

# Function to calculate best lap time
# Input: laps (pd.DataFrame)
# Output: best lap time (Timedelta)
# Precondition: laps DataFrame contains 'LapTime' column with time data
# Postcondition: best lap time is returned as a Timedelta object
def best_lap(laps: pd.DataFrame):
    laps = laps.copy()
    laps['LapTime'] = _ensure_time_format(laps['LapTime'])
    return laps['LapTime'].min()

# Function to calculate theoretical best lap time by summing best sector times
# Input: laps (pd.DataFrame)
# Output: theoretical best lap time (Timedelta)
# Precondition: laps DataFrame contains 'Sector1Time', 'Sector2Time', 'Sector3Time' columns with time data
# Postcondition: theoretical best lap time is returned as a Timedelta object representing the sum of the best sector times
def theoretical_best_lap(laps: pd.DataFrame):
    laps = laps.copy()

    laps['Sector1Time'] = _ensure_time_format(laps['Sector1Time'])
    laps['Sector2Time'] = _ensure_time_format(laps['Sector2Time'])
    laps['Sector3Time'] = _ensure_time_format(laps['Sector3Time'])

    return (
        laps['Sector1Time'].min() +
        laps['Sector2Time'].min() +
        laps['Sector3Time'].min()
    )

# Function to calculate potential gain by comparing theoretical best lap with actual best lap
# Input: laps (pd.DataFrame)
# Output: potential gain (Timedelta)
# Precondition: laps DataFrame contains necessary time columns for best lap and theoretical best lap calculations
# Postcondition: potential gain is returned as a Timedelta object representing the difference between theoretical
def potential_gain(laps: pd.DataFrame):
    theo = theoretical_best_lap(laps)
    best = best_lap(laps)

    if theo is None or best is None:
        return None

    return best - theo

# Function to calculate consistency score using standard deviation of lap times
# Input: laps (pd.DataFrame)
# Output: consistency score (Timedelta)
# Precondition: laps DataFrame contains 'LapTime' column with time data
# Postcondition: consistency score is returned as a Timedelta object representing the standard deviation of lap times, where a lower value indicates more consistency
def consistency_score(laps: pd.DataFrame):
    laps = laps.copy()
    laps['LapTime'] = _ensure_time_format(laps['LapTime'])

    return laps['LapTime'].std()

# Function to calculate average lap time
# Input: laps (pd.DataFrame)
# Output: average lap time (Timedelta)
# Precondition: laps DataFrame contains 'LapTime' column with time data
# Postcondition: average lap time is returned as a Timedelta object representing the mean of
def average_lap_time(laps: pd.DataFrame):
    laps = laps.copy()
    laps['LapTime'] = _ensure_time_format(laps['LapTime'])

    return laps['LapTime'].mean()

# Function to calculate best sector times
# Input: laps (pd.DataFrame)
# Output: dictionary of best sector times
# Precondition: laps DataFrame contains 'Sector1Time', 'Sector2Time', 'Sector3Time' columns with time data
# Postcondition: dictionary is returned with keys 'S1', 'S2', 'S3' corresponding to the best times for each sector, where each value is a Timedelta object representing the minimum time for that sector across all laps
def best_sectors(laps: pd.DataFrame):
    laps = laps.copy()

    laps['Sector1Time'] = _ensure_time_format(laps['Sector1Time'])
    laps['Sector2Time'] = _ensure_time_format(laps['Sector2Time'])
    laps['Sector3Time'] = _ensure_time_format(laps['Sector3Time'])

    return {
        "S1": laps['Sector1Time'].min(),
        "S2": laps['Sector2Time'].min(),
        "S3": laps['Sector3Time'].min(),
    }

# Function to generate a full summary of lap performance metrics for a driver
# Input: laps (pd.DataFrame)
# Output: dictionary containing all lap performance metrics
# Precondition: laps DataFrame contains necessary time columns for all metric calculations
# Postcondition: dictionary is returned with keys for each metric (best lap, theoretical best, potential gain, consistency, average lap time, best sectors) and corresponding values representing the calculated metrics,
def full_driver_summary(laps: pd.DataFrame):

    return {
        "best_lap": best_lap(laps),
        "theoretical_best": theoretical_best_lap(laps),
        "potential_gain": potential_gain(laps),
        "consistency": consistency_score(laps),
        "average_lap": average_lap_time(laps),
        "best_sectors": best_sectors(laps),
    }