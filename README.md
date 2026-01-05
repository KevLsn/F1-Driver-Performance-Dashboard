# F1 Driver Performance Dashboard

![Python](https://img.shields.io/badge/Python-3.9%2B-blue) ![FastF1](https://img.shields.io/badge/FastF1-Enabled-green)

---

## Description

The **F1 Driver Performance Dashboard** is an interactive Python tool that lets you analyze and compare Formula 1 drivers’ performance during a session. Using **FastF1**, it fetches official telemetry data from practice, qualifying, and race sessions and provides detailed visualizations.

With this dashboard, you can:

* Select the year, Grand Prix, and session type
* Compare the fastest lap of two drivers
* Visualize circuits

---

## Key Features

* **Interactive session & driver selection**
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

---

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/f1-driver-dashboard.git
cd f1-driver-dashboard

# Install dependencies
pip install -r requirements.txt
```

---

## Getting Started

To start the dashboard, simply run:

```bash
python3 src/main.py
```

---

## Possible Extensions

* Race strategy analysis (pit stops, tire degradation)
* Interactive web dashboard with **Dash** or **Streamlit**
* Advanced telemetry metrics (cornering speed, throttle/brake analysis)