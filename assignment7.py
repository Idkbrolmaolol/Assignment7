import pandas as pd
import re

def normalize_schema(df):
    df = df.copy()

    nan_before = df.isna().sum()
    inferred = {}

    for col in df.columns:
        s = df[col]

        if not s.dtype == object:
            inferred[col] = str(s.dtype)
            continue

        # try numeric
        numeric = pd.to_numeric(s, errors="coerce")
        numeric_rate = numeric.notna().sum() / s.notna().sum()

        # try datetime
        dt = pd.to_datetime(s, errors="coerce")
        dt_rate = dt.notna().sum() / s.notna().sum()

        # try currency
        cleaned = (
            s.astype(str)
             .str.replace(r"[^\d.\-]", "", regex=True)
             .replace("nan", pd.NA)
        )
        currency = pd.to_numeric(cleaned, errors="coerce")
        currency_rate = currency.notna().sum() / s.notna().sum()

        if currency_rate >= 0.6:
            df[col] = currency
            inferred[col] = "currency"
        elif numeric_rate >= 0.6:
            df[col] = numeric
            inferred[col] = "numeric"
        elif dt_rate >= 0.6:
            df[col] = dt
            inferred[col] = "datetime"
        else:
            df[col] = s.astype("string")
            inferred[col] = "string"

    nan_after = df.isna().sum()

    report = pd.DataFrame({
        "type": inferred,
        "nan_before": nan_before,
        "nan_after": nan_after
    })

    return df, report


df_clean, report = normalize_schema(df)
print(df_clean)
print(report)