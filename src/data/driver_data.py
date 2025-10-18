#Author : Loussouarn Kévin
#DATE : 18/10/2025
#DESCRIPTION : Driver data handling for F1 Driver Performance Dashboard

# Function to choose drivers
# Input: drivers (list of available drivers by their abbreviations)
# Output: driver1, driver2 (selected drivers' abbreviations)
# Precondition: none
# Postcondition: two different valid drivers are selected
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
# Input: best1, best2 (best laps for each driver)
# Output: none
# Precondition: none
# Postcondition: exits if one of the laps does not exist
def laps_verification(best1, best2):
    #===Start===
        if best1 is None or best2 is None:
            print("No valid lap found for one of the drivers.")
            exit(1)