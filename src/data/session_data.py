#Author : Loussouarn Kévin
#DATE : 18/10/2025
#DESCRIPTION : Session data handling for F1 Driver Performance Dashboard
import fastf1

# Enable FastF1 cache
# Input: none
# Output: none
# Precondition: none
# Postcondition: FastF1 cache is enabled in 'cache' directory
def setup_fastf1_cache():
    fastf1.Cache.enable_cache('cache')


# Function to choose theme mode
# Input: none
# Output: the selected mode ('bright' or 'dark')
# Precondition: none
# Postcondition: the matplotlib theme is set according to user choice
def choose_theme_mode():
    #===Start===
    while True:
        mode = input("Choose plot theme mode ('bright' or 'dark'): ").strip().lower()
        if mode in ('dark', 'bright'):
            # Setup matplotlib theme based on user choice
            if mode == 'dark':
                fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme='fastf1')
            else:
                fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme='fastf1-bright')
            return mode
        else:
            print("Invalid input. Please enter 'bright' or 'dark'.")

# Function to choose the GP
# Input: x
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

