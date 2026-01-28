

from fastapi import FastAPI
from pydantic import BaseModel
from src.inference import predict_single

app = FastAPI(
    title="Bank Account Fraud Detection API",
    version="1.0"
)

@app.get("/")
def health():
    return {"status": "ok"}


class TransactionInput(BaseModel):
    income: float
    customer_age: int
    credit_risk_score: int
    proposed_credit_limit: float
    intended_balcon_amount: float
    session_length_in_minutes: float
    days_since_request: float
    bank_months_count: int
    zip_count_4w: int
    velocity_6h: float
    velocity_24h: float
    velocity_4w: float
    bank_branch_count_8w: int
    device_distinct_emails_8w: int
    date_of_birth_distinct_emails_4w: int
    prev_address_months_count: int
    current_address_months_count: int
    email_is_free: int
    phone_home_valid: int
    phone_mobile_valid: int
    has_other_cards: int
    foreign_request: int
    keep_alive_session: int
    employment_status: str
    housing_status: str
    payment_type: str
    source: str
    device_os: str
    month: int


@app.post("/predict")
def predict(transaction: TransactionInput):
    print(transaction.dict().keys())
    return predict_single(transaction.dict())
