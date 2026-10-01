# Calcul haute performance — Pipeline data pour la santé

## Objectif

Comparer différentes technologies data (Pandas, Dask) sur un jeu de données de santé
publique (BRFSS 2024), à travers un benchmark d'opérations courantes, puis exploiter
les résultats dans un dashboard interactif.

## Dataset

BRFSS 2024: enquête de santé
publique américaine, environ 457 670 répondants et 301 variables.


## Structure du projet

```
.
├── data/
│   └── parquet/           Jeu de données converti, à différentes tailles
├── results/
│   ├── profil_colonnes.csv    Profil des colonnes (types, manquants, cardinalité)
│   ├── timings.csv             Résultats bruts du benchmark
│   └── INTERPRETATION.md       Document de synthèse (méthodologie, résultats, analyse)
└── src/
    ├── prepare_data.py         Conversion du fichier XPT en Parquet
    ├── generate_sizes.py       Génération des différentes tailles de données
    ├── operations.py           Opérations du benchmark (Pandas)
    ├── operations_dask.py      Opérations du benchmark (Dask)
    ├── benchmark.py            Harnais de mesure, génère results/timings.csv
    └── app.py                  Dashboard interactif (Streamlit)
```

## Utilisation

Toutes les commandes sont à lancer depuis la racine du projet.

### 1. Préparer les données

Uniquement nécessaire si `data/parquet/brfss_full.parquet` n'existe pas encore
(sinon, passer directement à l'étape 2 avec les fichiers déjà fournis).

```bash
python src/prepare_data.py
```

Convertit `data/raw/LLCP2024.XPT` en `data/parquet/brfss_full.parquet`.
LLCP2024.XPT etant trop lourd pour la compression, il a été enlevé du folder

### 2. Générer les différentes tailles de données

```bash
python src/generate_sizes.py
```

Produit, dans `data/parquet/` : `brfss_10.parquet`, `brfss_25.parquet`,
`brfss_50.parquet`, `brfss_100.parquet`, `brfss_x2.parquet`, `brfss_x3.parquet`
(10 %, 25 %, 50 %, 100 % du dataset, puis duplications ×2 et ×3).

### 3. Lancer le benchmark

```bash
python src/benchmark.py
```

Exécute les 5 opérations (sélection, filtrage, groupby, nouvelle variable,
statistiques descriptives) avec Pandas et Dask, sur chaque taille de données,
et enregistre les temps mesurés dans `results/timings.csv`.

### 4. Lancer le dashboard

```bash
streamlit run src/app.py
```

Ouvre une interface web permettant de choisir une taille de données, une
opération et une ou plusieurs technologies, puis d'afficher le résultat et
le temps d'exécution mesuré.

### 5. Consulter l'analyse

Le notebook `notebook/explorations.ipynb` contient l'exploration initiale du
dataset. Le document `results/INTERPRETATION.md` présente la méthodologie,
les résultats du benchmark et les recommandations.

## Reda LAHLOU KASSI
