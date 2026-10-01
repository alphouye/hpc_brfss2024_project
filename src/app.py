import streamlit as st
import pandas as pd
import dask.dataframe as dd
import time
from pathlib import Path

import operations as pd_ops
import operations_dask as dask_ops

RACINE = Path(__file__).resolve().parent.parent
DATA = RACINE / "data" / "parquet"

st.title("Exploration BRFSS 2024")

taille = st.selectbox("Taille des données", ["10", "25", "50", "100", "2", "3"])
operation = st.selectbox("Opération", ["selection", "filtrage", "group", "new_var", "stats"])
technos = st.multiselect("Technologies à comparer", ["pandas", "dask"], default=["pandas", "dask"])

chemin = DATA / f"brfss_{taille}.parquet"

if st.button("Lancer"):
    for techno in technos:
        debut = time.perf_counter()
        if techno == "pandas":
            df = pd.read_parquet(chemin)
            fonction = getattr(pd_ops, f"op_{operation}")
            resultat = fonction(df)
        else:
            ddf = dd.read_parquet(chemin)
            fonction = getattr(dask_ops, f"op_{operation}")
            resultat = fonction(ddf)
        temps = time.perf_counter() - debut

        st.subheader(f"{techno} — {temps:.3f} s")
        if operation == "group":
            st.bar_chart(resultat)
        elif operation == "new_var":
            st.bar_chart(resultat.value_counts())
        else:
            st.write(resultat.shape)
            st.dataframe(resultat.head(100))