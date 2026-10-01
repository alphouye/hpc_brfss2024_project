import time
import statistics
import pandas as pd
import dask.dataframe as dd
from pathlib import Path
import gc

import operations as pd_ops
import operations_dask as dask_ops

RACINE= Path(__file__).resolve().parent.parent
DATA =RACINE / "data" / "parquet"
RESULTS= RACINE / "results"
RESULTS.mkdir(exist_ok=True)

TAILLES = ["10", "25", "50", "100", "x2", "x3"]

OPERATIONS = ["selection", "filtrage", "group", "new_var", "stats"]

def mesure(fonction, *args, repet=5):
    temps=[]
    for i in range(repet):
        debut = time.perf_counter()
        fonction(*args)
        temps.append(time.perf_counter() - debut)
    return statistics.median(temps)

lines = []

for taille in TAILLES:
    path = DATA / f"brfss_{taille}.parquet"

    debut = time.perf_counter()
    df = pd.read_parquet(path)
    read_time_pd = time.perf_counter() - debut

    for nom_op in OPERATIONS:
        fonction = getattr(pd_ops, f"op_{nom_op}")
        temps = mesure(fonction, df)
        lines.append({"techno": "pandas", "operation": nom_op,
                        "taille": taille, "temps": temps})
        print(f"pandas  {taille:>4} {nom_op:<18} {temps:.4f} s")
    lines.append({"techno": "pandas", "operation": "lecture",
                    "taille": taille, "temps": read_time_pd})
    del df
    gc.collect()


    debut_dd = time.perf_counter()
    ddf = dd.read_parquet(path)
    read_time_dd = time.perf_counter() - debut_dd

    for nom_op in OPERATIONS:
            fonction = getattr(dask_ops, f"op_{nom_op}")
            temps = mesure(fonction, ddf)
            lines.append({"techno": "dask", "operation": nom_op,
                            "taille": taille, "temps": temps})
            print(f"dask  {taille:>4} {nom_op:<18} {temps:.4f} s")

    lines.append({"techno": "dask", "operation": "lecture",
                        "taille": taille, "temps": read_time_pd})

    del ddf
    gc.collect()
    

result = pd.DataFrame(lines)
result.to_csv(RESULTS / "timings.csv")
print("fini")