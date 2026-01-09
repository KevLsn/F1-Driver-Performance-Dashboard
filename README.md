# 🏎️ F1 Driver Performance Dashboard

![Python](https://img.shields.io/badge/Python-3.9%2B-blue) ![FastF1](https://img.shields.io/badge/FastF1-Enabled-green) ![Streamlit](https://img.shields.io/badge/Streamlit-Enabled-orange)

---

## Description

The **F1 Driver Performance Dashboard** is an interactive Python tool that lets you analyze and compare Formula 1 drivers’ performance during a session. Using **FastF1** and **Streamlit**, it fetches official telemetry data from practice, qualifying, and race sessions and provides detailed visualizations.

With this dashboard, you can:

* Select the year, Grand Prix, and session type
* Compare the fastest lap of two drivers
* Visualize circuits

---

## Key Features

* **Interactive session & driver selection via Streamlit sidebar**
* **Automatic data retrieval** via FastF1 with local caching
* **Fastest lap comparison** with speed & sector visualization
* **Error handling** for invalid inputs or missing drivers
* Extensible with new metrics (cornering, throttle/brake, trajectories)

---

## Technologies Used

* **Python 3.9+**
* **FastF1** – fetch and process F1 telemetry data
* **Matplotlib** – visualizations of speed, sectors, and comparisons
* **Pandas** – data manipulation and analysis
* **NumPy** – numerical computations used in plotting
* **Streamlit** – interactive web dashboard

---

## Installation (Local – without Docker)

```bash
# Clone the repository
git clone https://github.com/KevLsn/F1-Driver-Performance-Dashboard.git
cd f1-driver-dashboard

# Install dependencies
pip install -r requirements.txt
```

---

## Running the Dashboard

```bash
python3 -m streamlit run src/app.py
```

---

## 🐳 Running with Docker (Recommended)

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

## Dependencies

All direct dependencies are declared in `requirements.txt`:

```txt
fastf1==3.3.0
matplotlib>=3.5.0
pandas>=1.5.0
numpy>=1.23.0
streamlit>=1.15.0
```

---

## Possible Extensions

* Race strategy analysis (pit stops, tire degradation)
* Advanced telemetry metrics (cornering speed, throttle/brake analysis)