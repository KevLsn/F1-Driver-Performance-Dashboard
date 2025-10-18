#Author : Loussouarn Kévin
#DATE : 18/10/2025
#DESCRIPTION : Main script for F1 Driver Performance Dashboard

# === Imports ===
import data.session_data as sd
import data.driver_data as dd
import visualization.plots as pl

# === Main script ===
def main():
    # --- Step 1: Setup ---
    # Choose theme mode and setup FastF1 cache
    sd.choose_theme_mode()
    sd.setup_fastf1_cache()

    # Set the session
    year, gp_name, session_type = sd.choose_gp()
    print(f"Selected Grand Prix: {gp_name} {year} - {session_type}")

    session = sd.loading_FastF1_session(year, gp_name, session_type)
    print(f"Session loaded: {session.event['EventName']} {session.name}")

    # --- Step 2: Drivers ---
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
    dd.laps_verification(best1, best2)


    # --- Step 3: Plotting ---
    # Get circuit info
    circuit_info = session.get_circuit_info()

    # Telemetry
    tel1 = best1.get_car_data().add_distance()
    tel2 = best2.get_car_data().add_distance()

    # Plot speed comparison
    pl.plot_speed_comparison(tel1, tel2, driver1, driver2, year, gp_name, session_type, circuit_info)
    print("Plot generated successfully!")

    # --- Step 4: Display Results ---
    # Display fastest laps
    print(f"{driver1} fastest lap time: {best1['LapTime']}")
    print(f"{driver2} fastest lap time: {best2['LapTime']}")

    # --- Step 5: Additional Telemetry Comparisons ---
    # Display additional telemetry comparisons (time gaps, sector times, etc.)
    #===TO DO===

    #===End===

# === Entry point ===
if __name__ == "__main__":
    main()