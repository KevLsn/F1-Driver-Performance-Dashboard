#Author : Loussouarn Kévin
#DATE : 18/10/2025
#DESCRIPTION : Session data handling for F1 Driver Performance Dashboard

# === Imports ===
import fastf1

# Theme definitions
THEMES = {
    "bright": {
        "primary": "#1a1a1a",
        "secondary": "#d62728",
        "background": "#f0f0f0",
        "track": "#1a1a1a",
        "text": "#000000"
    },

    "dark": {
        "primary": "#ffffff",
        "secondary": "#ff4c4c",
        "background": "#121212",
        "track": "#ffffff",
        "text": "#ffffff"
    },

    "mercedes": {
        "primary": "#00D2BE",
        "secondary": "#C0C0C0",
        "background": "#0e0e0e",
        "track": "#00D2BE",
        "text": "#ffffff"
    },

    "redbull": {
        "primary": "#0600EF",
        "secondary": "#EF1C24",
        "background": "#0e0e0e",
        "track": "#0600EF",
        "text": "#ffffff"
    },

    "ferrari": {
        "primary": "#FA2C2C",
        "secondary": "#FFD700",
        "background": "#0e0e0e",
        "track": "#FA2C2C",
        "text": "#ffffff"
    },

    "mclaren": {
        "primary": "#FF5C00",
        "secondary": "#1a1a1a",
        "background": "#0e0e0e",
        "track": "#FF5C00",
        "text": "#ffffff"
    }
}

# Enable FastF1 cache
# Input: none
# Output: none
# Precondition: none
# Postcondition: FastF1 cache is enabled in 'cache' directory
def setup_fastf1_cache():
    fastf1.Cache.enable_cache('cache')

# Function to load FastF1 session 
# Input: year, gp_name, session_type
# Output: session
# Precondition: none
# Postcondition: session data is loaded
def loading_FastF1_session(year, gp_name, session_type):
    #===Start===
    try:
        print(f"Loading data for {gp_name} {year} - {session_type}...")
        session = fastf1.get_session(year, gp_name, session_type)
        session.load()
        return session
    except Exception as e:
        print(f"Error loading session: {e}")
        exit(1)

