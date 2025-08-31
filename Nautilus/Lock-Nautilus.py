#!/usr/bin/env python3
"""
A Nautilus Extension to manage files locking by adding an additionnal "Lock/Unlock" menu
Place in ~/.local/share/nautilus-python/extensions/lock_files.py
"""

import os
import stat
import locale
from gi.repository import Nautilus, GObject
from urllib.parse import unquote
from pathlib import Path


# Localization
def get_lock_texts():
    try:
        lang = os.environ.get('LANG', '').lower()
        
        if lang.startswith('fr'):  # French
            return {
                'lock': 'Verrouiller',
                'unlock': 'Déverrouiller',
                'lock_tip': 'Protéger le fichier en écriture',
                'unlock_tip': 'Autoriser la modification du fichier'
            }
        elif lang.startswith('de'):  # German
            return {
                'lock': 'Sperren',
                'unlock': 'Entsperren',
                'lock_tip': 'Datei vor Schreibzugriff schützen',
                'unlock_tip': 'Änderung der Datei erlauben'
            }
        elif lang.startswith('nl'):  # Dutch
            return {
                'lock': 'Vergrendelen',
                'unlock': 'Ontgrendelen',
                'lock_tip': 'Bestand beschermen tegen schrijven',
                'unlock_tip': 'Wijziging van bestand toestaan'
            }
        elif lang.startswith('it'):  # Italian
            return {
                'lock': 'Blocca',
                'unlock': 'Sblocca',
                'lock_tip': 'Proteggi il file dalla scrittura',
                'unlock_tip': 'Consenti la modifica del file'
            }
        elif lang.startswith('es'):  # Spanish
            return {
                'lock': 'Bloquear',
                'unlock': 'Desbloquear',
                'lock_tip': 'Proteger archivo contra escritura',
                'unlock_tip': 'Permitir modificación del archivo'
            }
        elif lang.startswith('ja'):  # Japonese
            return {
                'lock': 'ロック',
                'unlock': 'ロック解除',
                'lock_tip': 'ファイルを書き込みから保護',
                'unlock_tip': 'ファイルの変更を許可'
            }
        elif lang.startswith('zh_cn') or 'zh-cn' in lang:  # Simplified Chinese
            return {
                'lock': '锁定',
                'unlock': '解锁',
                'lock_tip': '保护文件免受写入',
                'unlock_tip': '允许修改文件'
            }
        elif lang.startswith('zh_tw') or 'zh-tw' in lang:  # Traditionnal Chinese
            return {
                'lock': '鎖定',
                'unlock': '解鎖',
                'lock_tip': '保護檔案免受寫入',
                'unlock_tip': '允許修改檔案'
            }
        elif lang.startswith('ru'):  # Russian
            return {
                'lock': 'Заблокировать',
                'unlock': 'Разблокировать',
                'lock_tip': 'Защитить файл от записи',
                'unlock_tip': 'Разрешить изменение файла'
            }
        else:  # English (default)
            return {
                'lock': 'Lock',
                'unlock': 'Unlock', 
                'lock_tip': 'Protect file from writing',
                'unlock_tip': 'Allow file modification'
            }
    except:
        return {
            'lock': 'Lock',
            'unlock': 'Unlock',
            'lock_tip': 'Protect file from writing', 
            'unlock_tip': 'Allow file modification'
        }

TEXTS = get_lock_texts()


class LockFilesExtension(GObject.GObject, Nautilus.MenuProvider):
    
    def __init__(self):
        super().__init__()
    
    def get_file_items(self, files):
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
                item = Nautilus.MenuItem(
                    name='LockExtension::unlock',
                    label=TEXTS['unlock'],
                    tip=TEXTS['unlock_tip']
                )
                item.connect('activate', self.unlock_files, files)
            else:
                # Unlocked File → offer to lock
                item = Nautilus.MenuItem(
                    name='LockExtension::lock',
                    label=TEXTS['lock'],
                    tip=TEXTS['lock_tip']
                )
                item.connect('activate', self.lock_files, files)
            
            return [item]
            
        except Exception:
            return []
    
    def is_manually_locked(self, file_path):
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
        for file_info in files:
            try:
                uri = file_info.get_uri()
                file_path = unquote(uri.replace('file://', ''))
                
                # Remove writting rights
                os.chmod(file_path, os.stat(file_path).st_mode & ~stat.S_IWUSR & ~stat.S_IWGRP & ~stat.S_IWOTH)
                
            except Exception:
                continue
    
    def unlock_files(self, menu, files):
        """Déverrouille les fichiers sélectionnés (restaure l'écriture)"""
        for file_info in files:
            try:
                uri = file_info.get_uri()
                file_path = unquote(uri.replace('file://', ''))
                
                # Give writting rights
                current_mode = os.stat(file_path).st_mode
                os.chmod(file_path, current_mode | stat.S_IWUSR)
                
            except Exception:
                continue


# Entry point for Nautilus
def main():
    pass

if __name__ == "__main__":
    main()
  
