import pandas as pd
from operations import *


from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
DATA = RACINE / "data" / "parquet"

df = pd.read_parquet(DATA / "brfss_10.parquet")

print("Sélection :", op_selection(df).shape)
print("Filtrage  :", op_filtrage(df).shape)
print("Groupby   :\n", op_group(df).head())
print("Nouvelle variable :\n", op_new_var(df).value_counts())
print("Stats     :\n", op_stats(df))