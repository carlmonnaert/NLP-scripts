"""
parser.py - Nettoyage et parsing des scripts de films
Extrait les dialogues, nettoie les noms de personnages, prépare le texte pour l'analyse
"""

import re
import os
from typing import Dict, List, Optional
import pandas as pd


def extract_character_name(line: str) -> Optional[str]:
    """
    Extrait le nom du personnage d'une ligne de script.
    Format typique: "PERSONNAGE: dialogue" ou "PERSONNAGE dialogue"
    
    Args:
        line: Ligne de script
        
    Returns:
        Nom du personnage ou None si non trouvé
    """
    # Pattern pour détecter un nom de personnage (tout en majuscules suivi de : ou espace)
    pattern = r'^([A-Z\s]{2,30})(?:\:|$)'
    match = re.match(pattern, line.strip())
    
    if match:
        return match.group(1).strip()
    return None


def clean_script_text(text: str, remove_stage_directions: bool = True) -> str:
    """
    Nettoie le texte d'un script.
    
    Args:
        text: Texte brut du script
        remove_stage_directions: Si True, supprime les indications scéniques (entre parenthèses)
        
    Returns:
        Texte nettoyé
    """
    if not isinstance(text, str):
        return ""
    
    # Supprimer les indications scéniques (ex: (Il sort), [pause], etc.)
    if remove_stage_directions:
        text = re.sub(r'\([^)]*\)', '', text)
        text = re.sub(r'\[[^\]]*\]', '', text)
    
    # Supprimer les numéros de scène
    text = re.sub(r'(SCENE|SÉQUENCE)\s+\d+', '', text, flags=re.IGNORECASE)
    
    # Supprimer les lignes vides multiples
    text = re.sub(r'\n\s*\n', '\n\n', text)
    
    # Supprimer les espaces en début/fin
    text = text.strip()
    
    return text


def extract_dialogues(script_text: str) -> List[Dict[str, str]]:
    """
    Extrait les dialogues d'un script avec les noms des personnages.
    
    Args:
        script_text: Texte complet du script
        
    Returns:
        Liste de dictionnaires {'character': nom, 'dialogue': texte}
    """
    dialogues = []
    lines = script_text.split('\n')
    
    current_character = None
    current_dialogue = []
    
    for line in lines:
        line = line.strip()
        if not line:
            # Ligne vide: sauvegarder le dialogue en cours si existant
            if current_character and current_dialogue:
                dialogues.append({
                    'character': current_character,
                    'dialogue': ' '.join(current_dialogue)
                })
                current_character = None
                current_dialogue = []
            continue
        
        # Vérifier si c'est un nom de personnage
        character_name = extract_character_name(line)
        
        if character_name:
            # Nouveau personnage: sauvegarder le dialogue précédent
            if current_character and current_dialogue:
                dialogues.append({
                    'character': current_character,
                    'dialogue': ' '.join(current_dialogue)
                })
            
            current_character = character_name
            current_dialogue = []
            
            # Si le dialogue commence sur la même ligne (après le :)
            if ':' in line:
                dialogue_part = line.split(':', 1)[1].strip()
                if dialogue_part:
                    current_dialogue.append(dialogue_part)
        else:
            # C'est une ligne de dialogue (continuation)
            if current_character:
                current_dialogue.append(line)
    
    # Sauvegarder le dernier dialogue
    if current_character and current_dialogue:
        dialogues.append({
            'character': current_character,
            'dialogue': ' '.join(current_dialogue)
        })
    
    return dialogues


def parse_script_file(filepath: str) -> Dict:
    """
    Parse un fichier de script complet.
    
    Args:
        filepath: Chemin vers le fichier .txt
        
    Returns:
        Dictionnaire avec le texte nettoyé et les dialogues extraits
    """
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        raw_text = f.read()
    
    clean_text = clean_script_text(raw_text)
    dialogues = extract_dialogues(clean_text)
    
    return {
        'filepath': filepath,
        'filename': os.path.basename(filepath),
        'raw_text': raw_text,
        'clean_text': clean_text,
        'dialogues': dialogues,
        'num_dialogues': len(dialogues),
        'characters': list(set(d['character'] for d in dialogues))
    }


def load_scripts_from_directory(directory: str, limit: Optional[int] = None) -> pd.DataFrame:
    """
    Charge et parse tous les scripts d'un répertoire.
    
    Args:
        directory: Chemin vers le dossier contenant les scripts .txt
        limit: Nombre maximum de fichiers à charger (None pour tous)
        
    Returns:
        DataFrame avec les scripts parsés
    """
    import glob
    
    script_files = glob.glob(os.path.join(directory, "*.txt"))
    
    if limit:
        script_files = script_files[:limit]
    
    print(f"Chargement de {len(script_files)} scripts...")
    
    parsed_scripts = []
    for i, filepath in enumerate(script_files):
        if i % 100 == 0:
            print(f"  Progression: {i}/{len(script_files)}")
        
        try:
            parsed = parse_script_file(filepath)
            parsed_scripts.append(parsed)
        except Exception as e:
            print(f"  Erreur sur {filepath}: {e}")
    
    return pd.DataFrame(parsed_scripts)


if __name__ == "__main__":
    # Test du parser
    test_script = """
    JOHN: Hello, how are you?
    
    MARY: I'm fine, thank you! (smiles)
    And you?
    
    JOHN: Great! Let's go.
    """
    
    dialogues = extract_dialogues(test_script)
    print("Test des dialogues extraits:")
    for d in dialogues:
        print(f"  {d['character']}: {d['dialogue']}")
