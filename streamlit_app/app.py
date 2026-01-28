import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(
    page_title="Bank Fraud Detection",
    page_icon="🏦",
    layout="centered"
)

st.title("🏦 Bank Account Fraud Detection")
st.markdown("Real-time fraud scoring powered by LightGBM")

st.divider()


with st.form("transaction_form"):
    st.subheader("Transaction Details")

    income = st.number_input("Income", min_value=0.0, value=50000.0)
    customer_age = st.number_input("Customer Age", min_value=18, value=35)
    credit_risk_score = st.number_input("Credit Risk Score", min_value=0, value=600)

    proposed_credit_limit = st.number_input("Proposed Credit Limit", value=3000.0)
    intended_balcon_amount = st.number_input("Intended Balance Amount", value=1200.0)

    session_length = st.number_input("Session Length (minutes)", value=8.5)
    days_since_request = st.number_input("Days Since Request", value=1.0)

    bank_months_count = st.number_input("Bank Months Count", value=12)
    zip_count_4w = st.number_input("Zip Count (4w)", value=3)

    velocity_6h = st.number_input("Velocity 6h", value=1.2)
    velocity_24h = st.number_input("Velocity 24h", value=3.4)
    velocity_4w = st.number_input("Velocity 4w", value=8.9)

    st.subheader("Binary Flags")
    email_is_free = st.selectbox("Email is Free", [0, 1])
    phone_home_valid = st.selectbox("Phone Home Valid", [0, 1])
    phone_mobile_valid = st.selectbox("Phone Mobile Valid", [0, 1])
    has_other_cards = st.selectbox("Has Other Cards", [0, 1])
    foreign_request = st.selectbox("Foreign Request", [0, 1])
    keep_alive_session = st.selectbox("Keep Alive Session", [0, 1])

    st.subheader("Categorical Features")

    employment_status = st.selectbox(
        "Employment Status",
        ["employed", "self-employed", "unemployed", "student"]
    )

    housing_status = st.selectbox(
        "Housing Status",
        ["rent", "own", "mortgage"]
    )

    payment_type = st.selectbox(
        "Payment Type",
        ["credit_card", "debit_card", "bank_transfer"]
    )

    source = st.selectbox(
        "Source",
        ["web", "mobile"]
    )

    device_os = st.selectbox(
        "Device OS",
        ["android", "ios", "windows", "mac"]
    )

    month = st.selectbox("Month", list(range(1, 13)))

    st.subheader("Account & Identity History")

    bank_branch_count_8w = st.number_input(
        "Bank Branch Count (last 8 weeks)", value=1, min_value=0
    )

    device_distinct_emails_8w = st.number_input(
        "Device Distinct Emails (last 8 weeks)", value=1, min_value=0
    )

    date_of_birth_distinct_emails_4w = st.number_input(
        "DOB Distinct Emails (last 4 weeks)", value=1, min_value=0
    )

    prev_address_months_count = st.number_input(
        "Previous Address Months", value=24, min_value=0
    )

    current_address_months_count = st.number_input(
        "Current Address Months", value=12, min_value=0
    )

    submitted = st.form_submit_button("🔍 Predict Fraud Risk")

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

    # binary flags
    "email_is_free": email_is_free,
    "phone_home_valid": phone_home_valid,
    "phone_mobile_valid": phone_mobile_valid,
    "has_other_cards": has_other_cards,
    "foreign_request": foreign_request,
    "keep_alive_session": keep_alive_session,

    # categorical
    "employment_status": employment_status,
    "housing_status": housing_status,
    "payment_type": payment_type,
    "source": source,
    "device_os": device_os,
    "month": month,
    }

    with st.spinner("Calling fraud detection API..."):
        response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        result = response.json()

        st.divider()
        st.subheader("📊 Prediction Result")

        score = result["risk_score"]
        fraud_flag = result["fraud_flag"]
        latency = result["latency_ms"]

        st.metric("Fraud Risk Score", score)

        if fraud_flag == 1:
            st.error("🚨 FRAUD DETECTED")
        else:
            st.success("✅ NOT FRAUD")

        st.caption(f"API latency: {latency} ms")
    else:
        st.error(f"API error {response.status_code}")
        st.code(response.text)
