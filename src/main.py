#Author : Loussouarn Kévin
#DATE : 18/10/2025
#DESCRIPTION : Main script for F1 Driver Performance Dashboard

# === Imports ===
import data.session_data as sd
import data.driver_data as dd
import visualization.plots as pl
import data.menu as menu

# ==========================
# FEATURE FUNCTIONS
# ==========================

# Function to setup and load a FastF1 session
# Input: none
# Output: session, year, gp_name, session_type
# Precondition: none
# Postcondition: FastF1 session is loaded and returned
def setup_session():

    year, gp_name, session_type = sd.choose_gp()
    print(f"Selected Grand Prix: {gp_name} {year} - {session_type}")

    session = sd.loading_FastF1_session(year, gp_name, session_type)
    print(f"Session loaded: {session.event['EventName']} {session.name}")

    return session, year, gp_name, session_type

# Function to run speed comparison feature
# Input: theme
# Output: none
# Precondition: none
# Postcondition: none
def run_speed_comparison(session, year, gp_name, session_type, theme):

    # --- Step 1: Drivers ---
    # Get available drivers in session
    drivers_list = session.laps['Driver'].unique()
    print("Drivers in session:", drivers_list)

    # Choose drivers
    driver1, driver2 = dd.choose_drivers(drivers_list)
    print(f"Selected Drivers: {driver1} - {driver2}")

    # Get the best laps for each driver
    best1 = session.laps.pick_drivers(driver1).pick_fastest()
    best2 = session.laps.pick_drivers(driver2).pick_fastest()

    # Verify that laps exist
    if not dd.laps_verification(best1, best2):
        print("Invalid laps for selected drivers.")
        return

    # --- Step 2: Plotting ---
    # Telemetry
    tel1 = best1.get_car_data().add_distance()
    tel2 = best2.get_car_data().add_distance()

    # Get circuit info
    circuit_info = session.get_circuit_info()

    # Plot speed comparison
    pl.plot_speed_comparison(tel1, tel2, driver1, driver2, year, gp_name, session_type, circuit_info, theme)
    print("Plot generated successfully!")

    # --- Step 4: Display Results ---
    # Display fastest laps
    print(f"{driver1} fastest lap time: {dd.format_laptime(best1['LapTime'])}")
    print(f"{driver2} fastest lap time: {dd.format_laptime(best2['LapTime'])}")

    # --- Step 5: Additional Telemetry Comparisons ---
    # Display additional telemetry comparisons (time gaps, sector times, etc.)
    #===TO DO===
    print("\nAdditional telemetry comparisons feature not developed yet. Coming soon!\n")
            
# Function to run circuit map feature
# Input: theme
# Output: none
# Precondition: none
# Postcondition: none            
def run_circuit_map(session, theme):

    circuit_info = session.get_circuit_info()
    pl.plot_circuit_map(circuit_info, session, theme)

# ==========================
# MAIN LOOP
# ==========================
def main():
    theme_mode = "bright"
    theme = sd.THEMES[theme_mode]

    sd.setup_fastf1_cache()
    running = True

    while running:
        choice = menu.main_menu()

        # Speed comparison menu
        if choice == "1":
            subchoice = menu.speed_comparison_menu()

            # Speed comparison only
            if subchoice == "1":
                session, year, gp_name, session_type = setup_session()
                run_speed_comparison(session, year, gp_name, session_type, theme)

            # Speed comparison + circuit map
            elif subchoice == "2":
                session, year, gp_name, session_type = setup_session()
                run_speed_comparison(session, year, gp_name, session_type, theme)
                run_circuit_map(session, theme)

            # Back to main menu
            elif subchoice == "3":
                continue

        # Championship scenario (coming soon)        
        elif choice == "2":
            print("\nFeature not developed yet. Coming soon!\n")

        # Track map
        elif choice == "3":
            session, year, gp_name, session_type = setup_session()
            run_circuit_map(session, theme)

        # Change theme/colors
        elif choice == "4":
            theme_mode, theme = sd.choose_theme_mode()

        # Exit
        elif choice == "0":
            print("Exiting Dashboard.")
            running = False

# === Entry point ===
if __name__ == "__main__":
    main()