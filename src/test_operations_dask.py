import dask.dataframe as dd
from operations_dask import * 

from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
DATA = RACINE / "data" / "parquet"

ddf = dd.read_parquet(DATA / "brfss_25.parquet", blocksize="5MB")
print("Nombre de partitions :", ddf.npartitions)

print("Sélection :", op_selection(ddf).shape)
print("Filtrage  :", op_filtrage(ddf).shape)
print("Groupby   :\n", op_group(ddf).head())
print("Nouvelle variable :\n", op_new_var(ddf).value_counts())
print("Stats     :\n", op_stats(ddf))