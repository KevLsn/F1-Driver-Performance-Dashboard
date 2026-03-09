# 🏎️ F1 Driver Performance Dashboard

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![FastF1](https://img.shields.io/badge/FastF1-Enabled-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Enabled-orange)

---

## Description

The **F1 Driver Performance Dashboard** is an interactive Python tool that lets you analyze and compare Formula 1 drivers’ performance during a session. Using **FastF1** and **Streamlit**, it fetches official telemetry data from practice, qualifying, and race sessions and provides detailed visualizations in a **visual, interactive web app**.

With this dashboard, you can:

* Select the year, Grand Prix, and session type
* Compare the fastest lap of two drivers
* Visualize circuits
* Simulate predictive 1-stop race strategies  
* Customize themes for all visualizations
* Access the app publicly via Streamlit Cloud

---

## Key Features

* **Interactive session & driver selection via Streamlit sidebar**
* **Automatic data retrieval** with FastF1 caching
* **Fastest lap comparison** with speed & sector visualization
* **Circuit map visualization** with corner labels  
* **Predictive 1-stop** race strategy simulation  
* **Theme customization** for all visualizations  
* **Error handling** for invalid inputs or missing drivers
* **Public deployment** with Streamlit Cloud for instant access
* Extensible with new metrics (cornering, throttle/brake, trajectories)

---

## Technologies Used

* **Python 3.9+**
* **FastF1** – fetch and process F1 telemetry data
* **Matplotlib** – visualizations of speed, sectors, and comparisons
* **Pandas** – data manipulation and analysis
* **NumPy** – numerical computations used in plotting
* **Streamlit** – interactive web dashboard and public deployment
* **Docker** – reproducible environment for easy deployment

---

## Live Demo

The app is deployed publicly via Streamlit Cloud:

[**Open the F1 Dashboard**](https://f1-driver-performance-dashboard.streamlit.app)

---

## Installation (Local – without Docker)

### Requirements

* **Python 3.9+**
* **pip** package manager

### Setup Steps

```bash
# Clone the repository
git clone https://github.com/KevLsn/F1-Driver-Performance-Dashboard.git
cd F1-Driver-Performance-Dashboard

# Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Running the Dashboard

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

---

## 🐳 Running with Docker

Docker guarantees the project runs **identically on any machine**.

### Requirements

* Docker Desktop (macOS / Windows / Linux)

> Make sure Docker is running before continuing

### Build the Docker image

```bash
docker build -t f1-dashboard .
```

### Run the dashboard

```bash
docker run --rm -it -p 8501:8501 f1-dashboard
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Usage Guide

### 1. Select a Feature
- Choose a feature from the sidebar: **Overview**, **Speed Comparison**, **Circuit Map**, or **Race Strategy Engine**

### 2. Load a Session
- After selecting **Speed Comparison**, **Circuit Map**, or **Race Strategy Engine**:  
  - Pick **Season** (2018–2026), **Grand Prix**, and **Session type** (FP1, FP2, FP3, Q, R)  
  - Click **"Load Session"**  
- ⚠️ Only FP1/FP2 sessions provide data for race strategy simulation  

### 3. Customize Theme (Speed & Map only)
- After loading a session for **Speed Comparison** or **Circuit Map**:  
  - Choose from multiple themes: bright, dark, Mercedes, Red Bull, Ferrari, McLaren  
  - Themes affect the plots and visualizations  

### 4. Speed Comparison
- Select **Driver 1** and **Driver 2**  
- Click **"Generate Comparison"**  
- View speed vs distance plots with corner markers and lap time metrics  

### 5. Circuit Map
- View the track layout with corner labels  

### 6. Race Strategy Simulator
- Select a **Driver**  
- Input **Race laps** for the upcoming race  
- Click **"Run Strategy Optimization"** to predict optimal 1-stop strategies  

---

## Troubleshooting

### Error: "Invalid or missing lap data"
- Ensure the Grand Prix name is correct (check [FastF1 documentation](https://github.com/theOehrly/Fast-F1))
- Verify both drivers participated in the selected session
- Try reloading the session

### Error: "Failed to load session"
- Check your internet connection (data is downloaded on first use)
- Verify the season year is available in FastF1
- Ensure the Grand Prix name uses the official event name
- Make sure **Streamlit sidebar selections** are complete (feature, season, GP, session)

### Theme not applied / incorrect colors
- Themes are applied **only** for Speed Comparison and Circuit Map
- Selecting another feature will ignore theme settings

### Slow Performance
- First load of a session downloads large datasets (normal)
- Data is cached locally in the `cache/` folder for faster subsequent loads
- On Docker, the cache is stored in the container and lost after exit

### Race Strategy Warnings
- Strategy optimization works **only** with FP1 or FP2 sessions
- At least **two tyre compounds** must have long-run laps to compute a 1-stop strategy
- Short practice sessions or missing data may prevent valid strategies

### Session not appearing
- Some older sessions (pre-2018) may have limited data availability
- Check the [FastF1 documentation](https://github.com/theOehrly/Fast-F1) for available seasons

---

## Dependencies

All direct dependencies are declared in `requirements.txt`:

```txt
fastf1>=3.3.0
matplotlib>=3.8.0
pandas>=2.0.0
numpy>=1.24.0
streamlit>=1.40.0
```

---

## Project Structure

```
F1-Driver-Performance-Dashboard/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Production dependencies
├── Dockerfile                      # Docker configuration
├── README.md                       # This file
├── cache/                          # Local FastF1 data cache
└── src/
    ├── data/
    │   ├── driver_data.py         # Driver utilities (lap time formatting, validation)
    │   └── session_data.py        # Session loading and caching
    ├── strategy/
    │   ├── predictor.py           # Tyre and lap predictive model
    │   ├── race_engine.py         # Race simulation engine
    │   └── optimizer.py           # Strategy optimization (1-stop)
    └── visualization/
        ├── plots.py                # Plotting functions for circuit & speed
        ├── theme.py                # Theme definitions
        └── utils.py                # Utility functions (formatting)
```

---

## Possible Extensions

* **Advanced telemetry metrics** (cornering speed, throttle/brake analysis)
* **Sector-by-sector comparison** (S1, S2, S3 analysis)
* **Lap-to-lap consistency** visualization
* **Championship scenario** simulation
* **Weather impact analysis** (temperature correlation)

---

## Support & Credits

* **FastF1**: Official F1 telemetry data ([GitHub](https://github.com/theOehrly/Fast-F1))
* **Streamlit**: Interactive web app framework ([Website](https://streamlit.io))
* **Matplotlib**: Visualization library ([Website](https://matplotlib.org))