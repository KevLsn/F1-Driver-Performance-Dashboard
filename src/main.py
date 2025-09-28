import fastf1
import fastf1.plotting
from matplotlib import pyplot as plt

# Enable FastF1 cache
fastf1.Cache.enable_cache('cache')

# Function to choose theme mode
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

# Function to load FastF1 session with error handling
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

# Function to choose drivers
def choose_drivers(drivers):
    #===Start===
    while True:

        driver1 = input("Enter the driver 1 name abbreviation (e.g., HAM, LEC): ").strip().upper()
        if not driver1:
            print("Input cannot be empty.")
            continue

        if driver1 not in drivers:
            print(driver1, "haven't participated.")
            continue

        break
    
    while True:

        driver2 = input("Enter the driver 2 name abbreviation (e.g., HAM, LEC): ").strip().upper()
        if not driver2:
            print("Input cannot be empty.")
            continue
    
        if driver1 == driver2:
            print("Please choose two different drivers.")
            continue
        
        if driver2 not in drivers:
            print(driver2, "haven't participated.")
            continue

        break

    return driver1, driver2

# Function to verify that laps exist
def laps_verification(best1, best2):
    #===Start===
        if best1 is None or best2 is None:
            print("No valid lap found for one of the drivers.")
            exit(1)

def plot_driver_speeds(ax, tel1, tel2, driver1, driver2):
    #===Start===
    ax.plot(tel1['Distance'], tel1['Speed'], label=driver1)
    ax.plot(tel2['Distance'], tel2['Speed'], label=driver2)

def set_plot_labels(ax, driver1, driver2, year, gp_name, session_type):
    #===Start===
    ax.set_xlabel('Distance (m)')
    ax.set_ylabel('Speed (km/h)')
    ax.set_title(f"Speed Comparison: {driver1} vs {driver2} - {year} | {gp_name} | {session_type}")
    ax.legend()

# Function to add circuit corners to the plot
def add_circuit_corners(ax, circuit_info, tel1, tel2):
    #===Start===
    v_min = min(tel1['Speed'].min(), tel2['Speed'].min())
    v_max = max(tel1['Speed'].max(), tel2['Speed'].max())

    # Add vertical lines for each corner
    ax.vlines(
        x=circuit_info.corners['Distance'],
        ymin=v_min,
        ymax=v_max,
        linestyles='dotted',
        colors='grey',
        alpha=0.6
    )

    # Add corner number labels below the lines
    for _, corner in circuit_info.corners.iterrows():
        label = f"{corner['Number']}{corner['Letter']}"
        ax.text(
        corner['Distance'],
        v_min - 30,
        label,
        va='center_baseline',
        ha='center',
        fontsize=6,  # ↓ smaller font
    )

    # Adjust y-limits to show labels clearly
    ax.set_ylim([v_min - 40, v_max + 20])

# Function to plot speed comparison
def plot_speed_comparison(tel1, tel2, driver1, driver2, year, gp_name, session_type, circuit_info):
    #===Start===
    fig, ax = plt.subplots(figsize=(12, 6))

    plot_driver_speeds(ax, tel1, tel2, driver1, driver2)
    set_plot_labels(ax, driver1, driver2, year, gp_name, session_type)

    if not circuit_info.corners.empty:
        add_circuit_corners(ax, circuit_info, tel1, tel2)

    plt.tight_layout()
    plt.show()



#===============================================================================================================================================


def main():
    #===Variables===
    #GP parameters
    year: int
    gp_name: str
    session_type: str

    #drivers abbreviations
    driver1: str    
    driver2: str
    #...
    #===Start===

    # Choose theme mode
    choose_theme_mode()

    # Choose GP
    year, gp_name, session_type = choose_gp()

    # Load FastF1 session with error handling
    session = loading_FastF1_session(year, gp_name, session_type)

    # Get circuit info
    circuit_info = session.get_circuit_info()

    # Get available drivers in session
    drivers = session.laps['Driver'].unique()
    print("Drivers in session:", drivers)

    driver1, driver2 = choose_drivers(drivers)

    # Get fastest laps (gets all laps of the driver and selects the fastest)
    laps1 = session.laps.pick_drivers(driver1)
    laps2 = session.laps.pick_drivers(driver2)
    best1 = laps1.pick_fastest()
    best2 = laps2.pick_fastest()

    # Check that laps exist
    laps_verification(best1, best2)

    # Telemetry
    tel1 = best1.get_car_data().add_distance()
    tel2 = best2.get_car_data().add_distance()

    # Plot speed comparison
    plot_speed_comparison(tel1, tel2, driver1, driver2, year, gp_name, session_type, circuit_info)

    # Display fastest laps
    print(f"{driver1} fastest lap time: {best1['LapTime']}")
    print(f"{driver2} fastest lap time: {best2['LapTime']}")
    #===End===

main()