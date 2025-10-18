#Author : Loussouarn Kévin
#DATE : 18/10/2025
#DESCRIPTION : Visualization plots for F1 Driver Performance Dashboard
import fastf1.plotting
from matplotlib import pyplot as plt

# Function to plot the speeds of two drivers
# Input: ax, tel1, tel2, driver1, driver2
# Output: none
# Precondition: none 
# Postcondition: the speeds of both drivers are plotted on the given axis
def plot_driver_speeds(ax, tel1, tel2, driver1, driver2):
    #===Start===
    ax.plot(tel1['Distance'], tel1['Speed'], label=driver1)
    ax.plot(tel2['Distance'], tel2['Speed'], label=driver2)

# Function to set plot labels and title
# Input: ax, driver1, driver2, year, gp_name, session_type
# Output: none
# Precondition: none
# Postcondition: the plot is labeled and titled appropriately
def set_plot_labels(ax, driver1, driver2, year, gp_name, session_type):
    #===Start===
    ax.set_xlabel('Distance (m)')
    ax.set_ylabel('Speed (km/h)')
    ax.set_title(f"Speed Comparison: {driver1} vs {driver2} - {year} | {gp_name} | {session_type}")
    ax.legend()

# Function to add circuit corners to the plot
# Input: ax, circuit_info, tel1, tel2
# Output: none
# Precondition: none
# Postcondition: circuit corners are added to the plot
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
        fontsize=6,  # ↓ smaller font so the corner numbers don't overlap
    )

    # Adjust y-limits to show labels clearly
    ax.set_ylim([v_min - 40, v_max + 20])

# Function to plot speed comparison
# Input: tel1, tel2, driver1, driver2, year, gp_name, session_type, circuit_info
# Output: none
# Precondition: none
# Postcondition: speed comparison plot is displayed
def plot_speed_comparison(tel1, tel2, driver1, driver2, year, gp_name, session_type, circuit_info):
    #===Start===
    fig, ax = plt.subplots(figsize=(12, 6))

    plot_driver_speeds(ax, tel1, tel2, driver1, driver2)
    set_plot_labels(ax, driver1, driver2, year, gp_name, session_type)

    if not circuit_info.corners.empty:
        add_circuit_corners(ax, circuit_info, tel1, tel2)

    plt.tight_layout()
    plt.show()