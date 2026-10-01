import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path

SRC=Path("data/parquet/brfss_full.parquet")
OUT=Path("data/parquet")
SEED=42
GROUP_SIZE=50000

df = pd.read_parquet(SRC)
df = df.sample(frac=1, random_state=SEED).reset_index(drop=True)
table = pa.Table.from_pandas(df, preserve_index=False)
n = table.num_rows
del df

for size in (10, 25, 50, 100):
    taille = int(n * size / 100)
    pq.write_table(table.slice(0, taille), OUT / f"brfss_{size}.parquet", compression="snappy", row_group_size=GROUP_SIZE)
    print(f"brfss_{size}.parquet : {taille} lignes")

for k in (2, 3):
    with pq.ParquetWriter(OUT / f"brfss_x{k}.parquet", table.schema, compression="snappy") as writer:
        for _ in range(k):
            writer.write_table(table, row_group_size=GROUP_SIZE)
    print(f"brfss_x{k}.parquet : {n * k} lignes")