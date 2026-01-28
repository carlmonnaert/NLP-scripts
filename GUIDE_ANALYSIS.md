# Guide d'Utilisation du Notebook analysis.ipynb

## 🎯 Objectif
Ce notebook implémente une analyse complète des stéréotypes au cinéma en appliquant les concepts vus en cours de **Linguistique Computationnelle**, **Graph Mining** et **Data Mining**.

## 📋 Prérequis

1. **Exécuter d'abord** `notebooks/0_clean_data.ipynb` pour :
   - Télécharger le dataset Kaggle
   - Nettoyer et parser les scripts
   - Créer `data/processed/scripts_clean.pkl`

2. **Dépendances** installées via `requirements.txt`

## 🔄 Pipeline du Notebook

### Phase 1 : Data Preprocessing
- **Imports** : Charger les modules personnalisés (`parser`, `dictionaries`, `stats_analysis`)
- **Tokenisation avancée** : Morphologie & Lexique (enlever stopwords, noms propres)
- **Concept** : Niveaux Linguistiques (Maria Boritchev)

### Phase 2 : N-grams & Co-occurrences
- **Extraction** : Mots co-occurrents autour de "woman", "black", etc.
- **Fenêtre contextuelle** : 5 mots avant/après
- **Concept** : Text Analysis - Mesurer les associations sémantiques

### Phase 3 : Graph Mining
- **Réseaux** : Visualiser les "bulles" de mots associés
- **NetworkX** : Graphes de co-occurrence pondérés
- **Concept** : Graph Mining - Identifier les structures sémantiques

### Phase 4 : Évolution Temporelle
- **Line Charts** : Fréquences de stéréotypes par décennie (1960-2020)
- **Question** : L'usage de termes dégradants diminue-t-il statistiquement ?
- **Concept** : Data Visualization - Tendances temporelles

### Phase 5 : Comparaison de Distributions
- **Bar Charts** : Usage verbes/adjectifs Femmes vs Hommes
- **Ratio** : Quantifier les biais genrés
- **Concept** : Feature Extraction - Champs lexicaux différenciés

### Phase 6 : Heatmap de Corrélations
- **Matrice** : Corrélations entre différents stéréotypes
- **Insight** : Identifier les "clusters" de biais
- **Concept** : Data Mining - Patterns multivariés

### Phase 7 : Word Embeddings (optionnel)
- **Word2Vec** : Entraînement diachronique (un modèle par décennie)
- **Évolution sémantique** : "Woman" associé à différents mots selon l'époque
- **Concept** : Sémantique distributionnelle (Maria Boritchev)

## 📊 Visualisations Générées

Tous les graphiques sont sauvegardés dans `results/figures/` :

1. **`evolution_temporelle_complete.png`** : 4 sous-graphiques
   - Ratio Femmes/Hommes
   - Stéréotypes négatifs sur les femmes
   - Représentation ethnique
   - Stéréotypes raciaux

2. **Réseaux de co-occurrence** (2 graphiques) :
   - 1960-1970 : Contexte de "woman"
   - 2000-2010 : Contexte de "woman"
   - → Observer le déplacement des "bulles"

3. **`comparison_verbes_genre.png`** :
   - Bar chart comparatif
   - Ratio par catégorie de verbes

4. **`heatmap_correlations.png`** :
   - Matrice de corrélation
   - Identifier les biais corrélés

## 🔬 Méthodologie Scientifique

### Concepts Appliqués

| Phase | Concept du Cours | Application |
|-------|------------------|-------------|
| 1 | **Morphologie** | Tokenisation, lemmatisation |
| 2 | **N-grams** | Co-occurrences avec fenêtre |
| 3 | **Graph Mining** | Réseaux de mots, centralité |
| 4 | **Data Viz** | Line charts temporels |
| 5 | **Feature Extraction** | Champs lexicaux par groupe |
| 6 | **Data Mining** | Corrélations multivariées |
| 7 | **Sémantique** | Word embeddings diachroniques |

### Lien avec l'Espace Public

- **Civil Rights Movement** (1960s) : Impact sur la représentation des minorités ?
- **Mouvement Féministe** (1970s-80s) : Évolution des stéréotypes genrés ?
- **#MeToo** (2017-) : Réduction de l'objectification ?

→ Le cinéma (média de masse) reflète-t-il ou influence-t-il ces luttes sociales ?

## 🎓 Questions Pédagogiques

### Pour approfondir votre analyse :

1. **Niveaux Linguistiques** : Pourquoi enlever les noms propres ? Quel impact sur l'analyse ?

2. **N-grams** : Pourquoi une fenêtre de 5 mots ? Tester avec 3 ou 10.

3. **Graph Mining** : Que signifie une forte centralité pour un mot ?

4. **Sémantique** : Comment Word2Vec capture-t-il le sens des mots ?

5. **Validation** : Comment vérifier que vos dictionnaires sont exhaustifs ?

## 🚀 Extensions Possibles

### Pour aller plus loin :

1. **Topic Modeling (LDA)** :
   ```python
   from gensim.models import LdaModel
   # Identifier automatiquement les thèmes par décennie
   ```

2. **Analyse de Sentiments** :
   ```python
   from transformers import pipeline
   sentiment = pipeline('sentiment-analysis')
   # Polarité des dialogues par groupe
   ```

3. **Graphes d'Interaction** :
   - Parser les dialogues pour extraire les personnages
   - Construire un réseau social par film
   - Mesurer la centralité par genre/ethnicité

4. **Intersectionnalité** :
   - Croiser genre × ethnicité
   - Analyser spécifiquement les femmes noires, asiatiques, etc.

5. **Machine Learning** :
   - Classifier automatiquement les stéréotypes
   - Prédire le niveau de biais d'un script

## 📚 Références Académiques

### Linguistique Computationnelle
- Jurafsky & Martin, *Speech and Language Processing*, 3rd ed.
- Maria Boritchev, cours 5-HSS_0EL44 (Télécom Paris)

### Biais dans les Médias
- **Geena Davis Institute** : Gender representation in media
- **USC Annenberg** : Inequality in Film Reports

### Graph Mining
- Newman, *Networks: An Introduction*, 2nd ed.
- Cours 2-Graph_Mining (Télécom Paris)

### NLP et Biais
- Bolukbasi et al. (2016), "Man is to Computer Programmer as Woman is to Homemaker?"
- Caliskan et al. (2017), "Semantics derived automatically from language corpora"

## 🆘 Troubleshooting

### Erreur : "Fichier scripts_clean.pkl introuvable"
→ Exécutez d'abord `notebooks/0_clean_data.ipynb`

### Erreur : "Module 'src' not found"
→ Vérifiez que vous êtes dans le bon répertoire : `NLP-scripts/src/`

### Graphes vides ou peu de données
→ Augmentez la taille de l'échantillon dans `0_clean_data.ipynb`

### Word2Vec : "Word not in vocabulary"
→ Le mot n'apparaît pas assez souvent. Réduire `min_count` dans Word2Vec.

---

**Bon courage pour votre projet !** 🎓

N'hésitez pas à adapter ce notebook à vos hypothèses spécifiques et à explorer d'autres pistes d'analyse.
