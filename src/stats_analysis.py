"""
stats_analysis.py - Calcul des statistiques et fréquences relatives
Analyse l'évolution des biais par décennie
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from collections import Counter
import re


def calculate_word_frequency(text: str, word_list: List[str]) -> Dict[str, int]:
    """
    Calcule la fréquence d'apparition de chaque mot d'une liste dans un texte.
    
    Args:
        text: Texte à analyser
        word_list: Liste de mots à chercher
        
    Returns:
        Dictionnaire {mot: fréquence}
    """
    if not isinstance(text, str):
        return {word: 0 for word in word_list}
    
    text_lower = text.lower()
    frequencies = {}
    
    for word in word_list:
        # Utiliser \b pour les limites de mots (éviter les faux positifs)
        pattern = r'\b' + re.escape(word.lower()) + r'\b'
        count = len(re.findall(pattern, text_lower))
        frequencies[word] = count
    
    return frequencies


def calculate_relative_frequency(text: str, word_list: List[str]) -> float:
    """
    Calcule la fréquence relative (pour 1000 mots) d'une liste de mots.
    
    Args:
        text: Texte à analyser
        word_list: Liste de mots à chercher
        
    Returns:
        Fréquence relative (occurrences pour 1000 mots)
    """
    if not isinstance(text, str) or not text.strip():
        return 0.0
    
    # Compter le nombre total de mots
    total_words = len(text.split())
    
    if total_words == 0:
        return 0.0
    
    # Compter les occurrences des mots cibles
    frequencies = calculate_word_frequency(text, word_list)
    total_occurrences = sum(frequencies.values())
    
    # Fréquence relative pour 1000 mots
    relative_freq = (total_occurrences / total_words) * 1000
    
    return relative_freq


def analyze_corpus_by_decade(df: pd.DataFrame, 
                              text_column: str,
                              year_column: str,
                              word_categories: Dict[str, List[str]]) -> pd.DataFrame:
    """
    Analyse un corpus de textes par décennie pour différentes catégories de mots.
    
    Args:
        df: DataFrame contenant les textes
        text_column: Nom de la colonne contenant le texte
        year_column: Nom de la colonne contenant l'année
        word_categories: Dict {nom_catégorie: liste_de_mots}
        
    Returns:
        DataFrame avec les fréquences relatives par décennie et catégorie
    """
    # Créer une colonne décennie si elle n'existe pas
    if 'decade' not in df.columns:
        df['decade'] = (df[year_column] // 10) * 10
    
    results = []
    
    for decade in sorted(df['decade'].unique()):
        decade_data = df[df['decade'] == decade]
        
        # Concaténer tous les textes de la décennie
        all_text = ' '.join(decade_data[text_column].dropna().astype(str))
        
        decade_result = {
            'decade': decade,
            'num_scripts': len(decade_data),
            'total_words': len(all_text.split())
        }
        
        # Calculer la fréquence pour chaque catégorie
        for category_name, word_list in word_categories.items():
            freq = calculate_relative_frequency(all_text, word_list)
            decade_result[f'{category_name}_freq'] = freq
            
            # Aussi compter les occurrences brutes
            frequencies = calculate_word_frequency(all_text, word_list)
            decade_result[f'{category_name}_count'] = sum(frequencies.values())
        
        results.append(decade_result)
    
    return pd.DataFrame(results)


def analyze_gender_bias_by_decade(df: pd.DataFrame,
                                   text_column: str,
                                   year_column: str) -> pd.DataFrame:
    """
    Analyse spécifique du biais de genre par décennie.
    
    Args:
        df: DataFrame contenant les textes
        text_column: Nom de la colonne contenant le texte
        year_column: Nom de la colonne contenant l'année
        
    Returns:
        DataFrame avec les métriques de biais de genre
    """
    from dictionaries import GENDER_WORDS, GENDER_STEREOTYPES
    
    if 'decade' not in df.columns:
        df['decade'] = (df[year_column] // 10) * 10
    
    results = []
    
    for decade in sorted(df['decade'].unique()):
        decade_data = df[df['decade'] == decade]
        all_text = ' '.join(decade_data[text_column].dropna().astype(str))
        
        # Fréquences des mentions de genre
        female_freq = calculate_relative_frequency(all_text, GENDER_WORDS['female'])
        male_freq = calculate_relative_frequency(all_text, GENDER_WORDS['male'])
        
        # Ratio femmes/hommes
        gender_ratio = female_freq / male_freq if male_freq > 0 else 0
        
        # Stéréotypes
        female_neg_freq = calculate_relative_frequency(all_text, GENDER_STEREOTYPES['female_negative'])
        female_obj_freq = calculate_relative_frequency(all_text, GENDER_STEREOTYPES['female_objectification'])
        male_stereo_freq = calculate_relative_frequency(all_text, GENDER_STEREOTYPES['male_stereotypes'])
        
        results.append({
            'decade': decade,
            'num_scripts': len(decade_data),
            'female_mentions_freq': female_freq,
            'male_mentions_freq': male_freq,
            'gender_ratio': gender_ratio,
            'female_negative_stereotypes': female_neg_freq,
            'female_objectification': female_obj_freq,
            'male_stereotypes': male_stereo_freq
        })
    
    return pd.DataFrame(results)


def analyze_racial_bias_by_decade(df: pd.DataFrame,
                                   text_column: str,
                                   year_column: str) -> pd.DataFrame:
    """
    Analyse spécifique du biais racial/ethnique par décennie.
    
    Args:
        df: DataFrame contenant les textes
        text_column: Nom de la colonne contenant le texte
        year_column: Nom de la colonne contenant l'année
        
    Returns:
        DataFrame avec les métriques de biais racial
    """
    from dictionaries import ETHNICITY_WORDS, RACIAL_STEREOTYPES
    
    if 'decade' not in df.columns:
        df['decade'] = (df[year_column] // 10) * 10
    
    results = []
    
    for decade in sorted(df['decade'].unique()):
        decade_data = df[df['decade'] == decade]
        all_text = ' '.join(decade_data[text_column].dropna().astype(str))
        
        decade_result = {
            'decade': decade,
            'num_scripts': len(decade_data)
        }
        
        # Fréquences par groupe ethnique
        for ethnicity, words in ETHNICITY_WORDS.items():
            freq = calculate_relative_frequency(all_text, words)
            decade_result[f'{ethnicity}_freq'] = freq
        
        # Stéréotypes raciaux
        for stereotype, words in RACIAL_STEREOTYPES.items():
            freq = calculate_relative_frequency(all_text, words)
            decade_result[f'stereotype_{stereotype}_freq'] = freq
        
        results.append(decade_result)
    
    return pd.DataFrame(results)


def compare_decades(df_stats: pd.DataFrame, metric: str) -> Dict:
    """
    Compare l'évolution d'une métrique entre les décennies.
    
    Args:
        df_stats: DataFrame avec les statistiques par décennie
        metric: Nom de la métrique à comparer
        
    Returns:
        Dictionnaire avec statistiques d'évolution
    """
    if metric not in df_stats.columns:
        return {'error': f'Metric {metric} not found'}
    
    values = df_stats[metric].values
    decades = df_stats['decade'].values
    
    # Calcul de tendance (régression linéaire simple)
    if len(values) > 1:
        slope = np.polyfit(decades, values, 1)[0]
        trend = 'increasing' if slope > 0 else 'decreasing'
    else:
        slope = 0
        trend = 'insufficient data'
    
    return {
        'metric': metric,
        'first_decade': decades[0] if len(decades) > 0 else None,
        'last_decade': decades[-1] if len(decades) > 0 else None,
        'first_value': values[0] if len(values) > 0 else None,
        'last_value': values[-1] if len(values) > 0 else None,
        'change': values[-1] - values[0] if len(values) > 1 else 0,
        'percent_change': ((values[-1] - values[0]) / values[0] * 100) if len(values) > 1 and values[0] != 0 else 0,
        'slope': slope,
        'trend': trend,
        'mean': np.mean(values),
        'std': np.std(values)
    }


if __name__ == "__main__":
    # Test des fonctions
    test_text = "The woman was beautiful and emotional. The man was strong and brave. The woman cried while the man fought."
    
    from dictionaries import GENDER_WORDS, GENDER_STEREOTYPES
    
    print("Test de fréquence relative:")
    female_freq = calculate_relative_frequency(test_text, GENDER_WORDS['female'])
    male_freq = calculate_relative_frequency(test_text, GENDER_WORDS['male'])
    
    print(f"Fréquence 'female': {female_freq:.2f} pour 1000 mots")
    print(f"Fréquence 'male': {male_freq:.2f} pour 1000 mots")
