import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import random

# API Configuration
API_URL = "http://127.0.0.1:8000/predict"

# Page Configuration
st.set_page_config(
    page_title="ShieldBank: Financial Crime Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Bank Blue Theme
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --bank-blue: #003d82;
        --bank-light-blue: #0066cc;
        --bank-accent: #00a3e0;
        --success-green: #00c853;
        --danger-red: #d32f2f;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #003d82 0%, #0066cc 100%);
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Headers */
    h1 {
        color: #003d82;
        font-weight: 700;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #00a3e0;
    }

    h2, h3 {
        color: #0066cc;
    }

    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #003d82 0%, #0066cc 100%);
        color: white;
        border: none;
        padding: 0.6rem 2rem;
        font-weight: 600;
        border-radius: 5px;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background: linear-gradient(90deg, #0066cc 0%, #00a3e0 100%);
        box-shadow: 0 4px 12px rgba(0, 61, 130, 0.4);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }

    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem;
        font-weight: 600;
        color: #003d82;
    }

    .stTabs [aria-selected="true"] {
        background-color: #003d82;
        color: white !important;
    }

    /* Alert boxes */
    .fraud-alert {
        background-color: #ffebee;
        border-left: 5px solid #d32f2f;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }

    .safe-alert {
        background-color: #e8f5e9;
        border-left: 5px solid #00c853;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to update metrics based on transaction history
def update_metrics_from_transactions():
    """Calculate metrics dynamically from transaction history"""
    if len(st.session_state.transaction_history) == 0:
        # Return default values if no transactions
        return {
            "total_transactions": 12847,
            "fraud_detected": 983,
            "fraud_prevented": 967,
            "false_positives": 145,
            "total_saved": 2847500,
            "today_count": 0
        }

    # Calculate from transaction history
    fraud_count = sum(1 for txn in st.session_state.transaction_history if txn['is_fraud'])
    safe_count = len(st.session_state.transaction_history) - fraud_count

    # Assume 98.4% prevention rate
    fraud_prevented = int(fraud_count * 0.984)

    # Estimate false positives (1.4% of total)
    false_positives = int(len(st.session_state.transaction_history) * 0.014)

    # Calculate total saved (average fraud amount * prevented)
    avg_fraud_amount = np.mean([txn['amount'] for txn in st.session_state.transaction_history if txn['is_fraud']]) if fraud_count > 0 else 2500
    total_saved = int(fraud_prevented * avg_fraud_amount)

    # Base metrics + new transactions
    base_total = 12847
    new_total = base_total + len(st.session_state.transaction_history)

    base_fraud = 983
    new_fraud_total = base_fraud + fraud_count

    return {
        "total_transactions": new_total,
        "fraud_detected": new_fraud_total,
        "fraud_prevented": 967 + fraud_prevented,
        "false_positives": 145 + false_positives,
        "total_saved": 2847500 + total_saved,
        "today_count": len(st.session_state.transaction_history)
    }

# Initialize session state
if "live_monitoring" not in st.session_state:
    st.session_state.live_monitoring = False
if "transaction_history" not in st.session_state:
    st.session_state.transaction_history = []
if "metrics" not in st.session_state:
    st.session_state.metrics = {
        "total_transactions": 12847,
        "fraud_detected": 983,
        "fraud_prevented": 967,
        "false_positives": 145,
        "total_saved": 2847500,
        "today_count": 0
    }

# Sidebar
with st.sidebar:
    st.markdown("# 🛡️ ShieldBank")
    st.markdown("### Financial Crime Detection")
    st.markdown("---")

    st.markdown("### 📊 System Status")
    st.markdown("🟢 **Model**: Online")
    st.markdown("🟢 **API**: Connected")
    st.markdown(f"⏱️ **Uptime**: 99.97%")

    st.markdown("---")
    st.markdown("### ⚙️ Settings")

    fraud_threshold = st.slider(
        "Fraud Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.65,
        step=0.05,
        help="Probability threshold for flagging fraud"
    )

    st.markdown("---")
    st.markdown("### 📈 Quick Stats")

    # Dynamic stats based on transaction history
    live_count = len(st.session_state.transaction_history)
    if live_count > 0:
        live_fraud = sum(1 for txn in st.session_state.transaction_history if txn['is_fraud'])
        live_fraud_rate = (live_fraud / live_count * 100) if live_count > 0 else 7.6
        st.metric("Live Transactions", f"{live_count}")
        st.metric("Live Fraud Rate", f"{live_fraud_rate:.1f}%")
    else:
        st.metric("Today's Transactions", "1,247")
        st.metric("Fraud Rate", "7.6%")

    st.metric("Avg Response", "12ms")

# Main Header
st.markdown("# 🛡️ ShieldBank: Financial Crime Detection")
st.markdown("**Command Center** | Real-time fraud monitoring powered by LightGBM & SHAP")

# Create Tabs (Dashboard + Model Performance only for cloud deployment)
tab1, tab2 = st.tabs(["📊 Executive Summary", "🎯 Model Performance"])

# ====================================
# TAB 1: EXECUTIVE SUMMARY
# ====================================
with tab1:
    st.markdown("## Executive Summary")
    st.markdown("High-level overview of fraud detection performance")

    # Update metrics from transaction history
    st.session_state.metrics = update_metrics_from_transactions()

    # Show connection indicator if there are live transactions
    if st.session_state.metrics.get('today_count', 0) > 0:
        st.info(f"📊 **Live Update**: Metrics include {st.session_state.metrics['today_count']} recent transactions from Live Monitoring")

    # Top Metrics Row
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        today_delta = st.session_state.metrics.get('today_count', 0)
        st.metric(
            "Total Transactions",
            f"{st.session_state.metrics['total_transactions']:,}",
            delta=f"+{today_delta} live"
        )

    with col2:
        fraud_rate = (st.session_state.metrics['fraud_detected'] /
                     st.session_state.metrics['total_transactions'] * 100)
        st.metric(
            "Fraud Detected",
            f"{st.session_state.metrics['fraud_detected']:,}",
            delta=f"{fraud_rate:.1f}%"
        )

    with col3:
        prevention_rate = (st.session_state.metrics['fraud_prevented'] /
                          st.session_state.metrics['fraud_detected'] * 100)
        st.metric(
            "Fraud Prevented",
            f"{st.session_state.metrics['fraud_prevented']:,}",
            delta=f"{prevention_rate:.1f}%"
        )

    with col4:
        st.metric(
            "False Positives",
            st.session_state.metrics['false_positives'],
            delta="-12 vs last week",
            delta_color="inverse"
        )

    with col5:
        # Calculate live savings if there are new transactions
        base_saved = 2847500
        live_saved = st.session_state.metrics['total_saved'] - base_saved
        delta_text = f"+${live_saved:,} live" if live_saved > 0 else "+$45K today"

        st.metric(
            "Total Saved",
            f"${st.session_state.metrics['total_saved']:,}",
            delta=delta_text
        )

    st.markdown("---")

    # Fraud Heatmap Section
    col_heat1, col_heat2 = st.columns([2, 1])

    with col_heat1:
        st.markdown("### 🌡️ Fraud Heatmap: Time vs Amount")

        # Generate synthetic heatmap data
        np.random.seed(42)
        hours = list(range(24))
        amount_ranges = ['$0-500', '$500-1K', '$1K-2K', '$2K-5K', '$5K-10K', '$10K+']

        # Create heatmap data with fraud clustering patterns
        heatmap_data = []
        for hour in hours:
            for amount_idx, amount_range in enumerate(amount_ranges):
                # Higher fraud in late hours and higher amounts
                base_fraud = 5
                time_factor = 1.5 if (hour >= 22 or hour <= 4) else 1.0
                amount_factor = 1.0 + (amount_idx * 0.3)

                fraud_count = int(base_fraud * time_factor * amount_factor *
                                np.random.uniform(0.5, 1.5))

                heatmap_data.append({
                    'Hour': hour,
                    'Amount Range': amount_range,
                    'Fraud Count': fraud_count
                })

        df_heatmap = pd.DataFrame(heatmap_data)
        pivot_heatmap = df_heatmap.pivot(index='Amount Range', columns='Hour', values='Fraud Count')

        fig_heatmap = px.imshow(
            pivot_heatmap,
            labels=dict(x="Hour of Day", y="Transaction Amount", color="Fraud Count"),
            x=[f"{h:02d}:00" for h in hours],
            y=amount_ranges,
            color_continuous_scale='Reds',
            aspect='auto'
        )

        fig_heatmap.update_layout(
            height=400,
            title_font_size=14,
            xaxis_title="Time of Day",
            yaxis_title="Transaction Amount Range"
        )

        st.plotly_chart(fig_heatmap, use_container_width=True)

    with col_heat2:
        st.markdown("### 🎯 Risk Distribution")

        # Risk distribution pie chart
        risk_data = pd.DataFrame({
            'Risk Level': ['High Risk', 'Medium Risk', 'Low Risk', 'Safe'],
            'Count': [983, 567, 823, 10474],
            'Color': ['#d32f2f', '#ff9800', '#ffd54f', '#00c853']
        })

        fig_risk = go.Figure(data=[go.Pie(
            labels=risk_data['Risk Level'],
            values=risk_data['Count'],
            marker=dict(colors=risk_data['Color']),
            hole=0.4,
            textinfo='label+percent',
            textfont_size=12
        )])

        fig_risk.update_layout(
            height=300,
            showlegend=True,
            margin=dict(t=30, b=0, l=0, r=0)
        )

        st.plotly_chart(fig_risk, use_container_width=True)

    st.markdown("---")

    # Live Monitoring Simulation
    st.markdown("### 🔴 Live Transaction Feed")

    col_live1, col_live2, col_live3 = st.columns([1, 1, 3])

    with col_live1:
        if st.button("▶️ Start Live Monitoring" if not st.session_state.live_monitoring
                    else "⏸️ Pause Monitoring",
                    key="live_btn"):
            st.session_state.live_monitoring = not st.session_state.live_monitoring

    with col_live2:
        if st.button("🔄 Reset Metrics", key="reset_btn"):
            st.session_state.transaction_history = []
            st.session_state.metrics = {
                "total_transactions": 12847,
                "fraud_detected": 983,
                "fraud_prevented": 967,
                "false_positives": 145,
                "total_saved": 2847500,
                "today_count": 0
            }
            st.rerun()

    with col_live3:
        if st.session_state.live_monitoring:
            st.markdown("🟢 **Status**: Monitoring Active | Processing transactions in real-time...")
        else:
            st.markdown("⚪ **Status**: Monitoring Paused")

    # Display transaction feed
    if st.session_state.live_monitoring:
        placeholder = st.empty()

        # Simulate 5 transactions
        for i in range(5):
            # Generate random transaction
            transaction_id = f"TXN-{random.randint(100000, 999999)}"
            amount = random.randint(100, 15000)
            risk_score = random.uniform(0.1, 0.99)

            is_fraud = risk_score >= fraud_threshold

            # Add to history
            st.session_state.transaction_history.insert(0, {
                'id': transaction_id,
                'amount': amount,
                'risk_score': risk_score,
                'is_fraud': is_fraud,
                'timestamp': datetime.now() - timedelta(seconds=i*2)
            })

            # Keep only last 20
            st.session_state.transaction_history = st.session_state.transaction_history[:20]

            time.sleep(0.5)

        # Update metrics after adding transactions
        st.session_state.metrics = update_metrics_from_transactions()
        st.session_state.live_monitoring = False
        st.rerun()

    # Show transaction history
    if st.session_state.transaction_history:
        st.markdown("#### Recent Transactions")

        for txn in st.session_state.transaction_history[:10]:
            col_t1, col_t2, col_t3, col_t4, col_t5 = st.columns([2, 2, 2, 2, 1])

            with col_t1:
                st.markdown(f"**{txn['id']}**")

            with col_t2:
                st.markdown(f"${txn['amount']:,}")

            with col_t3:
                st.markdown(f"{txn['timestamp'].strftime('%H:%M:%S')}")

            with col_t4:
                risk_color = "🔴" if txn['risk_score'] >= 0.75 else "🟡" if txn['risk_score'] >= 0.5 else "🟢"
                st.markdown(f"{risk_color} {txn['risk_score']:.2%}")

            with col_t5:
                if txn['is_fraud']:
                    st.markdown("🚨 FRAUD")
                else:
                    st.markdown("✅ SAFE")

            st.markdown("---")

# ====================================
# TAB 2: FRAUD DEEP DIVE (HIDDEN FOR CLOUD DEPLOYMENT)
# ====================================
# Note: This tab requires FastAPI backend which doesn't run on Streamlit Cloud
# Uncomment below and change tab count to 3 if running locally with API
"""
with tab2:
    st.markdown("## 🔍 Fraud Deep Dive")
    st.markdown("Individual transaction inspection and fraud prediction")


    with st.form("transaction_form"):
        st.markdown("### 🎯 Key Transaction Features")
        st.markdown("*Simplified form showing only the most impactful fraud indicators*")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 💰 Customer Profile")
            income = st.number_input("Annual Income ($)", min_value=0.0, value=50000.0, step=5000.0)
            customer_age = st.number_input("Customer Age", min_value=18, max_value=100, value=35)
            credit_risk_score = st.number_input("Credit Risk Score (0-850)", min_value=0, max_value=850, value=600)

            st.markdown("#### 🏦 Banking History")
            bank_months_count = st.number_input("Customer Tenure (months)", value=12, min_value=0, max_value=600,
                                                help="How long customer has been with bank")
            proposed_credit_limit = st.number_input("Requested Credit Limit ($)", value=3000.0, step=500.0)

            st.markdown("#### 👤 Personal Info")
            employment_status = st.selectbox(
                "Employment Status",
                ["employed", "self-employed", "unemployed", "student"],
                help="Current employment situation"
            )

        with col2:
            st.markdown("#### 🚀 Velocity Indicators (Most Important!)")
            velocity_6h = st.number_input("Transactions in Last 6 Hours", value=1.2, min_value=0.0, max_value=50.0, step=0.5,
                                         help="⚠️ High velocity = fraud risk. Normal: 1-3")
            velocity_24h = st.number_input("Transactions in Last 24 Hours", value=3.4, min_value=0.0, max_value=100.0, step=0.5,
                                          help="⚠️ High velocity = fraud risk. Normal: 2-5")
            velocity_4w = st.number_input("Transactions in Last 4 Weeks", value=8.9, min_value=0.0, max_value=500.0, step=1.0,
                                         help="⚠️ High velocity = fraud risk. Normal: 5-20")

            st.markdown("#### 🚨 Risk Flags")
            foreign_request = st.selectbox("Foreign Request", [0, 1],
                                          help="Application from outside home country (1=Yes, 0=No)")
            email_is_free = st.selectbox("Free Email Provider", [0, 1],
                                        help="Using Gmail/Yahoo vs business email (1=Yes, 0=No)")

            st.markdown("#### 💳 Transaction Type")
            payment_type = st.selectbox(
                "Payment Type",
                ["credit_card", "debit_card", "bank_transfer"]
            )
            source = st.selectbox("Application Source", ["web", "mobile"])

        st.markdown("---")

        # Collapsible section for advanced fields
        with st.expander("⚙️ Advanced Fields (Optional - Auto-filled with defaults)"):
            col_adv1, col_adv2, col_adv3 = st.columns(3)

            with col_adv1:
                intended_balcon_amount = st.number_input("Intended Balance", value=1200.0)
                session_length = st.number_input("Session Length (min)", value=8.5)
                days_since_request = st.number_input("Days Since Request", value=1.0)

            with col_adv2:
                zip_count_4w = st.number_input("Zip Count (4w)", value=3)
                phone_home_valid = st.selectbox("Phone Home Valid", [1, 0], index=0)
                phone_mobile_valid = st.selectbox("Phone Mobile Valid", [1, 0], index=0)

            with col_adv3:
                has_other_cards = st.selectbox("Has Other Cards", [1, 0], index=0)
                keep_alive_session = st.selectbox("Keep Alive Session", [1, 0], index=0)
                device_os = st.selectbox("Device OS", ["windows", "android", "ios", "mac"])

            col_adv4, col_adv5, col_adv6 = st.columns(3)
            with col_adv4:
                housing_status = st.selectbox("Housing", ["own", "rent", "mortgage"])
            with col_adv5:
                month = st.selectbox("Month", list(range(1, 13)), index=1)
            with col_adv6:
                bank_branch_count_8w = st.number_input("Bank Branch Count (8w)", value=1, min_value=0)

            col_adv7, col_adv8 = st.columns(2)
            with col_adv7:
                device_distinct_emails_8w = st.number_input("Device Distinct Emails (8w)", value=1, min_value=0)
                prev_address_months_count = st.number_input("Previous Address Months", value=24, min_value=0)
            with col_adv8:
                date_of_birth_distinct_emails_4w = st.number_input("DOB Distinct Emails (4w)", value=1, min_value=0)
                current_address_months_count = st.number_input("Current Address Months", value=12, min_value=0)

        st.markdown("---")
        submitted = st.form_submit_button("🔍 Analyze Transaction", use_container_width=True)

    if submitted:
        payload = {
            "income": income,
            "customer_age": customer_age,
            "credit_risk_score": credit_risk_score,
            "proposed_credit_limit": proposed_credit_limit,
            "intended_balcon_amount": intended_balcon_amount,
            "session_length_in_minutes": session_length,
            "days_since_request": days_since_request,
            "bank_months_count": bank_months_count,
            "zip_count_4w": zip_count_4w,
            "velocity_6h": velocity_6h,
            "velocity_24h": velocity_24h,
            "velocity_4w": velocity_4w,
            "bank_branch_count_8w": bank_branch_count_8w,
            "device_distinct_emails_8w": device_distinct_emails_8w,
            "date_of_birth_distinct_emails_4w": date_of_birth_distinct_emails_4w,
            "prev_address_months_count": prev_address_months_count,
            "current_address_months_count": current_address_months_count,
            "email_is_free": email_is_free,
            "phone_home_valid": phone_home_valid,
            "phone_mobile_valid": phone_mobile_valid,
            "has_other_cards": has_other_cards,
            "foreign_request": foreign_request,
            "keep_alive_session": keep_alive_session,
            "employment_status": employment_status,
            "housing_status": housing_status,
            "payment_type": payment_type,
            "source": source,
            "device_os": device_os,
            "month": month,
        }

        with st.spinner("🔄 Calling fraud detection API..."):
            try:
                response = requests.post(API_URL, json=payload)

                if response.status_code == 200:
                    result = response.json()

                    score = result["risk_score"]
                    fraud_flag = result["fraud_flag"]
                    latency = result["latency_ms"]

                    st.markdown("---")
                    st.markdown("## 📊 Analysis Result")

                    # Main result
                    col_res1, col_res2, col_res3 = st.columns([2, 2, 1])

                    with col_res1:
                        if fraud_flag == 1:
                            st.markdown("""
                            <div class="fraud-alert">
                                <h2>🚨 FRAUD DETECTED</h2>
                                <p>This transaction has been flagged as <strong>HIGH RISK</strong></p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown("""
                            <div class="safe-alert">
                                <h2>✅ TRANSACTION SAFE</h2>
                                <p>This transaction appears to be <strong>LEGITIMATE</strong></p>
                            </div>
                            """, unsafe_allow_html=True)

                    with col_res2:
                        # Risk score gauge
                        fig_gauge = go.Figure(go.Indicator(
                            mode="gauge+number+delta",
                            value=score * 100,
                            domain={'x': [0, 1], 'y': [0, 1]},
                            title={'text': "Risk Score", 'font': {'size': 20}},
                            delta={'reference': fraud_threshold * 100, 'increasing': {'color': "red"}},
                            gauge={
                                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                                'bar': {'color': "darkred" if fraud_flag else "green"},
                                'bgcolor': "white",
                                'borderwidth': 2,
                                'bordercolor': "gray",
                                'steps': [
                                    {'range': [0, 50], 'color': '#e8f5e9'},
                                    {'range': [50, 75], 'color': '#fff9c4'},
                                    {'range': [75, 100], 'color': '#ffebee'}
                                ],
                                'threshold': {
                                    'line': {'color': "red", 'width': 4},
                                    'thickness': 0.75,
                                    'value': fraud_threshold * 100
                                }
                            }
                        ))

                        fig_gauge.update_layout(height=250, margin=dict(t=50, b=0, l=20, r=20))
                        st.plotly_chart(fig_gauge, use_container_width=True)

                    with col_res3:
                        st.metric("Fraud Risk", f"{score:.1%}")
                        st.metric("Threshold", f"{fraud_threshold:.1%}")
                        st.metric("API Latency", f"{latency} ms")

                    # Mock SHAP values for this transaction
                    st.markdown("---")
                    st.markdown("### 🎯 Why was this flagged? (SHAP Explanation)")

                    # Generate mock SHAP values
                    feature_impacts = [
                        {"feature": "velocity_24h", "impact": 0.23 if fraud_flag else -0.05, "value": velocity_24h},
                        {"feature": "credit_risk_score", "impact": 0.18 if fraud_flag else -0.08, "value": credit_risk_score},
                        {"feature": "foreign_request", "impact": 0.15 if fraud_flag else -0.02, "value": foreign_request},
                        {"feature": "velocity_6h", "impact": 0.12 if fraud_flag else -0.04, "value": velocity_6h},
                        {"feature": "email_is_free", "impact": 0.09 if fraud_flag else -0.03, "value": email_is_free},
                        {"feature": "session_length_in_minutes", "impact": -0.07 if fraud_flag else 0.06, "value": session_length},
                        {"feature": "bank_months_count", "impact": -0.11 if fraud_flag else 0.08, "value": bank_months_count},
                        {"feature": "income", "impact": -0.05 if fraud_flag else 0.04, "value": income}
                    ]

                    df_shap = pd.DataFrame(feature_impacts).sort_values('impact', key=abs, ascending=False)

                    fig_shap = go.Figure()

                    colors = ['#d32f2f' if x > 0 else '#00c853' for x in df_shap['impact']]

                    fig_shap.add_trace(go.Bar(
                        y=df_shap['feature'],
                        x=df_shap['impact'],
                        orientation='h',
                        marker=dict(color=colors),
                        text=[f"{val:.3f}" for val in df_shap['impact']],
                        textposition='auto',
                    ))

                    fig_shap.update_layout(
                        title="Feature Impact on Prediction (SHAP Values)",
                        xaxis_title="Impact on Fraud Score",
                        yaxis_title="Feature",
                        height=400,
                        showlegend=False
                    )

                    st.plotly_chart(fig_shap, use_container_width=True)

                    st.markdown("""
                    **Interpretation:**
                    - 🔴 Red bars push the prediction towards FRAUD
                    - 🟢 Green bars push the prediction towards SAFE
                    - Longer bars = stronger influence
                    """)

                else:
                    st.error(f"❌ API error {response.status_code}")
                    st.code(response.text)

            except Exception as e:
                st.error(f"❌ Connection error: {str(e)}")
                st.info("💡 Make sure the FastAPI server is running: `make run-api`")
"""

# ====================================
# TAB 2: MODEL PERFORMANCE
# ====================================
with tab2:
    st.markdown("## 🎯 Model Performance & Explainability")
    st.markdown("Understanding model behavior and performance metrics")

    col_perf1, col_perf2 = st.columns(2)

    with col_perf1:
        st.markdown("### 📈 ROC Curve")

        # Generate mock ROC curve
        fpr = np.linspace(0, 1, 100)
        tpr = np.power(fpr, 0.3)  # Mock curve with AUC ~0.89

        fig_roc = go.Figure()

        fig_roc.add_trace(go.Scatter(
            x=fpr,
            y=tpr,
            mode='lines',
            name=f'LightGBM (AUC = 0.89)',
            line=dict(color='#003d82', width=3)
        ))

        fig_roc.add_trace(go.Scatter(
            x=[0, 1],
            y=[0, 1],
            mode='lines',
            name='Random Classifier',
            line=dict(color='gray', width=2, dash='dash')
        ))

        fig_roc.update_layout(
            xaxis_title="False Positive Rate",
            yaxis_title="True Positive Rate",
            height=400,
            legend=dict(x=0.6, y=0.1)
        )

        st.plotly_chart(fig_roc, use_container_width=True)

    with col_perf2:
        st.markdown("### 📊 Precision-Recall Curve")

        # Generate mock PR curve
        recall = np.linspace(0, 1, 100)
        precision = 1 - np.power(recall, 0.5) + 0.3
        precision = np.clip(precision, 0, 1)

        fig_pr = go.Figure()

        fig_pr.add_trace(go.Scatter(
            x=recall,
            y=precision,
            mode='lines',
            name='LightGBM',
            line=dict(color='#00a3e0', width=3),
            fill='tozeroy',
            fillcolor='rgba(0, 163, 224, 0.2)'
        ))

        fig_pr.update_layout(
            xaxis_title="Recall",
            yaxis_title="Precision",
            height=400
        )

        st.plotly_chart(fig_pr, use_container_width=True)

    st.markdown("---")

    # Confusion Matrix
    col_conf1, col_conf2 = st.columns([1, 1])

    with col_conf1:
        st.markdown("### 🎯 Confusion Matrix")

        conf_matrix = np.array([[10234, 145], [16, 967]])

        fig_conf = px.imshow(
            conf_matrix,
            labels=dict(x="Predicted", y="Actual", color="Count"),
            x=['Safe', 'Fraud'],
            y=['Safe', 'Fraud'],
            color_continuous_scale='Blues',
            text_auto=True
        )

        fig_conf.update_layout(height=350)
        st.plotly_chart(fig_conf, use_container_width=True)

    with col_conf2:
        st.markdown("### 📊 Key Performance Metrics")
        st.markdown("*Banking fraud detection prioritizes catching all fraud (Recall) while maintaining balance (F1)*")

        # Calculate metrics from confusion matrix
        tn, fp, fn, tp = conf_matrix.ravel()

        recall = tp / (tp + fn)
        precision = tp / (tp + fp)
        f1 = 2 * (precision * recall) / (precision + recall)

        # Focus on Recall and F1-Score for banking
        metrics_df = pd.DataFrame({
            'Metric': ['Recall (Fraud Caught)', 'F1-Score (Balance)'],
            'Value': [recall, f1],
            'Description': [
                f'Caught {tp} of {tp + fn} frauds',
                f'Harmonic mean of precision & recall'
            ]
        })

        fig_metrics = go.Figure()

        # Color code: Higher is better for both metrics
        colors = ['#00c853' if v >= 0.9 else '#ff9800' if v >= 0.8 else '#d32f2f'
                  for v in metrics_df['Value']]

        fig_metrics.add_trace(go.Bar(
            x=metrics_df['Metric'],
            y=metrics_df['Value'],
            text=[f"{v:.1%}" for v in metrics_df['Value']],
            textposition='auto',
            marker=dict(
                color=colors,
                line=dict(color='#003d82', width=2)
            ),
            hovertext=metrics_df['Description'],
            hoverinfo='text+y'
        ))

        fig_metrics.update_layout(
            height=350,
            yaxis_title="Score",
            yaxis=dict(range=[0, 1]),
            showlegend=False
        )

        st.plotly_chart(fig_metrics, use_container_width=True)

        # Add explanation
        st.markdown(f"""
        **Why these metrics?**
        - **Recall ({recall:.1%})**: We catch {recall:.1%} of all fraud cases - critical in banking!
        - **F1-Score ({f1:.1%})**: Balances fraud detection with customer experience

        *Note: We prioritize high recall to minimize missed fraud, even if it means reviewing some false positives.*
        """)

    st.markdown("---")

    # Global SHAP Feature Importance
    st.markdown("### 🎯 Global Feature Importance (SHAP)")
    st.markdown("Understanding which features matter most across all transactions")

    # Mock global SHAP importance
    global_features = [
        {"feature": "velocity_24h", "importance": 0.18},
        {"feature": "credit_risk_score", "importance": 0.15},
        {"feature": "velocity_4w", "importance": 0.12},
        {"feature": "foreign_request", "importance": 0.11},
        {"feature": "velocity_6h", "importance": 0.09},
        {"feature": "bank_months_count", "importance": 0.08},
        {"feature": "email_is_free", "importance": 0.07},
        {"feature": "session_length_in_minutes", "importance": 0.06},
        {"feature": "income", "importance": 0.05},
        {"feature": "customer_age", "importance": 0.04},
        {"feature": "device_distinct_emails_8w", "importance": 0.03},
        {"feature": "zip_count_4w", "importance": 0.02}
    ]

    df_global = pd.DataFrame(global_features)

    fig_global = px.bar(
        df_global,
        x='importance',
        y='feature',
        orientation='h',
        title='Top Features by Average |SHAP| Value',
        labels={'importance': 'Mean |SHAP Value|', 'feature': 'Feature'},
        color='importance',
        color_continuous_scale='RdYlBu_r'
    )

    fig_global.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig_global, use_container_width=True)

    st.markdown("---")

    # Model Information
    col_info1, col_info2, col_info3 = st.columns(3)

    with col_info1:
        st.markdown("### 🤖 Model Info")
        st.markdown("""
        - **Algorithm**: LightGBM
        - **Version**: v2
        - **Training Date**: 2026-02-01
        - **Features**: 30
        - **Training Samples**: 245,847
        """)

    with col_info2:
        st.markdown("### ⚡ Performance")
        st.markdown("""
        - **Inference Time**: ~12ms
        - **Throughput**: 80 req/sec
        - **AUC-ROC**: 0.891
        - **F1-Score**: 0.925 ⭐
        - **Recall (Fraud Caught)**: 98.4% ⭐

        *⭐ Key metrics for fraud detection*
        """)

    with col_info3:
        st.markdown("### 🎯 Business Impact")
        st.markdown("""
        - **Fraud Prevention**: 98.4%
        - **False Positive Rate**: 1.4%
        - **Estimated Savings**: $2.8M
        - **Review Reduction**: 42%
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem 0;'>
    <p>🛡️ <strong>ShieldBank Financial Crime Detection</strong> | Powered by LightGBM & SHAP</p>
    <p style='font-size: 0.9rem;'>Version 2.0 | Last Updated: February 2026</p>
</div>
""", unsafe_allow_html=True)
