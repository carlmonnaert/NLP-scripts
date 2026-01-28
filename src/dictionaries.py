"""
dictionaries.py - Dictionnaires de mots pour l'analyse des biais
Contient les listes de mots-clés pour détecter le sexisme, racisme, homophobie
"""

# ===== DICTIONNAIRE GENRE / SEXISME =====

GENDER_WORDS = {
    'female': [
        'woman', 'women', 'girl', 'girls', 'lady', 'ladies', 
        'female', 'she', 'her', 'herself', 'wife', 'mother',
        'daughter', 'sister', 'girlfriend', 'bride', 'widow'
    ],
    'male': [
        'man', 'men', 'boy', 'boys', 'gentleman', 'gentlemen',
        'male', 'he', 'him', 'himself', 'husband', 'father',
        'son', 'brother', 'boyfriend', 'groom', 'widower'
    ]
}

# Stéréotypes sexistes (à analyser dans le contexte)
GENDER_STEREOTYPES = {
    'female_negative': [
        'emotional', 'hysterical', 'weak', 'fragile', 'submissive',
        'passive', 'dependent', 'irrational', 'dramatic', 'sensitive',
        'nag', 'gossip', 'vain', 'superficial'
    ],
    'female_objectification': [
        'beautiful', 'pretty', 'sexy', 'attractive', 'hot', 'gorgeous',
        'cute', 'stunning', 'lovely', 'babe', 'doll', 'honey', 'sweetie'
    ],
    'male_stereotypes': [
        'strong', 'powerful', 'tough', 'brave', 'aggressive', 'dominant',
        'rational', 'logical', 'independent', 'leader', 'protector'
    ]
}

# Termes liés aux rôles genrés traditionnels
GENDERED_ROLES = {
    'domestic_female': [
        'housewife', 'homemaker', 'mother', 'cook', 'clean', 'nurture',
        'care', 'raise', 'babysit', 'sew', 'knit'
    ],
    'professional_male': [
        'boss', 'ceo', 'president', 'manager', 'director', 'leader',
        'entrepreneur', 'executive', 'commander', 'chief'
    ]
}


# ===== DICTIONNAIRE RACE / ETHNICITÉ =====

ETHNICITY_WORDS = {
    'african_american': [
        'black', 'african', 'negro', 'colored', 'afro-american'
    ],
    'asian': [
        'asian', 'chinese', 'japanese', 'korean', 'vietnamese',
        'thai', 'indian', 'pakistani', 'filipino'
    ],
    'hispanic': [
        'hispanic', 'latino', 'latina', 'mexican', 'spanish',
        'puerto rican', 'cuban', 'latin'
    ],
    'white': [
        'white', 'caucasian', 'european', 'anglo'
    ],
    'native': [
        'native', 'indian', 'indigenous', 'aboriginal'
    ],
    'middle_eastern': [
        'arab', 'arabian', 'persian', 'middle eastern', 'turkish'
    ]
}

# Stéréotypes raciaux (à analyser avec précaution)
RACIAL_STEREOTYPES = {
    'criminal': [
        'thug', 'gangster', 'criminal', 'dangerous', 'violent',
        'aggressive', 'savage', 'primitive', 'uncivilized'
    ],
    'exotic': [
        'exotic', 'mysterious', 'oriental', 'foreign', 'alien'
    ],
    'poverty': [
        'poor', 'ghetto', 'slum', 'welfare', 'uneducated', 'ignorant'
    ]
}


# ===== DICTIONNAIRE ORIENTATION SEXUELLE / HOMOPHOBIE =====

LGBTQ_WORDS = {
    'orientation': [
        'gay', 'lesbian', 'homosexual', 'bisexual', 'queer',
        'lgbtq', 'lgbt', 'same-sex', 'transgender', 'trans'
    ],
    'slurs': [
        # Note: Ces termes sont inclus pour détecter l'homophobie, pas pour l'encourager
        'faggot', 'fag', 'dyke', 'queer', 'homo', 'tranny'
    ]
}

HOMOPHOBIC_CONTEXT = [
    'unnatural', 'abnormal', 'sick', 'wrong', 'sinful', 'perverted',
    'deviant', 'disgusting', 'immoral', 'shameful'
]


# ===== VERBES D'ACTION PAR CONTEXTE =====

ACTION_VERBS = {
    'violence': [
        'kill', 'murder', 'fight', 'hit', 'punch', 'shoot', 'stab',
        'attack', 'assault', 'beat', 'destroy', 'rape', 'abuse'
    ],
    'power': [
        'control', 'dominate', 'command', 'order', 'rule', 'lead',
        'direct', 'manage', 'supervise', 'govern'
    ],
    'submission': [
        'obey', 'submit', 'follow', 'serve', 'comply', 'surrender',
        'yield', 'defer', 'bow'
    ],
    'emotion': [
        'cry', 'weep', 'sob', 'whine', 'complain', 'worry', 'fear',
        'panic', 'scream', 'hysterical'
    ]
}


# ===== ADJECTIFS PAR VALENCE =====

ADJECTIVES = {
    'positive': [
        'good', 'great', 'excellent', 'wonderful', 'amazing', 'brilliant',
        'intelligent', 'smart', 'capable', 'competent', 'strong', 'brave'
    ],
    'negative': [
        'bad', 'terrible', 'awful', 'horrible', 'stupid', 'dumb', 'foolish',
        'weak', 'incompetent', 'useless', 'pathetic', 'worthless'
    ],
    'appearance_positive': [
        'beautiful', 'handsome', 'attractive', 'pretty', 'gorgeous', 'stunning'
    ],
    'appearance_negative': [
        'ugly', 'hideous', 'unattractive', 'repulsive', 'grotesque'
    ]
}


def get_all_bias_words() -> set:
    """
    Retourne l'ensemble de tous les mots liés aux biais.
    Utile pour filtrer les scripts.
    """
    all_words = set()
    
    # Parcourir tous les dictionnaires
    for category_dict in [GENDER_WORDS, GENDER_STEREOTYPES, GENDERED_ROLES,
                          ETHNICITY_WORDS, RACIAL_STEREOTYPES, LGBTQ_WORDS,
                          ACTION_VERBS, ADJECTIVES]:
        for word_list in category_dict.values():
            all_words.update(word_list)
    
    # Ajouter les mots isolés
    all_words.update(HOMOPHOBIC_CONTEXT)
    
    return all_words


def get_category_words(category: str) -> list:
    """
    Retourne les mots d'une catégorie spécifique.
    
    Args:
        category: 'gender', 'race', 'lgbtq', 'violence', etc.
        
    Returns:
        Liste des mots de cette catégorie
    """
    category_map = {
        'gender': [GENDER_WORDS, GENDER_STEREOTYPES, GENDERED_ROLES],
        'race': [ETHNICITY_WORDS, RACIAL_STEREOTYPES],
        'lgbtq': [LGBTQ_WORDS],
        'violence': [ACTION_VERBS['violence']],
        'power': [ACTION_VERBS['power']]
    }
    
    words = []
    if category in category_map:
        for dict_or_list in category_map[category]:
            if isinstance(dict_or_list, dict):
                for word_list in dict_or_list.values():
                    words.extend(word_list)
            else:
                words.extend(dict_or_list)
    
    return list(set(words))


if __name__ == "__main__":
    # Test des dictionnaires
    print(f"Nombre total de mots dans les dictionnaires: {len(get_all_bias_words())}")
    print(f"\nMots liés au genre: {len(get_category_words('gender'))}")
    print(f"Mots liés à la race: {len(get_category_words('race'))}")
    print(f"Mots liés à LGBTQ: {len(get_category_words('lgbtq'))}")
