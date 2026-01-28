# Analyse de l'Évolution des Stéréotypes au Cinéma (1960-2020)

## 📌 Présentation du Projet

Ce projet analyse l'évolution des stéréotypes (sexisme, racisme, homophobie) dans les scripts de films entre **1960 et 2020**, en utilisant des techniques de **traitement automatique du langage (NLP)** et d'analyse quantitative.

### 🎯 Questions de Recherche

1. **Comment la représentation des femmes a-t-elle évolué dans les dialogues de films ?**
   - Fréquence des mentions femmes vs hommes
   - Évolution des stéréotypes genrés (émotionnelle, faible, etc.)
   - Objectification et descriptions physiques

2. **Les groupes ethniques minoritaires sont-ils sous-représentés ?**
   - Ratio de mentions par groupe ethnique
   - Évolution de la diversité ethnique
   - Stéréotypes raciaux (criminalité, exotisme, pauvreté)

3. **Comment les stéréotypes ont-ils évolué décennie par décennie ?**
   - Tendances quantitatives par période
   - Comparaison années 1960 vs 2020
   - Points de rupture et évolutions significatives

### 💡 Hypothèses

- **H1** : La représentation des femmes dans les scripts a augmenté depuis 1960, mais reste inférieure à celle des hommes
- **H2** : Les stéréotypes négatifs sur les femmes (émotionnelle, faible) ont diminué depuis les années 1960
- **H3** : Les groupes ethniques minoritaires sont significativement sous-représentés, surtout avant les années 2000
- **H4** : Les associations négatives (criminalité, pauvreté) avec les minorités ont diminué mais persistent

---

## 🗂️ Structure du Projet

```
movie_scripts_analysis/
├── data/
│   ├── raw/                # Scripts .txt de Kaggle (non versionnés)
│   ├── meta/               # Fichiers CSV avec métadonnées (titres, années)
│   └── processed/          # Données nettoyées (scripts_clean.pkl)
│
├── src/
│   ├── __init__.py
│   ├── parser.py           # Parsing et nettoyage des scripts (Regex)
│   ├── dictionaries.py     # Listes de mots pour sexisme/racisme/homophobie
│   └── stats_analysis.py   # Calcul des fréquences relatives par décennie
│
├── notebooks/
│   ├── 0_clean_data.ipynb  # Téléchargement et nettoyage massif
│   ├── 1_gender_bias.ipynb # Analyse du sexisme (femmes vs hommes)
│   └── 2_ethnic_bias.ipynb # Analyse des biais ethniques/raciaux
│
├── results/
│   ├── figures/            # Graphiques (évolution par décennie, ratios, etc.)
│   ├── gender_bias_by_decade.csv
│   ├── ethnic_bias_by_decade.csv
│   └── models/             # Modèles Word2Vec ou LDA (si utilisés)
│
├── requirements.txt        # Dépendances Python
└── README.md               # Ce fichier
```

---

## 🚀 Installation et Utilisation

### 1. Cloner le projet

```bash
git clone <votre-repo>
cd movie_scripts_analysis
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

**Dépendances principales :**
- `pandas`, `numpy` : Manipulation de données
- `matplotlib`, `seaborn` : Visualisation
- `nltk` : Tokenisation et stopwords
- `kagglehub` : Téléchargement du dataset
- `gensim` : Word embeddings (Word2Vec)
- `spacy` : Lemmatisation avancée (optionnel)

### 3. Configurer Kaggle API (pour télécharger le dataset)

1. Créer un compte sur [Kaggle](https://www.kaggle.com/)
2. Télécharger votre clé API : **Profile → API → Create New API Token**
3. Placer le fichier `kaggle.json` dans `~/.kaggle/`

```bash
mkdir -p ~/.kaggle
mv ~/Downloads/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json
```

### 4. Exécuter les notebooks dans l'ordre

#### a) Nettoyage des données
```bash
jupyter notebook notebooks/0_clean_data.ipynb
```
- Télécharge le dataset **Movie Scripts Corpus** de Kaggle
- Nettoie les scripts avec Regex
- Sauvegarde `data/processed/scripts_clean.pkl`

#### b) Analyse du sexisme
```bash
jupyter notebook notebooks/1_gender_bias.ipynb
```
- Calcule les fréquences de mentions femmes vs hommes
- Analyse les stéréotypes genrés
- Génère des graphiques d'évolution

#### c) Analyse des biais ethniques
```bash
jupyter notebook notebooks/2_ethnic_bias.ipynb
```
- Analyse la représentation des groupes ethniques
- Stéréotypes raciaux (criminalité, exotisme, pauvreté)
- Co-occurrences de mots

---

## 📊 Méthodologie

### 1. **Acquisition des Données**

**Source** : [Movie Scripts Corpus (Kaggle)](https://www.kaggle.com/datasets/gufukuro/movie-scripts-corpus)
- **~1500 scripts** de films (formats .txt)
- **Métadonnées** : titres, années de sortie, genres

**Période étudiée** : 1960-2020 (6 décennies)

### 2. **Prétraitement**

- **Nettoyage Regex** : Suppression des indications scéniques, numéros de scène
- **Tokenisation** : Découpage en mots
- **Lemmatisation** : Normalisation (optionnel)
- **Suppression des stopwords** : Mots vides (the, a, is, etc.)

### 3. **Dictionnaires de Mots-Clés**

Création de listes de mots pour chaque catégorie de biais :

#### Sexisme (`dictionaries.py`)
```python
GENDER_WORDS = {
    'female': ['woman', 'women', 'girl', 'she', 'her', ...],
    'male': ['man', 'men', 'boy', 'he', 'him', ...]
}

GENDER_STEREOTYPES = {
    'female_negative': ['emotional', 'hysterical', 'weak', ...],
    'female_objectification': ['beautiful', 'sexy', 'hot', ...],
    'male_stereotypes': ['strong', 'brave', 'dominant', ...]
}
```

#### Racisme (`dictionaries.py`)
```python
ETHNICITY_WORDS = {
    'african_american': ['black', 'african', ...],
    'asian': ['asian', 'chinese', 'japanese', ...],
    'hispanic': ['hispanic', 'latino', 'mexican', ...],
    'white': ['white', 'caucasian', ...]
}

RACIAL_STEREOTYPES = {
    'criminal': ['thug', 'gangster', 'violent', ...],
    'exotic': ['exotic', 'mysterious', 'oriental', ...],
    'poverty': ['poor', 'ghetto', 'slum', ...]
}
```

### 4. **Calcul des Fréquences Relatives**

Pour chaque décennie et catégorie :

$$
\text{Fréquence relative} = \frac{\text{Nb occurrences mot-clé}}{\text{Nb total de mots}} \times 1000
$$

**Exemple** : Si "woman" apparaît 50 fois dans un script de 10 000 mots → fréquence = 5 pour 1000 mots.

### 5. **Analyse Statistique**

- **Ratios** : Femmes/Hommes, Minorités/Blancs
- **Tendances** : Régression linéaire pour détecter augmentation/diminution
- **Comparaisons** : Tests de significativité (t-tests) entre décennies

### 6. **Visualisations**

- Histogrammes par décennie
- Courbes d'évolution temporelle
- Boxplots de distribution
- Heatmaps de corrélations

---

## 📈 Résultats Attendus

### Graphiques Générés

1. **`gender_mentions_by_decade.png`** : Barres comparant mentions femmes vs hommes
2. **`gender_ratio_evolution.png`** : Courbe du ratio femmes/hommes
3. **`gender_stereotypes.png`** : Évolution des stéréotypes négatifs
4. **`ethnic_mentions_by_decade.png`** : Mentions des groupes ethniques
5. **`racial_stereotypes.png`** : Associations négatives par décennie

### Fichiers de Résultats

- **`results/gender_bias_by_decade.csv`** : Statistiques agrégées par décennie
- **`results/ethnic_bias_by_decade.csv`** : Biais ethniques par décennie
- **`results/gender_bias_by_film.csv`** : Métriques détaillées par film

---

## 🔍 Pistes d'Amélioration

### Analyses Complémentaires

1. **Word Embeddings (Word2Vec)**
   - Entraîner un modèle par décennie
   - Analyser l'évolution sémantique de "woman", "black", etc.
   - Visualiser avec t-SNE

2. **Topic Modeling (LDA)**
   - Identifier les thèmes dominants par décennie
   - Tracker l'évolution des sujets liés aux minorités

3. **Analyse de Graphes**
   - Graphes d'interaction entre personnages
   - Mesure de centralité par genre et ethnicité

4. **Analyse de Sentiments**
   - Polarité des dialogues associés à chaque groupe
   - Évolution du ton (positif/négatif)

5. **Intersectionnalité**
   - Croisement genre × ethnicité
   - Analyse spécifique des femmes noires, asiatiques, etc.

---

## 📚 Références

### Datasets

- [Movie Scripts Corpus (Kaggle)](https://www.kaggle.com/datasets/gufukuro/movie-scripts-corpus)
- [CMU Movie Summary Corpus](http://www.cs.cmu.edu/~ark/personas/)

### Littérature Académique

1. **Linguistique Computationnelle**
   - Cours Maria Boritchev (Télécom Paris)
   - Jurafsky & Martin, *Speech and Language Processing*

2. **Biais dans les Médias**
   - Geena Davis Institute on Gender in Media
   - USC Annenberg Inclusion Initiative

3. **NLP et Biais**
   - Bolukbasi et al. (2016), *Man is to Computer Programmer as Woman is to Homemaker?*
   - Caliskan et al. (2017), *Semantics derived automatically from language corpora*

---

## 👥 Auteurs

- **Antoine Ollivier** - Télécom Paris (Promo 2026)
- **Projet** : Computational Science (Créneau D)

---

## 📝 Licence

Projet académique - Télécom Paris 2025

---

## 🆘 Contact

Pour toute question :
- Email : antoine.ollivier@telecom-paris.fr
- GitHub : [Votre pseudo GitHub]

---

**Dernière mise à jour** : Janvier 2026
