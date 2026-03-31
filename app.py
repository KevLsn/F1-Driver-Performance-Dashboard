# Author : Loussouarn Kévin
# DATE : 03/02/2026
# DESCRIPTION : Streamlit app for F1 Driver Performance Dashboard

# === Imports ===
import streamlit as st
from datetime import date
import src.data.session_data as sd
import src.data.driver_data as dd
import src.visualization.plots as pl
import src.strategy.predictor as sp
import src.strategy.race_engine as sr
import src.strategy.optimizer as so
import src.visualization.utils as vu
import src.visualization.theme as vt
import src.analysis.lap_metrics as al
import src.analysis.driver_performance as ad
import pandas as pd

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
        "Circuit Map",
        "Speed Comparison",
        "Position Changes",
        "Driver Analysis",
        "Race Strategy Engine",
        "Championship Scenario (Coming soon)"
    ]
)

# ==========================
# SIDEBAR — SESSION SELECTION
# ==========================
if feature in ["Speed Comparison", "Circuit Map", "Position Changes", "Race Strategy Engine", "Driver Analysis"]:
    st.sidebar.divider()
    st.sidebar.subheader("📅 Session Selection")

    # Pre-fill a session for quick testing
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
                try:
                    session_date = session.date.date() if hasattr(session.date, 'date') else session.date
                    if session_date > date.today():
                        st.error("⚠️ This session hasn't happened yet! Please select a past session.")
                    else:
                        st.session_state.session = session
                        st.success("Session loaded successfully!")
                except Exception as e:
                    st.error(f"Failed to validate session date: {e}")
else:
    # Clear session state if not needed for the selected feature
    st.session_state.pop("session", None)

# ==========================
# SIDEBAR — THEME SELECTION
# ==========================
# Apply custom plot themes only to features that include visualizations
if feature in ["Speed Comparison", "Circuit Map"]:
    st.sidebar.divider()
    st.sidebar.subheader("🎨 Theme Selection")
    theme_mode = st.sidebar.selectbox("Plot theme", list(vt.THEMES.keys()))
    theme = vt.THEMES[theme_mode]
else:
    theme = None

# ==========================
# OVERVIEW
# ==========================
if feature == "Overview":
    st.header("Welcome 👋")
    st.markdown(
        """
        This dashboard allows you to explore **Formula 1 session data** using real telemetry.

        **Features include:**
        - Predicting the optimal strategy for an upcoming race
        - Comparing the fastest laps of two drivers (speed vs distance)
        - Visualizing the circuit layout
        - Tracking position changes of drivers during a race
        - Driver Analysis: evaluate driver performance, theoretical lap potential, and consistency
        - Exploring different session types (Practice, Qualifying, Race)

        👉 Start by selecting a feature in the sidebar.

        Enjoy your analysis! 🏁
        """
    )
    
# ==========================
# CIRCUIT MAP
# ==========================
elif feature == "Circuit Map":

    st.header("🗺️ Circuit Map")
    st.caption("Visualize the circuit layout")

    # Check if session is loaded
    if "session" not in st.session_state:
        st.info("👈 Load a session first.")
    else:
        
        # Get circuit info and plot map
        session = st.session_state.session
        circuit_info = session.get_circuit_info()
        fig = pl.plot_circuit_map(circuit_info, session, theme)
        st.pyplot(fig)

# ==========================
# SPEED COMPARISON
# ==========================
elif feature == "Speed Comparison":

    st.header("📊 Speed Comparison")
    st.caption("Compare fastest lap telemetry between two drivers")

    # Check if session is loaded
    if "session" not in st.session_state:
        st.info("👈 Please select a **season, Grand Prix, and session** from the sidebar to start Speed Comparison.")
    else:

        # Load session
        session = st.session_state.session
        col1, col2, col3 = st.columns(3)
        col1.metric("Season", year)
        col2.metric("Grand Prix", session.event["EventName"])
        col3.metric("Session", session.name)

        # Driver selection
        drivers = sorted(session.laps["Driver"].unique().tolist())
        col1, col2 = st.columns(2)
        with col1:
            driver1 = st.selectbox("Driver 1", drivers, key="driver1_select")
        with col2:
            driver2 = st.selectbox("Driver 2", [d for d in drivers if d != driver1], index=0, key="driver2_select")

        # Initialize comparison data in session state
        if "comparison_data" not in st.session_state:
            st.session_state.comparison_data = None

        # Generate comparison on button click
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
            fig = pl.plot_speed_comparison(data["tel1"], data["tel2"], driver1, driver2, year, gp_name, session_type, data["circuit_info"], theme)
            st.pyplot(fig)

            # Metrics for lap times
            m1, m2 = st.columns(2)
            lap_time_1 = data["best1"]["LapTime"]
            lap_time_2 = data["best2"]["LapTime"]

            m1.metric(driver1, dd.format_laptime(lap_time_1))
            m2.metric(driver2, dd.format_laptime(lap_time_2))

            delta_seconds = (lap_time_2 - lap_time_1).total_seconds()

            if delta_seconds > 0:
                st.success(
                    f"🏁 **{driver1} is {delta_seconds:.3f}s faster than {driver2} on the fastest lap.**"
                )
            elif delta_seconds < 0:
                st.success(
                    f"🏁 **{driver2} is {abs(delta_seconds):.3f}s faster than {driver1} on the fastest lap.**"
                )
            else:
                st.info("🏁 Both drivers set identical fastest lap times.")

            st.caption("This comparison highlights speed differences along the lap distance.")


# ==========================
# POSITION CHANGES
# ==========================
elif feature == "Position Changes":

    st.header("📈 Position Changes")
    st.caption("Visualize the position evolution of all drivers during a race.")

    # Check if session is loaded and is a race
    if "session" not in st.session_state:
        st.info("👈 Please load a session first.")
    elif st.session_state.session.name != "Race":
        st.warning("⚠️ Please select a Race session (R) to view position changes.")
    else:
        session = st.session_state.session
        fig = pl.plot_position_changes(session)
        st.pyplot(fig)

# ==========================
# DRIVER ANALYSIS  
# ==========================
elif feature == "Driver Analysis":

    st.header("⚙️ Driver Performance Analysis")
    st.caption("Deep analysis of driver performance using telemetry and lap data")

    if "session" not in st.session_state:
        st.info("👈 Load a session first.")
    else:

        session = st.session_state.session

        col1, col2, col3 = st.columns(3)
        col1.metric("Season", year)
        col2.metric("Grand Prix", session.event["EventName"])
        col3.metric("Session", session.name)

        drivers = sorted(session.laps["Driver"].unique().tolist())
        driver = st.selectbox("Select Driver", drivers)

        if st.button("Analyze Driver"):

            raw_laps = session.laps.pick_driver(driver)

            clean_laps = (raw_laps.pick_quicklaps().dropna(subset=["LapTime"]))
            clean_laps = clean_laps[clean_laps["LapTime"] < clean_laps["LapTime"].quantile(0.95)]

            # ======================
            # CORE METRICS
            # ======================
            summary = al.full_driver_summary(clean_laps)


            if not summary:
                st.error("No valid laps for this driver.")
                st.stop()

            # ======================
            # ADVANCED REPORT
            # ======================
            report = ad.full_driver_report(clean_laps, summary)

            # ======================
            # KEY METRICS
            # ======================
            st.subheader("📊 Key Performance Metrics")

            c1, c2, c3 = st.columns(3)
            c1.metric("🏁 Best Lap", vu.fmt(summary["best_lap"]))
            c2.metric("🚀 Theoretical Best", vu.fmt(summary["theoretical_best"]))
            c3.metric("📉 Potential Gain", vu.fmt_delta(summary["potential_gain"]))

            # ======================
            # INSIGHT 
            # ======================
            st.subheader("🧠 Insight")
            st.write(report["insight"])

            # ======================
            # PERFORMANCE SCORE
            # ======================
            st.subheader("🏆 Performance Score")
            st.metric("Score", f"{report['score']} / 100")
            st.progress(report['score'] / 100)
            st.caption("Score based on pace, consistency, and potential improvement")

            # ======================
            # SECTOR ANALYSIS
            # ======================
            st.subheader("📊 Sector Analysis")

            s = summary["best_sectors"]

            col1, col2, col3 = st.columns(3)
            col1.metric("S1", vu.fmt(s["S1"]))
            col2.metric("S2", vu.fmt(s["S2"]))
            col3.metric("S3", vu.fmt(s["S3"]))

            st.write(f"⚠️ Weakest sector: **{report['weakest_sector']}**")

            # ======================
            # SECTOR RANKING
            # ======================
            st.subheader("📊 Sector Ranking (Fastest → Slowest)")

            for sector, time in report["sector_ranking"].items():
                st.write(f"{sector}: {vu.fmt(time)}")

            # ======================
            # CONSISTENCY
            # ======================
            st.subheader("📈 Consistency Analysis")

            col1, col2 = st.columns(2)
            col1.metric("Average Lap", vu.fmt(summary["average_lap"]))

            if summary["consistency"] is not None:
                col2.metric("Standard Deviation", vu.fmt(summary["consistency"]))
            else:
                col2.metric("Standard Deviation", "N/A")

            # ======================
            # LAP TIME ANALYSIS
            # ======================
            st.subheader("📈 Lap Time Analysis")

            raw_laps = session.laps.pick_driver(driver)

            lap_data = raw_laps[["LapNumber", "LapTime"]].dropna()

            if lap_data.empty:
                st.warning("Not enough valid lap data.")
            else:
                lap_data["LapTime_s"] = lap_data["LapTime"].dt.total_seconds()

                st.line_chart(lap_data.set_index("LapNumber")["LapTime_s"])

                best = lap_data.loc[lap_data["LapTime_s"].idxmin()]
                worst = lap_data.loc[lap_data["LapTime_s"].idxmax()]
                mean = lap_data["LapTime_s"].mean()

                st.caption(f"""
                🟢 Best lap: Lap {int(best["LapNumber"])} ({vu.fmt(best["LapTime"])})  
                🔴 Worst lap: Lap {int(worst["LapNumber"])} ({vu.fmt(worst["LapTime"])})  
                📊 Average pace: {vu.fmt(pd.to_timedelta(mean, unit="s"))}
                """)

# ==========================
# RACE STRATEGY ENGINE
# ==========================
elif feature == "Race Strategy Engine":

    st.header("🏁 Race Strategy Simulator")
    st.caption("Predict optimal 1-stop strategy using tyre degradation data from practice sessions.")

    # Check if session is loaded
    if "session" not in st.session_state:
        st.info(
            "👈 **Please load a Practice session (FP1 or FP2) first.**  \n"
            "These sessions include long-run simulations that provide the tyre degradation data required for race strategy modeling."
        )
        st.stop()

    else:
        # Load session
        session = st.session_state.session

        # Validate session type
        if session.name not in ["Practice 1", "Practice 2"]:
            st.warning(
                "⚠️ Strategy prediction is only available for FP1 or FP2. "
                "These sessions contain representative race-pace long runs "
                "used to model tyre degradation."
            )
            st.stop()

        # Driver selection
        drivers = sorted(session.laps["Driver"].unique().tolist())
        driver = st.selectbox("Select Driver", drivers)

        # Race laps input
        if "race_laps" not in st.session_state:
            st.session_state.race_laps = 50

        st.session_state.race_laps = st.number_input(
            "Race laps (upcoming race)",
            min_value=10,
            max_value=70,
            value=st.session_state.race_laps,
            help="Enter the total number of laps for the upcoming race."
        )

        race_laps = st.session_state.race_laps

        # Run strategy optimization on button click
        if st.button("Run Strategy Optimization"):

            with st.spinner("Building predictive model..."):

                # Build practice sessions dictionary.
                # Designed to support multiple sessions in the future, but currently using only the selected session.
                sessions = {session.name: session}
                st.caption(f"📊 Model built using: {', '.join(sessions.keys())}")

                # Predictor
                predictor = sp.Predictor(sessions, driver)
                params = predictor.get_parameters()
                if not params:
                    st.error("Not enough long-run data to build a model.")
                    st.stop()

                # Engine
                engine = sr.RaceEngine(parameters=params, race_laps=race_laps)

                # Optimizer
                optimizer = so.StrategyOptimizer(engine)

                # Optimize 1-stop strategies
                results = optimizer.optimize_1stop(available_compounds=list(params.keys()), min_pit_lap=10, max_pit_lap=race_laps - 1)
                if not results:
                    if len(params) < 2:
                        st.warning(
                            "⚠️ Strategy optimization cannot be performed because only one tyre compound "
                            "was detected with enough long-run laps. At least two compounds are required "
                            "to create a 1-stop race strategy."
                        )
                    else:
                        st.error("No valid strategies could be generated with the available data.")
                    st.stop()

                st.subheader("🏆 Top 5 Strategies")
                best_time = results[0]["total_time"]

                for i, strat in enumerate(results[:5], 1):
                    delta = strat["total_time"] - best_time

                    st.write(
                        f"**{i}. {strat['compounds'][0]} → {strat['compounds'][1]}**  |  "
                        f"Pit Lap: {strat['pit_lap']}  |  "
                        f"Total: {vu.format_total(strat['total_time'])}  |  "
                        f"Δ {vu.format_delta(delta)}"
                    )


# ==========================
#  CHAMPIONSHIP SCENARIO (COMING SOON)
# ==========================
elif feature == "Championship Scenario (Coming soon)":

    st.header("🏆 Championship Scenario Simulator")
    st.caption("Simulate title fight outcomes based on race results and FIA points system")

    st.info(
        """
        🚧 **Module under development**

        The Championship Scenario Simulator will allow you to explore
        how different race outcomes impact the Drivers' Championship standings.

        **Planned features:**
        - 📊 Automatic calculation of championship standings
        - 🧮 FIA official points system integration (including fastest lap (only for sessions happening before 2025))
        - 🏁 Simulation of remaining races in the season
        - 🔄 What-if scenarios (DNF, podium swaps, alternative results)
        - 📈 Title probability estimation based on performance trends
        - 👥 Comparison between two drivers fighting for the championship

        This module will transform single-race analysis into
        a full-season strategic projection tool.
        """
    )    