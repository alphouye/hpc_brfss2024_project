import pandas as pd

COLONNES = [
    "_STATE", "SEXVAR", "_AGEG5YR", "_BMI5", "GENHLTH",
    "_SMOKER3", "DIABETE4", "_RACE", "EDUCA", "INCOME3",
    "_TOTINDA", "PHYSHLTH", "MENTHLTH", "_MICHD", "ASTHMA3",
]

def op_selection(df):
    return df[COLONNES]

def op_filtrage(df):
    return df[(df["_AGEG5YR"] >= 9) & (df["_AGEG5YR"] <= 13) & (df["_BMI5"].notna())]

def op_group(df):
    return df.assign(bmi=df["_BMI5"] / 100).groupby("_STATE")["bmi"].mean()

def op_new_var(df):
    bmi = df["_BMI5"] / 100
    return pd.cut(bmi, bins = [0, 18.5, 25, 30, 100],
                  labels=["insuffisant", "normal", "surpoids", "obese"])

def op_stats(df):
    x = df["PHYSHLTH"].replace(88, 0)
    x = x[~x.isin([77, 99])]
    return x.describe()