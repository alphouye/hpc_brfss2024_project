import dask.dataframe as dd
import pandas as pd

COLONNES = [
    "_STATE", "SEXVAR", "_AGEG5YR", "_BMI5", "GENHLTH",
    "_SMOKER3", "DIABETE4", "_RACE", "EDUCA", "INCOME3",
    "_TOTINDA", "PHYSHLTH", "MENTHLTH", "_MICHD", "ASTHMA3",
]

def op_selection(ddf):
    return ddf[COLONNES].compute()

def op_filtrage(ddf):
    tmp = (ddf["_AGEG5YR"] >= 9) & (ddf["_AGEG5YR"] <= 13) & (ddf["_BMI5"].notnull())
    return ddf[tmp].compute()

def op_group(ddf):
    return ddf.assign(bmi=ddf["_BMI5"] / 100).groupby("_STATE")["bmi"].mean().compute()

def op_new_var(ddf):
    bmi = ddf["_BMI5"] / 100
    return bmi.map_partitions(
        pd.cut, bins=[0, 18.5, 25, 30, 100],
        labels=["insuffisant", "normal", "surpoids", "obese"]
    ).compute()

def op_stats(ddf):
    x = ddf["PHYSHLTH"].replace(88, 0)
    x = x[~x.isin([77, 99])]
    return x.describe().compute()