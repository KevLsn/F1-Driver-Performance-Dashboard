#Author : Loussouarn Kévin
#DATE : 18/10/2025
#DESCRIPTION : Visualization plots for F1 Driver Performance Dashboard

# === Imports ===
import fastf1.plotting
from matplotlib import pyplot as plt
import numpy as np

# ============================
# Speed Comparison Components
# ============================

# Function to plot speed comparison
# Input: tel1, tel2, driver1, driver2, year, gp_name, session_type, circuit_info
# Output: none
# Precondition: none
# Postcondition: speed comparison plot is displayed
def plot_speed_comparison(tel1, tel2, driver1, driver2, year, gp_name, session_type, circuit_info, THEME):
    #===Start===
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot driver speeds
    ax.plot(tel1['Distance'], tel1['Speed'], label=driver1, color=THEME['primary'])
    ax.plot(tel2['Distance'], tel2['Speed'], label=driver2, color=THEME['secondary'])

    # Set labels and title
    ax.set_xlabel('Distance (m)')
    ax.set_ylabel('Speed (km/h)')
    ax.set_title(f"Speed Comparison: {driver1} vs {driver2} - {year} | {gp_name} | {session_type}")
    ax.legend()

    if not circuit_info.corners.empty:
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
                fontsize=6,
            )

        # Adjust y-limits to show labels clearly
        ax.set_ylim([v_min - 40, v_max + 20])

    plt.tight_layout()
    plt.show()


# ============================
# Circuit Map Components
# ============================

# Function to rotate coordinates by a given angle
# Input: xy (coordinates), angle (rotation angle in radians)
# Output: rotated coordinates
# Precondition: none
# Postcondition: coordinates are rotated by the specified angle
# Credit to FastF1 library
def rotate(xy, *, angle):
    rot_mat = np.array([[np.cos(angle), np.sin(angle)],
                        [-np.sin(angle), np.cos(angle)]])
    return np.matmul(xy, rot_mat)

# Function to plot circuit map (inspired by FastF1 library)
# Input: circuit_info, session
# Output: none
# Precondition: none
# Postcondition: circuit map is displayed
def plot_circuit_map(circuit_info, session, THEME):
    #===Start===
    # === Setup figure ===
    fig, ax = plt.subplots(figsize=(8, 8))

    # === Get fastest lap position data ===
    lap = session.laps.pick_fastest()
    pos = lap.get_pos_data()

    # Extract track coordinates
    # Get an array of shape [n, 2] where n is the number of points and the second
    # axis is x and y.
    track = pos.loc[:, ('X', 'Y')].to_numpy()

    # Close the track loop to avoid gap
    track = np.vstack([track, track[0]])

    # Remove NaN values that may be present in the position data.
    track = track[~np.isnan(track).any(axis=1)]

    # Convert the rotation angle from degrees to radian.
    track_angle = circuit_info.rotation / 180 * np.pi

    # Rotate and plot the track map.
    rotated_track = rotate(track, angle=track_angle)
    ax.plot(
        rotated_track[:, 0],
        rotated_track[:, 1],
        color=THEME["track"],
        linewidth=2.5
    )

    offset_vector = [500, 0]  # offset length is chosen arbitrarily to 'look good'

    # Iterate over all corners.
    for _, corner in circuit_info.corners.iterrows():
        # Create a string from corner number and letter
        txt = f"{corner['Number']}{corner['Letter']}"

        # Convert the angle from degrees to radian.
        offset_angle = corner['Angle'] / 180 * np.pi

        # Rotate the offset vector so that it points sideways from the track.
        offset_x, offset_y = rotate(offset_vector, angle=offset_angle)

        # Add the offset to the position of the corner
        text_x = corner['X'] + offset_x
        text_y = corner['Y'] + offset_y

        # Rotate the text position equivalently to the rest of the track map
        text_x, text_y = rotate([text_x, text_y], angle=track_angle)

        # Rotate the center of the corner equivalently to the rest of the track map
        track_x, track_y = rotate([corner['X'], corner['Y']], angle=track_angle)

        # Finally, print the corner number.
        ax.text(
            text_x,
            text_y,
            txt,
            va='center',
            ha='center',
            size=9,
            color=THEME["text"]
        )

    ax.set_facecolor(THEME["background"])
    fig.patch.set_facecolor(THEME["background"])

    # Visual formatting
    ax.set_title(f"Track Map — {session.event['EventName']} {session.name}", color=THEME["text"])
    plt.xticks([])
    plt.yticks([])
    plt.axis('equal')
    plt.show()