#Author : Loussouarn Kévin
#DATE : 18/10/2025
#DESCRIPTION : Menu definitions for F1 Driver Performance Dashboard

# Function to display main menu and get user choice
# Input: none
# Output: choice (user's menu choice)
# Precondition: none
# Postcondition: returns the user's choice from the main menu
def main_menu():
    print("\n=== F1 Driver Performance Dashboard Menu ===")
    print("1. Speed Comparison")
    print("2. Championship Scenario (coming soon)")
    print("3. Track map ")
    print("4. Change Colors / Theme")
    print("0. Exit")

    while True:
        choice = input("Choose an option (0-4): ")
        if choice in ["0", "1", "2", "3", "4"]:
            return choice
        print("Invalid choice, try again.")

        
# Function to display speed comparison submenu and get user choice
# Input: none
# Output: sub (user's submenu choice)
# Precondition: none
# Postcondition: returns the user's choice from the speed comparison submenu
def speed_comparison_menu():
    print("\n=== Speed Comparison Options ===")
    print("1. Speed comparison only")
    print("2. Speed comparison + circuit map")
    print("3. Back to main menu")

    while True:
        sub = input("Choose an option (1-3): ")

        if sub in ["1", "2", "3"]:
            return sub
        print("Invalid choice, try again.")
