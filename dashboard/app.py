
import sys
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px


# ---------------- PROJECT PATHS ----------------

PROJECT_DIR = Path(__file__).resolve().parent.parent
REPORT_PATH = PROJECT_DIR / "reports" / "full_detection_results.csv"

if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI-NIDS | Security Operations",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background-color: #F5F6F8;
    }

    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #263244;
    }

    [data-testid="stSidebar"] * {
        color: #E5E7EB;
    }

    .brand {
        font-size: 21px;
        font-weight: 700;
        letter-spacing: -0.7px;
        color: #FFFFFF;
        padding: 12px 0 4px 0;
    }

    .brand span {
        color: #60A5FA;
    }

    .sidebar-caption {
        color: #94A3B8;
        font-size: 10px;
        letter-spacing: 1.5px;
        margin-bottom: 25px;
    }

    .page-eyebrow {
        color: #64748B;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 1.5px;
    }

    .page-title {
        color: #111827;
        font-size: 29px;
        font-weight: 700;
        letter-spacing: -1px;
        margin-top: 3px;
    }

    .page-subtitle {
        color: #64748B;
        font-size: 13px;
        margin-bottom: 25px;
    }

    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        padding: 18px;
        border-radius: 8px;
    }

    div[data-testid="stMetricLabel"] {
        color: #64748B;
        font-size: 12px;
    }

    div[data-testid="stMetricValue"] {
        color: #111827;
        font-weight: 700;
    }

    .section-title {
        font-size: 16px;
        font-weight: 600;
        color: #111827;
        margin: 12px 0;
    }

    .status-online {
        display: inline-block;
        background: #DCFCE7;
        color: #166534;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #E5E7EB;
        border-radius: 8px;
    }

    #MainMenu, footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)


# ---------------- LOAD DATA ----------------

@st.cache_data
def load_results():
    if REPORT_PATH.exists():
        return pd.read_csv(REPORT_PATH)
    return pd.DataFrame()


df = load_results()


# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.markdown(
        '<div class="brand">NEXUS<span>.</span> SOC</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-caption">NETWORK SECURITY OPERATIONS</div>',
        unsafe_allow_html=True
    )

    st.markdown("**WORKSPACE**")

    page = st.radio(
        "Navigation",
        [
            "Overview",
            "Security Alerts",
            "Attack Analysis",
            "Model Performance",
            "Upload & Predict",
            "SOC Panel"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.caption("DETECTION ENGINE")

    st.markdown(
        '<span class="status-online">● Models available</span>',
        unsafe_allow_html=True
    )

    st.divider()

    st.caption("AI-NIDS v1.0")
    st.caption("Defensive monitoring platform")


# ---------------- OVERVIEW PAGE ----------------

if page == "Overview":

    st.markdown(
        '<div class="page-eyebrow">SECURITY OPERATIONS / OVERVIEW</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-title">Security overview</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">'
        'Monitor network traffic and review detected security events.'
        '</div>',
        unsafe_allow_html=True
    )

    if df.empty:
        st.warning(
            "No detection report found. Generate a report before viewing "
            "dashboard statistics."
        )
        st.stop()

    # Calculate actual statistics from the report
    total_flows = len(df)
    known_attacks = df["verdict"].astype(str).str.startswith(
        "Known attack:"
    ).sum()
    suspicious = (
        df["verdict"] == "Suspicious / Possible unknown attack"
    ).sum()
    safe_flows = (df["verdict"] == "Safe").sum()
    critical_alerts = (df["severity"] == "Critical").sum()

    # KPI cards
    st.markdown("### Traffic summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total flows analysed", f"{total_flows:,}")
    col2.metric("Known attacks", f"{known_attacks:,}")
    col3.metric("Suspicious flows", f"{suspicious:,}")
    col4.metric("Critical alerts", f"{critical_alerts:,}")

    st.markdown("---")

    left, right = st.columns([1.15, 0.85])

    # Traffic classification chart
    with left:
        st.markdown(
            '<div class="section-title">Traffic classification</div>',
            unsafe_allow_html=True
        )

        classification = pd.Series({
            "Safe": safe_flows,
            "Known attacks": known_attacks,
            "Suspicious": suspicious
        })

        classification = classification[classification > 0]

        fig = px.pie(
            values=classification.values,
            names=classification.index,
            hole=0.68
        )

        fig.update_traces(
            textposition="inside",
            textinfo="label+percent",
            marker=dict(
                colors=["#3B82F6", "#DC5A5A", "#E6A23C"],
                line=dict(color="#FFFFFF", width=3)
            )
        )

        fig.update_layout(
            height=310,
            margin=dict(t=15, b=15, l=10, r=10),
            showlegend=False,
            paper_bgcolor="white",
            plot_bgcolor="white",
            font=dict(color="#334155")
        )

        st.plotly_chart(fig, use_container_width=True)

    # Severity distribution
    with right:
        st.markdown(
            '<div class="section-title">Alert severity</div>',
            unsafe_allow_html=True
        )

        severity_order = ["Low", "Medium", "High", "Critical"]

        severity_counts = (
            df["severity"]
            .value_counts()
            .reindex(severity_order, fill_value=0)
            .reset_index()
        )

        severity_counts.columns = ["Severity", "Count"]

        fig2 = px.bar(
            severity_counts,
            x="Severity",
            y="Count",
            text="Count",
            color="Severity",
            category_orders={"Severity": severity_order},
            color_discrete_map={
                "Low": "#60A5FA",
                "Medium": "#E6A23C",
                "High": "#EA8055",
                "Critical": "#DC5A5A"
            }
        )

        fig2.update_layout(
            height=310,
            showlegend=False,
            margin=dict(t=15, b=15, l=10, r=10),
            paper_bgcolor="white",
            plot_bgcolor="white",
            xaxis_title="",
            yaxis_title="Number of flows",
            font=dict(color="#334155")
        )

        fig2.update_traces(textposition="outside")

        st.plotly_chart(fig2, use_container_width=True)

    # Recent alerts
    st.markdown("---")
    st.markdown(
        '<div class="section-title">Recent detection results</div>',
        unsafe_allow_html=True
    )

    alerts = df[df["severity"].isin(["High", "Critical", "Medium"])]

    if alerts.empty:
        st.info("No medium or higher severity alerts in this report.")
    else:
        display_columns = [
            "rf_prediction",
            "verdict",
            "risk_score",
            "severity",
            "recommended_action"
        ]

        st.dataframe(
            alerts[display_columns].head(10),
            use_container_width=True,
            hide_index=True
        )

    st.caption(
        "Statistics are calculated from the currently loaded detection report. "
        "They do not represent live network traffic."
    )


# ---------------- OTHER PAGES: TEMPORARY ----------------

else:
    st.markdown(
        f'<div class="page-eyebrow">SECURITY OPERATIONS</div>'
        f'<div class="page-title">{page}</div>',
        unsafe_allow_html=True
    )

    st.info(
        f"The {page} page will be implemented in the next development steps."
    )
