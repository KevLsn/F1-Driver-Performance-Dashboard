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

# Format a time delta in seconds to a human-readable string with appropriate units.
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
    
# Format a timedelta object to a string in the format "M:SS.sss"
# Input: td (Timedelta)
# Output: formatted time string (str)
# Precondition: td is a pandas Timedelta object
# Postcondition: returns a formatted time string in the format "M:SS.sss"    
def fmt(td):
    if td is None:
        return "N/A"
                
    total_seconds = td.total_seconds()

    minutes = int(total_seconds // 60)
    seconds = total_seconds % 60

    return f"{minutes}:{seconds:05.3f} s"

# Format a timedelta object to a string showing the difference in seconds with a "+" or "-" sign
# Input: td (Timedelta)
# Output: formatted time string (str)
# Precondition: td is a pandas Timedelta object
# Postcondition: returns a formatted time string showing the difference in seconds with a "+" or "-" sign, or "N/A" if td is None
def fmt_delta(td):
    if td is None:
        return "N/A"
                
    seconds = td.total_seconds()
    return f"{seconds:+.3f} s"