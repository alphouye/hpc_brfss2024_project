import pandas as pd
from pathlib import Path

PARQUET = Path("data/parquet/brfss_full.parquet")
XPT = Path("data/raw/LLCP2024.XPT")
RESULTS = Path("results")
RESULTS.mkdir(exist_ok=True)

df = pd.read_parquet(PARQUET)

# 1. Dimensions et tailles
print("=== Dimensions ===")
print(df.shape)
print(f"Mémoire en RAM : {df.memory_usage(deep=True).sum() / 1e6:.0f} Mo")
print(f"Fichier XPT     : {XPT.stat().st_size / 1e6:.0f} Mo")
print(f"Fichier Parquet : {PARQUET.stat().st_size / 1e6:.0f} Mo")

# 2. Types
print("\n=== Types de colonnes ===")
print(df.dtypes.value_counts())

# 3. Valeurs manquantes
na = df.isna().mean().sort_values(ascending=False)
print("\n=== Colonnes les plus vides ===")
print(na.head(15))
print(f"\nColonnes à plus de 50 % de manquants : {(na > 0.5).sum()}")

# 4. Profil complet de chaque colonne, sauvegardé en CSV
profil = pd.DataFrame({
    "dtype": df.dtypes.astype(str),
    "pct_manquants": (df.isna().mean() * 100).round(2),
    "nb_valeurs_distinctes": df.nunique(),
})
profil.to_csv(RESULTS / "profil_colonnes.csv")
print("\nProfil complet sauvegardé dans results/profil_colonnes.csv")

# 5. Colonnes candidates (à adapter avec le codebook)
CANDIDATES = ["_STATE", "SEXVAR", "GENHLTH", "_AGEG5YR", "_BMI5"]

print("\n=== Colonnes candidates ===")
for col in CANDIDATES:
    if col not in df.columns:
        print(f"\n{col} : ABSENTE (vérifier le nom dans le codebook)")
        continue
    print(f"\n--- {col} ---")
    if df[col].nunique() <= 20:
        print(df[col].value_counts(dropna=False).sort_index())
    else:
        print(df[col].describe())