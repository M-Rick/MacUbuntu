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

def get_localized_text():
    """Returns texts according to system language"""
    
    # Translations
    translations = {
        'en': {  # English (default)
            'label': 'Duplicate',
            'tip': 'Duplicate selected files',
            'copy_suffix': ' copy'
        },
        'de': {  # German
            'label': 'Duplizieren',
            'tip': 'Ausgewählte Dateien duplizieren',
            'copy_suffix': ' - Kopie'
        },
        'nl': {  # Dutch
            'label': 'Dupliceren',
            'tip': 'Geselecteerde bestanden dupliceren',
            'copy_suffix': ' - kopie'
        },
        'sv': {  # Swedish
            'label': 'Duplicera',
            'tip': 'Duplicera valda filer',
            'copy_suffix': ' - kopia'
        },
        'da': {  # Danish
            'label': 'Duplikér',
            'tip': 'Duplikér valgte filer',
            'copy_suffix': ' - kopi'
        },
        'no': {  # Norwegian
            'label': 'Dupliser',
            'tip': 'Dupliser valgte filer',
            'copy_suffix': ' - kopi'
        },
        'fi': {  # Finnish
            'label': 'Monista',
            'tip': 'Monista valitut tiedostot',
            'copy_suffix': ' - kopio'
        },
        'fr': {  # French
            'label': 'Dupliquer',
            'tip': 'Dupliquer les fichiers sélectionnés',
            'copy_suffix': ' - copie'
        },
        'it': {  # Italian
            'label': 'Duplica',
            'tip': 'Duplica i file selezionati',
            'copy_suffix': ' - copia'
        },
        'es': {  # Spanish
            'label': 'Duplicar',
            'tip': 'Duplicar archivos seleccionados',
            'copy_suffix': ' - copia'
        },
        'pt': {  # Portuguese
            'label': 'Duplicar',
            'tip': 'Duplicar arquivos selecionados',
            'copy_suffix': ' - cópia'
        },
        'ro': {  # Romanian
            'label': 'Duplicare',
            'tip': 'Duplică fișierele selectate',
            'copy_suffix': ' - copie'
        },
        'pl': {  # Polish
            'label': 'Duplikuj',
            'tip': 'Duplikuj wybrane pliki',
            'copy_suffix': ' - kopia'
        },
        'hu': {  # Hungarian
            'label': 'Duplikálás',
            'tip': 'Kiválasztott fájlok duplikálása',
            'copy_suffix': ' - másolat'
        },
        'ru': {  # Russian
            'label': 'Дублировать',
            'tip': 'Дублировать выбранные файлы',
            'copy_suffix': ' - копия'
        },
        'zh_CN': {  # Simplified Chinese
            'label': '复制',
            'tip': '复制所选文件',
            'copy_suffix': ' 的副本'
        },
        'zh_TW': {  # Traditional Chinese
            'label': '複製',
            'tip': '複製所選檔案',
            'copy_suffix': ' 的副本'
        },
        'ja': {  # Japanese
            'label': '複製',
            'tip': '選択されたファイルを複製',
            'copy_suffix': ' のコピー'
        },
        'ko': {  # Korean
            'label': '복제',
            'tip': '선택한 파일 복제',
            'copy_suffix': ' 사본'
        },
        'hi': {  # Hindi
            'label': 'प्रतिलिपि',
            'tip': 'चयनित फाइलों की प्रतिलिपि बनाएं',
            'copy_suffix': ' की प्रति'
        },
        'ar': {  # Arabic
            'label': 'تكرار',
            'tip': 'تكرار الملفات المحددة',
            'copy_suffix': ' - نسخة'
        },
        'he': {  # Hebrew
            'label': 'שכפול',
            'tip': 'שכפול הקבצים הנבחרים',
            'copy_suffix': ' - עותק'
        },
        'tr': {  # Turkish
            'label': 'Çoğalt',
            'tip': 'Seçili dosyaları çoğalt',
            'copy_suffix': ' - kopya'
        }
    }
    
    try:
        # Get system language variables
        lang_env = os.environ.get('LANG', '').lower()
        lc_messages = os.environ.get('LC_MESSAGES', '').lower()
        
        try:
            system_locale = locale.getdefaultlocale()[0]
            if system_locale:
                system_locale = system_locale.lower()
        except:
            system_locale = ''
        
        # Function to detect language
        def detect_language():
            # List of sources to check (by priority order)
            sources = [lc_messages, lang_env, system_locale]
            
            for source in sources:
                if not source:
                    continue
                    
                # Exact check for Chinese variants
                if 'zh_cn' in source or 'zh-cn' in source:
                    return 'zh_CN'
                elif 'zh_tw' in source or 'zh-tw' in source or 'zh_hk' in source:
                    return 'zh_TW'
                    
                # Check other languages (2-letter code)
                for lang_code in translations.keys():
                    if lang_code.startswith('zh'):  # Already handled above
                        continue
                    if source.startswith(lang_code + '_') or source.startswith(lang_code + '-'):
                        return lang_code
            
            # Default language if nothing found
            return 'en'
        
        detected_lang = detect_language()
        return translations.get(detected_lang, translations['en'])
        
    except Exception:
        # In case of error, use English
        return translations['en']

# Get localized texts
TEXTS = get_localized_text()


class DuplicateExtension(GObject.GObject, Nautilus.MenuProvider):
    
    def __init__(self):
        super().__init__()
    
    def get_file_items(self, files):
        """Add 'Duplicate' option to context menu"""
        # Nautilus 4.x API - files is passed directly
        
        # Display nothing if no files selected
        if not files:
            return []
        
        # Create menu entry (automatically localized)
        item = Nautilus.MenuItem(
            name='DuplicateExtension::duplicate',
            label=TEXTS['label'],
            tip=TEXTS['tip']
        )
        
        # Connect action
        item.connect('activate', self.duplicate_files, files)
        
        return [item]
    
    def duplicate_files(self, menu, files):
        """Duplicate selected files"""
        for file_info in files:
            try:
                # Get file path
                uri = file_info.get_uri()
                file_path = unquote(uri.replace('file://', ''))
                
                # Duplicate file
                self.duplicate_single_file(file_path)
                
            except Exception as e:
                # In case of error, continue with other files
                print(f"Error during duplication: {e}")
    
    def duplicate_single_file(self, original_path):
        """Duplicate a single file or folder"""
        path = Path(original_path)
        parent_dir = path.parent
        name = path.stem
        suffix = path.suffix
        
        # Build copy name (localized)
        copy_suffix = TEXTS['copy_suffix']
        if suffix:
            copy_name = f"{name}{copy_suffix}{suffix}"
        else:
            copy_name = f"{name}{copy_suffix}"
        
        copy_path = parent_dir / copy_name
        
        # Handle name conflicts
        counter = 2
        while copy_path.exists():
            if suffix:
                copy_name = f"{name}{copy_suffix} {counter}{suffix}"
            else:
                copy_name = f"{name}{copy_suffix} {counter}"
            copy_path = parent_dir / copy_name
            counter += 1
        
        # Perform copy
        if path.is_file():
            shutil.copy2(original_path, str(copy_path))
        elif path.is_dir():
            shutil.copytree(original_path, str(copy_path))


# Entry point for Nautilus
def main():
    pass

if __name__ == "__main__":
    main()
