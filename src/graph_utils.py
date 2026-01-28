# Ajout de fonctionnalités avancées pour Graph Mining

import networkx as nx
from collections import defaultdict
import matplotlib.pyplot as plt

def build_bipartite_graph(df, entity_words_dict):
    """
    Construit un graphe biparti : Films ↔ Thèmes/Stéréotypes
    Permet d'identifier les clusters de films avec des patterns similaires
    
    Args:
        df: DataFrame avec les scripts
        entity_words_dict: Dict {nom_entité: liste_de_mots}
    
    Returns:
        Graphe biparti NetworkX
    """
    G = nx.Graph()
    
    for idx, row in df.iterrows():
        film_node = f"Film_{row['title'][:20]}_{row['release_year']:.0f}"
        G.add_node(film_node, bipartite=0, decade=row['decade'])
        
        # Calculer la présence de chaque entité
        for entity_name, words in entity_words_dict.items():
            freq = calculate_relative_frequency(row['clean_text'], words)
            if freq > 1.0:  # Seuil de présence significative
                entity_node = f"Theme_{entity_name}"
                G.add_node(entity_node, bipartite=1)
                G.add_edge(film_node, entity_node, weight=freq)
    
    return G


def detect_communities(G):
    """
    Détecte les communautés dans le graphe de co-occurrence.
    Application : Identifier les clusters de mots qui forment des "bulles" sémantiques
    """
    from networkx.algorithms import community
    
    # Louvain community detection
    communities = community.louvain_communities(G)
    
    return communities


def centrality_analysis(G):
    """
    Analyse de centralité : quels mots sont les plus "importants" dans le réseau ?
    """
    degree_cent = nx.degree_centrality(G)
    betweenness_cent = nx.betweenness_centrality(G)
    closeness_cent = nx.closeness_centrality(G)
    
    return {
        'degree': degree_cent,
        'betweenness': betweenness_cent,
        'closeness': closeness_cent
    }


# Utilisation de ces fonctions dans le notebook analysis.ipynb
