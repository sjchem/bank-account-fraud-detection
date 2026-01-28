
TARGET = "fraud_bool"

NUM_COLS = [
    "income","customer_age","credit_risk_score",
    "proposed_credit_limit","intended_balcon_amount",
    "session_length_in_minutes","days_since_request",
    "bank_months_count","zip_count_4w",
    "velocity_6h","velocity_24h","velocity_4w",
    "bank_branch_count_8w","device_distinct_emails_8w",
    "date_of_birth_distinct_emails_4w",
    "current_address_months_count","prev_address_months_count",
    "income_per_age","credit_utilization",
    "velocity_ratio","avg_velocity_per_hour"
]

BIN_COLS = [
    "email_is_free","phone_home_valid","phone_mobile_valid",
    "has_other_cards","foreign_request","keep_alive_session"
]

CAT_COLS = [
    "employment_status","housing_status","payment_type",
    "source","device_os","month"
]

FEATURES = NUM_COLS + BIN_COLS + CAT_COLS

MODEL_PATH = "models/lgb_modified.pkl"
RANDOM_STATE = 42
MODEL_VERSION = "v2"
FRAUD_THRESHOLD = 0.75   # precomputed offline
