#Author : Loussouarn Kévin
#DATE : 03/02/2026
#DESCRIPTION : Session data handling for F1 Driver Performance Dashboard

# === Imports ===
import os
from typing import Optional
import fastf1
from fastf1.core import Session


# Function to setup FastF1 cache
# Input: none
# Output: none
# Precondition: none
# Postcondition: FastF1 cache is set up
def setup_fastf1_cache() -> None:
    cache_dir = "cache"

    # Create cache directory if it doesn't exist
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    # Enable FastF1 caching
    fastf1.Cache.enable_cache(cache_dir)


# Function to load FastF1 session 
# Input: year, gp_name, session_type
# Output: session or None if loading fails
# Precondition: none
# Postcondition: session data is loaded or None is returned on error
def loading_FastF1_session(year: int, gp_name: str, session_type: str) -> Optional[Session]:
    try:
        print(f"Loading data for {gp_name} {year} - {session_type}...")
        session = fastf1.get_session(year, gp_name, session_type)
        session.load()
        return session
    except ValueError as e:
        print(f"Error: Invalid session parameters - {e}")
        return None
    except Exception as e:
        print(f"Error loading session: {e}")
        return None

# Function to get the scheduled number of laps for a GP in a given year
# Input: year (int), gp_name (str)
# Output: total laps (int) or None if unavailable
# Precondition: none
# Postcondition: returns total laps for the specified GP and year, or None if data is unavailable
def get_scheduled_race_laps(year: int, gp_name: str) -> Optional[int]:
    try:
        race_session = loading_FastF1_session(year, gp_name, "R")
        if race_session is not None:
            return race_session.event["TotalLaps"]
        else:
            return None
    except Exception as e:
        print(f"Error getting scheduled race laps: {e}")
        return None