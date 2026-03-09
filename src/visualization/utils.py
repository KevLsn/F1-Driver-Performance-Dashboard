# utils.py
# Author: Loussouarn Kévin
# Date: 07/03/2026
# Description: Utility functions for F1 Driver Performance Dashboard

# Utility functions for formatting time values in the dashboard.
# Input: seconds (float)
# Output: formatted time string (str)
# Precondition: seconds is a non-negative float
# Postcondition: returns a formatted time string
def format_total(seconds: float) -> str:
    hours, remainder = divmod(seconds, 3600)
    minutes, sec = divmod(remainder, 60)
    if hours > 0:
        return f"{int(hours)}h {int(minutes)}m {sec:.2f}s"
    else:
        return f"{int(minutes)}m {sec:.2f}s"

#
# Input: seconds (float)
# Output: formatted time string (str)
# Precondition: seconds is a non-negative float
# Postcondition: returns a formatted time string
def format_delta(seconds: float) -> str:
    if seconds == 0:
        return "–"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    else:
        minutes, sec = divmod(seconds, 60)
        return f"{int(minutes)}m {sec:.2f}s"