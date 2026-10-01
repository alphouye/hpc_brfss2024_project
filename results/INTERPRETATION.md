# Interprétation des résultats – Benchmark Pandas vs Dask

## 1. Protocole expérimental

- **Dataset** : BRFSS 2024 (~457 000 individus, 301 variables)
- **Technologies comparées** : Pandas, Dask
- **Tailles testées** : 10 %, 25 %, 50 %, 100 % du dataset
- **Opérations mesurées** :
  - `selection` : sélection de colonnes
  - `filtrage` : filtrage de lignes selon une condition
  - `group` : agrégation par groupe (groupby)
  - `new_var` : création d'une nouvelle variable
  - `stats` : calcul de statistiques descriptives


## 2. Analyse

### 2.1 Pandas est plus rapide que Dask

Sur les opérations de traitement, Pandas est nettement plus rapide que Dask.
Par exemple, le **filtrage sur 100 % des données** prend 0,14 s avec Pandas
contre 1,95 s avec Dask, soit un facteur d'environ **14**. Mais Dask reste plus
performant sur des opérations comme stats ou de nouvelle variables (new_var) ou
il est nettement plus rapide.

### 2.2 Pourquoi Dask est plus lent ici

Ce résultat est attendu et s'explique par le fonctionnement de Dask :

- **Overhead de planification** : Dask découpe les données en partitions,
  construit un graphe de tâches puis l'exécute via `.compute()`. Ce coût fixe
  est élevé par rapport à des opérations qui ne durent que quelques millisecondes.
- **Les données tiennent en mémoire** : avec 457 000 lignes, le dataset est
  traité directement en RAM par Pandas. Le découpage en partitions de Dask
  n'apporte alors aucun bénéfice.
- **Évaluation paresseuse (lazy)** : chaque appel à `.compute()` peut relancer
  une partie de la chaîne de calcul, ce qui ajoute du temps.

### 2.3 Évolution avec la taille

- **Filtrage (Dask)** : le temps croît de façon quasi linéaire avec la taille
  (0,17 s → 0,46 s → 0,89 s → 1,95 s). Le coût est proportionnel au volume traité.
- **Group (Dask)** : 0,81 s à 50 %, soit l'une des opérations les plus coûteuses.
  Un groupby nécessite des échanges de données entre partitions,
  ce qui est particulièrement cher dans Dask.
- **Opérations légères** (`selection`, `new_var`, `stats`) : elles restent
  rapides pour les deux technologies (de l'ordre de quelques centièmes de seconde).

## 3. Limites

- **Mesure unique** : chaque test n'a été exécuté qu'une fois. Une moyenne sur
  plusieurs exécutions rendrait les résultats plus robustes face aux variations
  de la machine.
- **Temps de lecture identiques** : Pandas et Dask affichent exactement le même
  temps de lecture à chaque taille, ce qui est très improbable entre deux mesures
  réelles. Il s'agit probablement d'une même mesure attribuée aux deux
  technologies. Cette opération est donc exclue de la comparaison.
- **Périmètre** : Polars et la comparaison des formats CSV/Parquet n'ont pas
  été testés. Ce sont des pistes d'extension.
- **Échelle limitée** : le dataset tient en mémoire, ce qui ne permet pas
  d'observer le cas d'usage principal de Dask.

## 4. Conclusion

Pour un dataset de cette taille, Pandas est le choix le plus adapté :
il est plus simple à utiliser et nettement plus rapide. Dask devient pertinent
lorsque les données dépassent la mémoire disponible ou lorsqu'on souhaite
paralléliser les calculs sur plusieurs cœurs ou machines. Pour observer un gain,
il faudrait tester des volumes beaucoup plus importants, par exemple plusieurs
années de BRFSS concaténées.