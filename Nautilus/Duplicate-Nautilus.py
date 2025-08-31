#!/usr/bin/env python3
"""
A Nautilus Extension to duplicate files
Place in: ~/.local/share/nautilus-python/extensions/duplicate_files.py
"""

import os
import shutil
import locale
from gi.repository import Nautilus, GObject
from urllib.parse import unquote
from pathlib import Path

# Détection automatique de la langue multilingue
def get_localized_text():
    """Retourne les textes selon la langue du système"""
    
    # Dictionnaire de toutes les traductions
    translations = {
        'en': {  # Anglais (défaut)
            'label': 'Duplicate',
            'tip': 'Duplicate selected files',
            'copy_suffix': ' copy'
        },
        'fr': {  # Français
            'label': 'Dupliquer',
            'tip': 'Dupliquer les fichiers sélectionnés',
            'copy_suffix': ' - copie'
        },
        'de': {  # Allemand
            'label': 'Duplizieren',
            'tip': 'Ausgewählte Dateien duplizieren',
            'copy_suffix': ' - Kopie'
        },
        'nl': {  # Hollandais
            'label': 'Dupliceren',
            'tip': 'Geselecteerde bestanden dupliceren',
            'copy_suffix': ' - kopie'
        },
        'it': {  # Italien
            'label': 'Duplica',
            'tip': 'Duplica i file selezionati',
            'copy_suffix': ' - copia'
        },
        'es': {  # Espagnol
            'label': 'Duplicar',
            'tip': 'Duplicar archivos seleccionados',
            'copy_suffix': ' - copia'
        },
        'ja': {  # Japonais
            'label': '複製',
            'tip': '選択されたファイルを複製',
            'copy_suffix': ' のコピー'
        },
        'zh_CN': {  # Chinois simplifié
            'label': '复制',
            'tip': '复制所选文件',
            'copy_suffix': ' 的副本'
        },
        'zh_TW': {  # Chinois traditionnel
            'label': '複製',
            'tip': '複製所選檔案',
            'copy_suffix': ' 的副本'
        },
        'ru': {  # Russe
            'label': 'Дублировать',
            'tip': 'Дублировать выбранные файлы',
            'copy_suffix': ' - копия'
        }
    }
    
    try:
        # Récupérer les variables de langue du système
        lang_env = os.environ.get('LANG', '').lower()
        lc_messages = os.environ.get('LC_MESSAGES', '').lower()
        
        try:
            system_locale = locale.getdefaultlocale()[0]
            if system_locale:
                system_locale = system_locale.lower()
        except:
            system_locale = ''
        
        # Fonction pour détecter la langue
        def detect_language():
            # Liste des sources à vérifier (par ordre de priorité)
            sources = [lc_messages, lang_env, system_locale]
            
            for source in sources:
                if not source:
                    continue
                    
                # Vérification exacte pour les variantes chinoises
                if 'zh_cn' in source or 'zh-cn' in source:
                    return 'zh_CN'
                elif 'zh_tw' in source or 'zh-tw' in source or 'zh_hk' in source:
                    return 'zh_TW'
                    
                # Vérification des autres langues (code à 2 lettres)
                for lang_code in translations.keys():
                    if lang_code.startswith('zh'):  # Déjà traité ci-dessus
                        continue
                    if source.startswith(lang_code + '_') or source.startswith(lang_code + '-'):
                        return lang_code
            
            # Langue par défaut si rien trouvé
            return 'en'
        
        detected_lang = detect_language()
        return translations.get(detected_lang, translations['en'])
        
    except Exception:
        # En cas d'erreur, utiliser l'anglais
        return translations['en']

# Récupérer les textes localisés
TEXTS = get_localized_text()


class DuplicateExtension(GObject.GObject, Nautilus.MenuProvider):
    
    def __init__(self):
        super().__init__()
    
    def get_file_items(self, files):
        """Ajoute l'option 'Dupliquer' au menu contextuel"""
        # API Nautilus 4.x - files est directement passé
        
        # Ne rien afficher si aucun fichier sélectionné
        if not files:
            return []
        
        # Créer l'entrée de menu (localisée automatiquement)
        item = Nautilus.MenuItem(
            name='DuplicateExtension::duplicate',
            label=TEXTS['label'],
            tip=TEXTS['tip']
        )
        
        # Connecter l'action
        item.connect('activate', self.duplicate_files, files)
        
        return [item]
    
    def duplicate_files(self, menu, files):
        """Duplique les fichiers sélectionnés"""
        for file_info in files:
            try:
                # Récupérer le chemin du fichier
                uri = file_info.get_uri()
                file_path = unquote(uri.replace('file://', ''))
                
                # Dupliquer le fichier
                self.duplicate_single_file(file_path)
                
            except Exception as e:
                # En cas d'erreur, continuer avec les autres fichiers
                print(f"Erreur lors de la duplication : {e}")
    
    def duplicate_single_file(self, original_path):
        """Duplique un seul fichier ou dossier"""
        path = Path(original_path)
        parent_dir = path.parent
        name = path.stem
        suffix = path.suffix
        
        # Construire le nom de la copie (localisé)
        copy_suffix = TEXTS['copy_suffix']
        if suffix:
            copy_name = f"{name}{copy_suffix}{suffix}"
        else:
            copy_name = f"{name}{copy_suffix}"
        
        copy_path = parent_dir / copy_name
        
        # Gérer les conflits de noms
        counter = 2
        while copy_path.exists():
            if suffix:
                copy_name = f"{name}{copy_suffix} {counter}{suffix}"
            else:
                copy_name = f"{name}{copy_suffix} {counter}"
            copy_path = parent_dir / copy_name
            counter += 1
        
        # Effectuer la copie
        if path.is_file():
            shutil.copy2(original_path, str(copy_path))
        elif path.is_dir():
            shutil.copytree(original_path, str(copy_path))


# Point d'entrée pour Nautilus
def main():
    pass

if __name__ == "__main__":
    main()
