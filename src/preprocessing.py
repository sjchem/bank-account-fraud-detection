# logic-main/preprocessing.py

import pandas as pd
from src.config import CAT_COLS

def cast_categorical(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for c in CAT_COLS:
        df[c] = df[c].astype("category")
    return df
