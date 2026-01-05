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


# Function to choose theme mode
# Input: none
# Output: mode, theme_colors (selected mode and corresponding colors)
# Precondition: none
# Postcondition: theme mode is chosen and applied
def choose_theme_mode():
    #===Start===
    while True:
        mode = input("Choose theme mode ('bright', 'dark', 'Mercedes', 'McLaren', 'RedBull', 'Ferrari'): ").strip().lower()
        if mode in THEMES:
            # Apply FastF1 plotting style for base brightness
            if mode in ("dark", "redbull", "ferrari", "mercedes", "mclaren"):
                fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme='fastf1')
            else:
                fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme='fastf1-bright')
            return mode, THEMES[mode]
        else:
            print("Invalid choice. Pick from: " + ", ".join(THEMES.keys()))


# Function to choose the GP
# Input: none
# Output: year, gp_name, session_type
# Precondition: none
# Postcondition: none
def choose_gp():
    #===Start===
    while True:
        try:
            year = int(input("Enter the year of the GP (e.g., 2025): "))
            gp_name = input("Enter the name of the GP (e.g., Monza, Silverstone): ").strip()
            session_type = input("Session type (R = Race, Q = Qualifying, FP1 = Practice 1): ").strip().upper()
            # Validate inputs
            if session_type not in ['R', 'Q', 'FP1', 'FP2', 'FP3']:
                raise ValueError("Invalid session type")
            return year, gp_name, session_type
        except ValueError as e:
            print(f"Error: {e}. Please try again.")

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

