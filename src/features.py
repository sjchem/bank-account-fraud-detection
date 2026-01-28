
# src/features.py

import numpy as np
import pandas as pd

def add_interaction_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["income_per_age"] = df["income"] / df["customer_age"].clip(lower=18)
    df["credit_utilization"] = (
        df["intended_balcon_amount"] /
        df["proposed_credit_limit"].clip(lower=50)
    )
    df["velocity_ratio"] = (
        df["velocity_6h"] /
        df["velocity_4w"].clip(lower=1)
    )
    df["avg_velocity_per_hour"] = df["velocity_24h"] / 24

    return df
