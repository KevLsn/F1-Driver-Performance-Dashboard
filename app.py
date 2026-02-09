# Author : Loussouarn Kévin
# DATE : 18/10/2025
# DESCRIPTION : Streamlit app for F1 Driver Performance Dashboard

# === Imports ===
import streamlit as st
from datetime import date
import src.data.session_data as sd
import src.data.driver_data as dd
import src.visualization.plots as pl

# ==========================
# INITIAL SETUP
# ==========================
st.set_page_config(page_title="F1 Driver Performance Dashboard", page_icon="🏎️", layout="wide")
st.title("🏎️ F1 Driver Performance Dashboard")

sd.setup_fastf1_cache()

# ==========================
# SIDEBAR — FEATURE SELECTION
# ==========================
st.sidebar.header("🏎️ Feature Selection")
feature = st.sidebar.radio(
    "Select a feature",
    [
        "Overview",
        "Speed Comparison",
        "Circuit Map",
        "Championship Scenario (Coming soon)"
    ]
)

# ==========================
# SIDEBAR — SESSION SELECTION
# ==========================
# Clear session selection when switching to a feature that doesn't need it
if feature not in ["Speed Comparison", "Circuit Map"]:
    if "session" in st.session_state:
        del st.session_state.session

if feature in ["Speed Comparison", "Circuit Map"]:
    st.sidebar.divider()
    st.sidebar.subheader("📅 Session Selection")

    current_year = date.today().year
    
    year = st.sidebar.number_input("Season", min_value=2018, max_value=current_year, value=current_year, step=1)
    gp_name = st.sidebar.text_input("Grand Prix", value="Monza", help="Official Grand Prix name (e.g., 'Monza', 'Silverstone')")
    session_type = st.sidebar.selectbox("Session", ["FP1", "FP2", "FP3", "Q", "R"])

    if st.sidebar.button("Load Session"):
        with st.spinner("Loading FastF1 session..."):
            session = sd.loading_FastF1_session(year, gp_name, session_type)
            if session is None:
                st.error("Failed to load session. Please check the season, Grand Prix name, and session type.")
            else:
                # Check if session date is in the past
                try:
                    session_date = session.date.date() if hasattr(session.date, 'date') else session.date
                    if session_date > date.today():
                        st.error("⚠️ This session hasn't happened yet! Please select a past session.")
                    else:
                        st.session_state.session = session
                        st.success("Session loaded successfully!")
                except Exception as e:
                    st.error(f"Failed to validate session date: {e}")

# ==========================
# SIDEBAR — THEME SELECTION
# ==========================
if feature in ["Speed Comparison", "Circuit Map"]:
    st.sidebar.divider()
    st.sidebar.subheader("🎨 Theme Selection")
    theme_mode = st.sidebar.selectbox("Plot theme", list(sd.THEMES.keys()))
    theme = sd.THEMES[theme_mode]

# ==========================
# OVERVIEW PAGE
# ==========================
# Overview page
if feature == "Overview":
    st.header("Welcome 👋")
    st.markdown(
        """
        This dashboard allows you to explore **Formula 1 session data** using real telemetry.

        **You can:**
        - Compare the fastest laps of two drivers (speed vs distance)
        - Visualize the circuit layout
        - Explore different sessions (practice, qualifying, race)

        👉 Start by selecting a feature in the sidebar.

        Enjoy the analysis! 🏁"""
        )

# ==========================
# SPEED COMPARISON
# ==========================
elif feature == "Speed Comparison":
    st.header("📊 Speed Comparison")
    st.caption("Compare fastest lap telemetry between two drivers")

    # Check if a session is loaded
    if "session" not in st.session_state:
        st.info("👈 Please select a **season, Grand Prix, and session** from the sidebar to start Speed Comparison.")
    else:
        session = st.session_state.session

        # Display loaded session in a clean row of metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Season", year)
        col2.metric("Grand Prix", session.event["EventName"])
        col3.metric("Session", session.name)

        drivers = sorted(session.laps["Driver"].unique().tolist())
        col1, col2 = st.columns(2)

        with col1:
            driver1 = st.selectbox("Driver 1", drivers, key="driver1_select")
        with col2:
            driver2 = st.selectbox("Driver 2", [d for d in drivers if d != driver1], index=0, key="driver2_select")

        # Initialize session state for storing comparison data
        if "comparison_data" not in st.session_state:
            st.session_state.comparison_data = None

        if st.button("Generate Comparison", key="speed_comp_button"):
            with st.spinner("Analyzing telemetry..."):
                best1 = session.laps.pick_drivers(driver1).pick_fastest()
                best2 = session.laps.pick_drivers(driver2).pick_fastest()

                if not dd.laps_verification(best1, best2):
                    st.error("Invalid or missing lap data for selected drivers.")
                else:
                    tel1 = best1.get_car_data().add_distance()
                    tel2 = best2.get_car_data().add_distance()
                    circuit_info = session.get_circuit_info()

                    st.session_state.comparison_data = {
                        "tel1": tel1,
                        "tel2": tel2,
                        "best1": best1,
                        "best2": best2,
                        "circuit_info": circuit_info
                    }

        # Display comparison if data is available
        if st.session_state.comparison_data is not None:
            data = st.session_state.comparison_data
            fig = pl.plot_speed_comparison(
                data["tel1"],
                data["tel2"],
                driver1,
                driver2,
                year,
                gp_name,
                session_type,
                data["circuit_info"],
                theme
            )
            st.pyplot(fig)

            # Metrics for lap times
            m1, m2 = st.columns(2)
            m1.metric(driver1, dd.format_laptime(data["best1"]["LapTime"]))
            m2.metric(driver2, dd.format_laptime(data["best2"]["LapTime"]))

            st.info("This comparison highlights speed differences along the lap distance.")

# ==========================
# CIRCUIT MAP
# ==========================
elif feature == "Circuit Map":
    st.header("🗺️ Circuit Map")
    st.caption("Track layout and racing line visualization")

    # Check if a session is loaded
    if "session" not in st.session_state:
        st.info("👈 Please select a **season, Grand Prix, and session** from the sidebar to view the Circuit Map.")
    else:
        session = st.session_state.session

        if st.button("Show Circuit Map"):
            with st.spinner("Rendering circuit map..."):
                circuit_info = session.get_circuit_info()
                fig = pl.plot_circuit_map(circuit_info, session, theme)
            st.pyplot(fig)

# ==========================
# COMING SOON
# ==========================
elif feature.startswith("Championship"):
    st.warning("🚧 Feature not developed yet. Coming soon!")