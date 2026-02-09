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
* Access the app publicly via Streamlit Cloud

---

## Key Features

* **Interactive session & driver selection via Streamlit sidebar**
* **Automatic data retrieval** via FastF1 with local caching
* **Fastest lap comparison** with speed & sector visualization
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

### 1. Select a Session
- Choose the **Season** (2018-2026)
- Enter the **Grand Prix name** (e.g., "Monza", "Silverstone")
- Select the **Session type** (FP1, FP2, FP3, Q, R)
- Click **"Load Session"**

### 2. Speed Comparison
- Select **Driver 1** and **Driver 2** from dropdowns
- Click **"Generate Comparison"**
- View the speed comparison graph with corner markers
- Compare lap times in the metrics display

### 3. Circuit Map
- After loading a session, click **"Show Circuit Map"**
- View the track layout with corner labels
- The map shows the racing line from the fastest lap

### 4. Customize Theme
- Choose from multiple themes: bright, dark, Mercedes, Red Bull, Ferrari, McLaren
- Themes affect both the speed comparison and circuit map visualization

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

### Slow Performance
- First load of a session downloads large datasets (normal)
- Data is cached locally in the `cache/` folder for faster subsequent loads
- On Docker, the cache is stored in the container and lost after exit

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
├── pyproject.toml                  # Project configuration
├── Dockerfile                      # Docker configuration
├── README.md                       # This file
├── CODE_REVIEW.md                  # Code review findings
├── cache/                          # Local FastF1 data cache
└── src/
    ├── data/
    │   ├── driver_data.py         # Driver utilities (lap time formatting)
    │   └── session_data.py        # Session loading and caching
    └── visualization/
        └── plots.py                # Plotting functions
```

---

## Possible Extensions

* **Race strategy analysis** (pit stops, tire degradation)
* **Advanced telemetry metrics** (cornering speed, throttle/brake analysis)
* **Sector-by-sector comparison** (S1, S2, S3 analysis)
* **Lap-to-lap consistency** visualization
* **Championship scenario** simulation
* **Multiple driver comparison** (3+ drivers simultaneously)
* **Weather impact analysis** (temperature correlation)

---

## Support & Credits

* **FastF1**: Official F1 telemetry data ([GitHub](https://github.com/theOehrly/Fast-F1))
* **Streamlit**: Interactive web app framework ([Website](https://streamlit.io))
* **Matplotlib**: Visualization library ([Website](https://matplotlib.org))