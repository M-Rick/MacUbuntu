#!/usr/bin/env python3
"""
A Nemo Extension to manage files locking by adding an additional "Lock/Unlock" menu
Place in: ~/.local/share/nemo-python/extensions/lock_files.py
"""

import os
import stat
import locale
from gi.repository import Nemo, GObject
from urllib.parse import unquote
from pathlib import Path

def get_localized_text():
    """Returns texts according to system language"""
    
    # Translations
    translations = {
        'en': {  # English (default)
            'lock': 'Lock',
            'unlock': 'Unlock',
            'lock_tip': 'Protect file from writing',
            'unlock_tip': 'Allow file modification'
        },
        'de': {  # German
            'lock': 'Sperren',
            'unlock': 'Entsperren',
            'lock_tip': 'Datei vor Schreibzugriff schützen',
            'unlock_tip': 'Änderung der Datei erlauben'
        },
        'nl': {  # Dutch
            'lock': 'Vergrendelen',
            'unlock': 'Ontgrendelen',
            'lock_tip': 'Bestand beschermen tegen schrijven',
            'unlock_tip': 'Wijziging van bestand toestaan'
        },
        'sv': {  # Swedish
            'lock': 'Lås',
            'unlock': 'Lås upp',
            'lock_tip': 'Skydda fil från skrivning',
            'unlock_tip': 'Tillåt filmodifiering'
        },
        'da': {  # Danish
            'lock': 'Lås',
            'unlock': 'Lås op',
            'lock_tip': 'Beskyt fil mod skrivning',
            'unlock_tip': 'Tillad filændring'
        },
        'no': {  # Norwegian
            'lock': 'Lås',
            'unlock': 'Lås opp',
            'lock_tip': 'Beskytt fil mot skriving',
            'unlock_tip': 'Tillat filendring'
        },
        'fi': {  # Finnish
            'lock': 'Lukitse',
            'unlock': 'Avaa lukitus',
            'lock_tip': 'Suojaa tiedosto kirjoittamiselta',
            'unlock_tip': 'Salli tiedoston muokkaus'
        },
        'fr': {  # French
            'lock': 'Verrouiller',
            'unlock': 'Déverrouiller',
            'lock_tip': 'Protéger le fichier en écriture',
            'unlock_tip': 'Autoriser la modification du fichier'
        },
        'it': {  # Italian
            'lock': 'Blocca',
            'unlock': 'Sblocca',
            'lock_tip': 'Proteggi il file dalla scrittura',
            'unlock_tip': 'Consenti la modifica del file'
        },
        'es': {  # Spanish
            'lock': 'Bloquear',
            'unlock': 'Desbloquear',
            'lock_tip': 'Proteger archivo contra escritura',
            'unlock_tip': 'Permitir modificación del archivo'
        },
        'pt': {  # Portuguese
            'lock': 'Bloquear',
            'unlock': 'Desbloquear',
            'lock_tip': 'Proteger arquivo contra escrita',
            'unlock_tip': 'Permitir modificação do arquivo'
        },
        'ro': {  # Romanian
            'lock': 'Blocare',
            'unlock': 'Deblocare',
            'lock_tip': 'Protejează fișierul de la scriere',
            'unlock_tip': 'Permite modificarea fișierului'
        },
        'pl': {  # Polish
            'lock': 'Zablokuj',
            'unlock': 'Odblokuj',
            'lock_tip': 'Chroń plik przed zapisem',
            'unlock_tip': 'Pozwól na modyfikację pliku'
        },
        'hu': {  # Hungarian
            'lock': 'Zárolás',
            'unlock': 'Zárolás feloldása',
            'lock_tip': 'Fájl védelme írás ellen',
            'unlock_tip': 'Fájl módosításának engedélyezése'
        },
        'ru': {  # Russian
            'lock': 'Заблокировать',
            'unlock': 'Разблокировать',
            'lock_tip': 'Защитить файл от записи',
            'unlock_tip': 'Разрешить изменение файла'
        },
        'hi': {  # Hindi
            'lock': 'लॉक',
            'unlock': 'अनलॉक',
            'lock_tip': 'फाइल को लिखने से सुरक्षित करें',
            'unlock_tip': 'फाइल संशोधन की अनुमति दें'
        },
        'zh_CN': {  # Simplified Chinese
            'lock': '锁定',
            'unlock': '解锁',
            'lock_tip': '保护文件免受写入',
            'unlock_tip': '允许修改文件'
        },
        'zh_TW': {  # Traditional Chinese
            'lock': '鎖定',
            'unlock': '解鎖',
            'lock_tip': '保護檔案免受寫入',
            'unlock_tip': '允許修改檔案'
        },
        'ja': {  # Japanese
            'lock': 'ロック',
            'unlock': 'ロック解除',
            'lock_tip': 'ファイルを書き込みから保護',
            'unlock_tip': 'ファイルの変更を許可'
        },
        'ko': {  # Korean
            'lock': '잠금',
            'unlock': '잠금 해제',
            'lock_tip': '쓰기로부터 파일 보호',
            'unlock_tip': '파일 수정 허용'
        },
        'ar': {  # Arabic
            'lock': 'قفل',
            'unlock': 'إلغاء القفل',
            'lock_tip': 'حماية الملف من الكتابة',
            'unlock_tip': 'السماح بتعديل الملف'
        },
        'he': {  # Hebrew
            'lock': 'נעל',
            'unlock': 'בטל נעילה',
            'lock_tip': 'הגן על הקובץ מכתיבה',
            'unlock_tip': 'אפשר שינוי קובץ'
        },
        'tr': {  # Turkish
            'lock': 'Kilitle',
            'unlock': 'Kilidi aç',
            'lock_tip': 'Dosyayı yazmaya karşı koru',
            'unlock_tip': 'Dosya değişikliğine izin ver'
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
                    
                # Check Chinese variants
                if 'zh_cn' in source or 'zh-cn' in source:
                    return 'zh_CN'
                elif 'zh_tw' in source or 'zh-tw' in source or 'zh_hk' in source:
                    return 'zh_TW'
                    
                # Check other languages
                for lang_code in translations.keys():
                    if lang_code.startswith('zh'):  # Already handled above
                        continue
                    if source.startswith(lang_code + '_') or source.startswith(lang_code + '-'):
                        return lang_code
            
            # Default language
            return 'en'
        
        detected_lang = detect_language()
        return translations.get(detected_lang, translations['en'])
        
    except Exception:
        # In case of error, use English
        return translations['en']

# Get localized texts
TEXTS = get_localized_text()


class LockFilesExtension(GObject.GObject, Nemo.MenuProvider):
    
    def __init__(self):
        super().__init__()
    
    def get_file_items(self, window, files):
        """Add 'Lock/Unlock' option to context menu (Nemo signature)"""
        if not files:
            return []
        
        # Check the status of the first selected file for the menu label
        first_file = files[0]
        uri = first_file.get_uri()
        file_path = unquote(uri.replace('file://', ''))
        
        try:
            # Determine whether to display "Lock" or "Unlock"
            if self.is_manually_locked(file_path):
                # Locked File → offer to unlock
                item = Nemo.MenuItem(
                    name='LockExtension::unlock',
                    label=TEXTS['unlock'],
                    tip=TEXTS['unlock_tip']
                )
                item.connect('activate', self.unlock_files, files)
            else:
                # Unlocked File → offer to lock
                item = Nemo.MenuItem(
                    name='LockExtension::lock',
                    label=TEXTS['lock'],
                    tip=TEXTS['lock_tip']
                )
                item.connect('activate', self.lock_files, files)
            
            return [item]
            
        except Exception:
            return []
    
    def is_manually_locked(self, file_path):
        """Check if file is locked (write-protected by user)"""
        try:
            file_stat = os.stat(file_path)
            file_mode = file_stat.st_mode
            current_uid = os.getuid()
            
            # Check if it is OUR file and read-only
            if file_stat.st_uid == current_uid:
                return not (file_mode & stat.S_IWUSR)
            
            return False
            
        except (OSError, PermissionError):
            return False
    
    def lock_files(self, menu, files):
        """Lock selected files (remove write permissions)"""
        for file_info in files:
            try:
                uri = file_info.get_uri()
                file_path = unquote(uri.replace('file://', ''))
                
                # Remove writing rights
                os.chmod(file_path, os.stat(file_path).st_mode & ~stat.S_IWUSR & ~stat.S_IWGRP & ~stat.S_IWOTH)
                
            except Exception:
                continue
    
    def unlock_files(self, menu, files):
        """Unlock selected files (restore write permissions)"""
        for file_info in files:
            try:
                uri = file_info.get_uri()
                file_path = unquote(uri.replace('file://', ''))
                
                # Give writing rights
                current_mode = os.stat(file_path).st_mode
                os.chmod(file_path, current_mode | stat.S_IWUSR)
                
            except Exception:
                continue


# Entry point for Nemo
def main():
    pass

if __name__ == "__main__":
    main()
