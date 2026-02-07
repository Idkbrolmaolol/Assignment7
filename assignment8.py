import numpy as np
import pandas as pd

def iqr_bounds(s, k=1.5):
    q1 = s.quantile(0.25)
    q3 = s.quantile(0.75)
    iqr = q3 - q1
    low = q1 - k * iqr
    high = q3 + k * iqr
    return low, high

def detect_outliers_iqr(s, k=1.5):
    low, high = iqr_bounds(s, k=k)
    return (s < low) | (s > high)

def detect_outliers_zscore(s, threshold=3.0):
    x = s.astype(float)
    mu = x.mean()
    sigma = x.std(ddof=0)
    if sigma == 0:
        return pd.Series(False, index=s.index)
    z = (x - mu) / sigma
    return z.abs() > threshold

s = df["income"]

iqr_mask = detect_outliers_iqr(s, k=1.5)
z_mask = detect_outliers_zscore(s, threshold=3.0)

low, high = iqr_bounds(s, k=1.5)
df["income_iqr_capped"] = s.clip(lower=low, upper=high)
df["income_log1p"] = np.log1p(s)

summary = pd.DataFrame({
    "strategy": ["no_handling", "iqr_capping", "log1p"],
    "min": [s.min(), df["income_iqr_capped"].min(), df["income_log1p"].min()],
    "median": [s.median(), df["income_iqr_capped"].median(), df["income_log1p"].median()],
    "mean": [s.mean(), df["income_iqr_capped"].mean(), df["income_log1p"].mean()],
    "max": [s.max(), df["income_iqr_capped"].max(), df["income_log1p"].max()],
})

print("IQR outliers:", int(iqr_mask.sum()))
print("Z-score outliers:", int(z_mask.sum()))
print(summary)