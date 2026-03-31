# Author : Loussouarn Kévin
# DATE : 19/03/2026
# DESCRIPTION : Advanced driver performance analysis (insights, scoring, comparison)

# === Imports ===
import pandas as pd


# Function to generate a human-readable performance insight based on the potential gain metric
# Input: summary (dict containing performance metrics)
# Output: string insight
# Precondition: summary contains key 'potential_gain' with a Timedelta value
# Postcondition: a string insight is returned that categorizes the driver's performance ceiling based on the potential gain metric, where a large negative potential gain indicates a high performance ceiling (significant improvement possible
def generate_driver_insight(summary: dict) -> str:
    gain = summary["potential_gain"].total_seconds()

    if gain < -0.5:
        return "🔥 High performance ceiling — significant lap time can still be gained."
    elif gain < -0.2:
        return "⚡ Competitive performance with some room for improvement."
    elif gain < 0:
        return "📈 Small improvements possible."
    else:
        return "🏁 Driver is already close to optimal performance."


# Function to compute a driver performance score (0–100) based on consistency, potential gain, and average performance
# Input: summary (dict containing performance metrics)
# Output: float score between 0 and 100
# Precondition: summary contains keys 'consistency' (Timedelta), 'potential_gain' (Timedelta), and 'average_lap' (Timedelta)
# Postcondition: a float score is returned that quantifies the driver's overall performance, where a higher score indicates better performance, taking into account consistency (lower is better), potential gain (closer to 0 is better), and
def performance_score(summary: dict) -> float:

    gain = summary["potential_gain"].total_seconds()
    consistency = summary["consistency"].total_seconds()

    score = 100

    # Normalize consistency (typical good F1 std dev ≈ 0.2–0.6s)
    score -= min(consistency, 1) * 50

    # Penalize unused potential (but not too much)
    score -= abs(gain) * 30

    return max(0, min(100, round(score, 2)))


# Function to analyze sector performance and identify weakest sector
# Input: sectors (dict of best sector times)
# Output: string indicating weakest sector
# Precondition: sectors dictionary contains keys 'S1', 'S2', 'S3' with Timedelta values
# Postcondition: a string is returned indicating which sector is the weakest (slowest) based on the best sector times, where the sector with the highest time is identified as the weakest
def analyze_sectors(sectors: dict) -> str:

    if not sectors:
        return "N/A"

    return max(sectors, key=sectors.get)

# Function to rank sectors from fastest to slowest
# Input: sectors (dict of best sector times)
# Output: dict with ordered sectors
# Precondition: sectors dictionary contains keys for each sector (e.g., 'S1', 'S2', 'S3') with Timedelta values
# Postcondition: a dictionary is returned where the keys are the sector names and the values are the corresponding times, ordered from fastest to slowest, allowing for easy identification of sector strengths and weaknesses
def sector_strengths(sectors: dict) -> dict:

    return dict(sorted(sectors.items(), key=lambda x: x[1]))


# Function to generate a full driver report combining all analysis components
# Input: laps (pd.DataFrame), summary (dict from full_driver_summary)
# Output: dict containing insights, score, sector analysis, and lap trend
# Precondition: laps DataFrame contains necessary time columns, summary dictionary contains all required metrics
# Postcondition: a dictionary is returned that compiles a comprehensive report on the driver's performance, including a human-readable insight, a performance score, analysis of sector strengths and weaknesses, and a trend
def full_driver_report(laps: pd.DataFrame, summary: dict) -> dict:

    return {
        "insight": generate_driver_insight(summary),
        "score": performance_score(summary),
        "weakest_sector": analyze_sectors(summary["best_sectors"]),
        "sector_ranking": sector_strengths(summary["best_sectors"]),
    }