
# AI-NIDS-SOC
### AI-Powered Network Intrusion Detection & Security Operations Platform

An ML-based network intrusion detection system that combines supervised learning and unsupervised anomaly detection to identify malicious network traffic, assess risk, and provide security recommendations through a SOC dashboard.

## Overview

AI-NIDS-SOC uses a dual-layer detection architecture:

- **Random Forest:** Classifies known network attacks.
- **Autoencoder:** Detects unusual traffic patterns that may indicate unknown or suspicious activity.
- **Risk Scoring:** Assigns a risk score from 0–100.
- **SOC Recommendations:** Generates investigation recommendations based on severity.
- **Dashboard:** Provides a visual interface for analysing detection results.

## Architecture

```text
Network Traffic Dataset
        |
        v
Data Preprocessing
        |
        v
Feature Selection
        |
        v
+-----------------------+
|   Random Forest       |
| Known Attack Detection|
+-----------------------+
        |
        v
  Predicted Benign?
    /           \
  Yes            No
   |              |
   v              v
Autoencoder    Known Attack
Anomaly Check  Classification
   |
   v
Risk Scoring
   |
   v
Severity Classification
   |
   v
SOC Recommendations
   |
   v
Streamlit Dashboard
```

## Machine Learning Models

### Supervised Learning
Random Forest classifier trained to identify benign traffic and known attack categories.

### Unsupervised Learning
Autoencoder trained on benign traffic to identify deviations from learned traffic patterns using reconstruction error.

## Dataset

This project uses the **CSE-CIC-IDS2018** dataset.

The dataset contains benign traffic and multiple attack categories.

Dataset source:

https://www.unb.ca/cic/datasets/ids-2018.html

The dataset is not included in this repository due to its large size.

## Project Structure

```text
AI-NIDS-SOC/
│
├── dashboard/
│   └── app.py
│
├── notebooks/
│   ├── model_trained.ipynb
│   └── cicids2018-preprocess.ipynb
│
├── src/
│   ├── pipeline.py
│   ├── risk.py
│   ├── actions.py
│   └── reporting.py
│
├── models/
│   ├── random_forest.pkl
│   ├── autoencoder.keras
│   ├── imputer.pkl
│   ├── scaler.pkl
│   ├── label_encoder.pkl
│   ├── autoencoder_threshold.pkl
│   └── selected_features.json
│
├── data/
├── reports/
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/navyajain1406/AI-NIDS-SOC.git

cd AI-NIDS-SOC
```

### 2. Create a virtual environment

#### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the Dashboard

From the project root directory:

```bash
streamlit run dashboard/app.py
```

The dashboard will open in your browser.

Local URL:

```text
http://localhost:8501
```

## Running the Notebooks

Open the notebooks located inside the `notebooks/` directory using Jupyter Notebook or VS Code.

The notebooks cover dataset preprocessing, model training, evaluation, and experimentation.

Ensure the dataset is downloaded and its path is correctly configured before executing notebook cells.

## Detection Logic

| Detection Result | Decision |
|---|---|
| Random Forest identifies an attack | Known attack |
| Random Forest predicts benign, Autoencoder flags anomaly | Suspicious |
| Both models indicate normal traffic | Safe |

## Risk Severity

| Risk Score | Severity |
|---|---|
| 0–25 | Low |
| 26–50 | Medium |
| 51–75 | High |
| 76–100 | Critical |

SOC recommendations are generated based on the assigned severity.

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- TensorFlow / Keras
- Streamlit
- Plotly
- Jupyter Notebook

## Project Status

This project is under active development.

Current components include:

- Data preprocessing
- Random Forest classification
- Autoencoder anomaly detection
- Integrated detection pipeline
- Risk scoring
- SOC recommendations
- CSV reporting
- Streamlit dashboard overview

Additional dashboard modules and simulated monitoring features are planned.

## Disclaimer

This project is developed for educational, research, and defensive cybersecurity purposes.

Detection results should be validated before being used in real-world security environments.

## Contributors

Developed as an academic machine learning and cybersecurity project.