
import pandas as pd

def calculate_risk(row):
    verdict = row["verdict"]
    confidence = float(row["rf_confidence"])
    anomaly_score = row["anomaly_score"]

    # Known attacks receive a high risk score.
    if verdict.startswith("Known attack:"):
        risk_score = 75 + (confidence * 25)

    # Suspicious anomalies receive a medium-to-high risk score.
    elif verdict == "Suspicious / Possible unknown attack":
        risk_score = 50 + min(
            (float(anomaly_score) / 0.1424) * 25,
            25
        )

    # Normal traffic receives a low risk score.
    else:
        risk_score = confidence * 25

    risk_score = round(min(max(risk_score, 0), 100), 2)

    if risk_score <= 25:
        severity = "Low"
    elif risk_score <= 50:
        severity = "Medium"
    elif risk_score <= 75:
        severity = "High"
    else:
        severity = "Critical"

    return pd.Series({
        "risk_score": risk_score,
        "severity": severity
    })

def add_risk_scores(results):
    results = results.copy()

    risk_details = results.apply(calculate_risk, axis=1)
    results[["risk_score", "severity"]] = risk_details

    return results