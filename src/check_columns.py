import pandas as pd

df = pd.read_parquet("data/parquet/brfss_full.parquet")

CANDIDATES = [
    "_STATE", "SEXVAR", "_AGEG5YR", "_BMI5", "GENHLTH",
    "_SMOKER3", "DIABETE4", "_RACE", "EDUCA", "INCOME3",
    "_TOTINDA", "PHYSHLTH", "MENTHLTH", "_MICHD", "ASTHMA3",
]

for col in CANDIDATES:
    if col not in df.columns:
        print(f"{col:10s} ABSENTE")
        continue
    manquants = df[col].isna().mean() * 100
    distinctes = df[col].nunique()
    print(f"{col:10s} manquants: {manquants:5.1f} %   valeurs distinctes: {distinctes}")