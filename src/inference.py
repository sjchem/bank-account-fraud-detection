# logic-main/inference.py

import time
import pandas as pd
import numpy as np

from src.config import (
    FEATURES,
    MODEL_PATH,
    MODEL_VERSION,
    FRAUD_THRESHOLD,
)

from src.model import load_model
from src.features import add_interaction_features
from src.preprocessing import cast_categorical

# Load once at startup
model = load_model(MODEL_PATH)

def predict_single(transaction: dict) -> dict:
    """
    Real-time fraud prediction (FastAPI)
    """
    start_time = time.time()

    df = pd.DataFrame([transaction])
    df = add_interaction_features(df)
    df = cast_categorical(df)

    score = float(model.predict(df[FEATURES])[0])

    latency_ms = round((time.time() - start_time) * 1000, 2)

    return {
        "model_version": MODEL_VERSION,
        "risk_score": round(score, 4),
        "fraud_flag": int(score >= FRAUD_THRESHOLD),
        "latency_ms": latency_ms
    }
