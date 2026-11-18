
import os
import json
import joblib
import numpy as np
import pandas as pd

from pathlib import Path
from tensorflow.keras.models import load_model

# ==========================================
# 1. PROJECT PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"

# ==========================================
# 2. LOAD SAVED MODELS AND PREPROCESSORS
# ==========================================

random_forest = joblib.load(MODEL_DIR / "random_forest.pkl")

autoencoder = load_model(MODEL_DIR / "autoencoder.keras")

imputer = joblib.load(MODEL_DIR / "imputer.pkl")

scaler = joblib.load(MODEL_DIR / "scaler.pkl")

label_encoder = joblib.load(MODEL_DIR / "label_encoder.pkl")

threshold = joblib.load(
    MODEL_DIR / "autoencoder_threshold.pkl"
)

with open(MODEL_DIR / "selected_features.json", "r") as f:
    selected_features = json.load(f)

# ==========================================
# 3. MAIN DETECTION FUNCTION
# ==========================================

def detect_flows(data):

    # Accept a DataFrame as input
    if isinstance(data, dict):
        data = pd.DataFrame([data])

    elif not isinstance(data, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame or dictionary.")

    # Check required features
    missing = [
        feature for feature in selected_features
        if feature not in data.columns
    ]

    if missing:
        raise ValueError(f"Missing required features: {missing}")

    # Select features in the correct order
    X = data[selected_features].copy()

    # Clean invalid values
    X = X.replace([np.inf, -np.inf], np.nan)

    # Apply saved preprocessing
    X_imputed = imputer.transform(X)

    X_scaled = scaler.transform(X_imputed)

    X_scaled = X_scaled.astype(np.float32)

    # ======================================
    # LAYER 1: RANDOM FOREST
    # ======================================

    rf_predictions = random_forest.predict(X_scaled)

    rf_probabilities = random_forest.predict_proba(X_scaled)

    rf_confidences = np.max(rf_probabilities, axis=1)

    predicted_labels = label_encoder.inverse_transform(
        rf_predictions.astype(int)
    )

    results = []

    # ======================================
    # LAYER 2: AUTOENCODER
    # Only checks RF-benign flows
    # ======================================

    benign_indices = np.where(
        predicted_labels == "Benign"
    )[0]

    anomaly_errors = {}

    if len(benign_indices) > 0:

        benign_data = X_scaled[benign_indices]

        reconstructed = autoencoder.predict(
            benign_data,
            batch_size=256,
            verbose=0
        )

        errors = np.mean(
            np.square(benign_data - reconstructed),
            axis=1
        )

        for index, error in zip(benign_indices, errors):
            anomaly_errors[index] = float(error)

    # ======================================
    # 4. FINAL DECISION
    # ======================================

    for i, label in enumerate(predicted_labels):

        anomaly_score = anomaly_errors.get(i, None)

        if label != "Benign":

            verdict = f"Known attack: {label}"

        elif anomaly_score is not None and anomaly_score > threshold:

            verdict = "Suspicious / Possible unknown attack"

        else:

            verdict = "Safe"

        results.append({
            "rf_prediction": label,
            "rf_confidence": float(rf_confidences[i]),
            "anomaly_score": anomaly_score,
            "verdict": verdict
        })

    return pd.DataFrame(results)

print("AI-NIDS-SOC detection pipeline loaded successfully!")