#Author : Loussouarn Kévin
#DATE : 18/10/2025
#DESCRIPTION : Driver data handling for F1 Driver Performance Dashboard

from datetime import timedelta
from fastf1.core import Lap


# Function to verify both laps are valid
# Input: best1, best2 (Lap objects)
# Output: bool
# Precondition: none
# Postcondition: returns True if both laps exist
def laps_verification(best1: Lap, best2: Lap) -> bool:
    return best1 is not None and best2 is not None


# Function to format lap time
# Input: lt (timedelta)
# Output: str
# Precondition: none
# Postcondition: returns formatted lap time string
def format_laptime(lt: timedelta) -> str:
    total_ms = lt.total_seconds() * 1000
    m = int(total_ms // 60000)
    s = int((total_ms % 60000) // 1000)
    ms = int(total_ms % 1000)
    return f"{m:02}:{s:02}.{ms:03}"