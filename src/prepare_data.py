import pandas as pd
from pathlib import Path

RAW = Path("data/raw/LLCP2024.XPT")
OUT = Path("data/parquet")
OUT.mkdir(parents=True, exist_ok=True)

df = pd.read_sas(RAW, format="xport", encoding='latin-1')
print(df.shape)

df.to_parquet(OUT / "brfss_full.parquet", engine="pyarrow", compression="snappy", index=False)
print("ji fini")