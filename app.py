# Author : Loussouarn Kévin
# DATE : 18/10/2025
# DESCRIPTION : Streamlit app for F1 Driver Performance Dashboard

# === Imports ===
import streamlit as st
import src.data.session_data as sd
import src.data.driver_data as dd
import src.visualization.plots as pl

# ==========================
# INITIAL SETUP
# ==========================
st.set_page_config(page_title="F1 Driver Performance Dashboard", layout="wide")
st.title("🏎️ F1 Driver Performance Dashboard")

sd.setup_fastf1_cache()

# Function to load FastF1 session with caching
# Input: year, gp_name, session_type
# Output: session
# Precondition: none
# Postcondition: FastF1 session is loaded and returned
@st.cache_data(show_spinner=False)
def load_session(year, gp_name, session_type):
    return sd.loading_FastF1_session(year, gp_name, session_type)

# ==========================
# FEATURE SELECTION
# ==========================
st.sidebar.header("Feature Selection")

feature = st.sidebar.radio(
    "What do you want to do ?",
    [
        "Speed Comparison",
        "Circuit Map",
        "Championship Scenario (Coming soon)"
    ]
)

# Plot theme selection)
st.sidebar.divider()
theme_mode = st.sidebar.selectbox("Plot theme", list(sd.THEMES.keys()))
theme = sd.THEMES[theme_mode]

# ==========================
# SESSION SELECTION
# ==========================
st.sidebar.divider()
st.sidebar.header("Session Selection")

year = st.sidebar.number_input("Year", min_value=2018, max_value=2025, value=2025)
gp_name = st.sidebar.text_input("Grand Prix", value="Monza")
session_type = st.sidebar.selectbox("Session Type", ["FP1", "FP2", "FP3", "Q", "R"])

if st.sidebar.button("Load Session"):
    with st.spinner("Loading FastF1 session..."):
        session = load_session(year, gp_name, session_type)
        st.session_state.session = session
    st.success(f"{session.event['EventName']} {session.name} loaded")

# ==========================
# MAIN CONTENT
# ==========================
if "session" not in st.session_state:
    st.info("Please choose a feature and load a session from the sidebar.")
    st.stop()

session = st.session_state.session

# ==========================
# SPEED COMPARISON
# ==========================
if feature == "Speed Comparison":
    st.header("📊 Speed Comparison")

    drivers = session.laps["Driver"].unique().tolist()

    col1, col2 = st.columns(2)
    with col1:
        driver1 = st.selectbox("Driver 1", drivers)
    with col2:
        driver2 = st.selectbox("Driver 2", [d for d in drivers if d != driver1])

    if st.button("Generate Comparison"):
        best1 = session.laps.pick_drivers(driver1).pick_fastest()
        best2 = session.laps.pick_drivers(driver2).pick_fastest()

        if not dd.laps_verification(best1, best2):
            st.error("Invalid laps for selected drivers.")
        else:
            tel1 = best1.get_car_data().add_distance()
            tel2 = best2.get_car_data().add_distance()
            circuit_info = session.get_circuit_info()

            fig = pl.plot_speed_comparison(tel1, tel2, driver1, driver2, year, gp_name, session_type, circuit_info, theme)
            st.pyplot(fig)

            st.metric(driver1, dd.format_laptime(best1["LapTime"]))
            st.metric(driver2, dd.format_laptime(best2["LapTime"]))

            st.info("Additional telemetry comparisons coming soon!")

# ==========================
# CIRCUIT MAP
# ==========================
elif feature == "Circuit Map":
    st.header("🗺️ Circuit Map")

    if st.button("Show Circuit Map"):
        circuit_info = session.get_circuit_info()
        fig = pl.plot_circuit_map(circuit_info, session, theme)
        st.pyplot(fig)

# ==========================
# COMING SOON
# ==========================
elif feature.startswith("Championship"):
    st.warning("Feature not developed yet. Coming soon!")