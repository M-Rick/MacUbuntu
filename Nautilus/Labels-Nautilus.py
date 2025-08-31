#!/usr/bin/env python3
"""
A Nautilus Extension to add color labels on files, like in macOS and Pantheon Files
Place in: ~/.local/share/nautilus-python/extensions/color_labels.py
"""
import os
import locale
import subprocess
from pathlib import Path
from gi.repository import Nautilus, GObject, Gio
from urllib.parse import unquote

# Dictionnaire des traductions
TRANSLATIONS = {
    'en': {
        'label': 'Label',
        'remove_label': 'Remove Label',
        'tip_assign': 'Assign color labels to files',
        'tip_remove': 'Remove color label from files',
        'colors': {
            'blueberry': 'Blueberry',
            'mint': 'Mint',
            'lime': 'Lime',
            'banana': 'Banana',
            'orange': 'Orange',
            'strawberry': 'Strawberry',
            'bubblegum': 'Bubblegum',
            'grape': 'Grape',
            'cocoa': 'Cocoa',
            'slate': 'Slate'
        }
    },
    'fr': {
        'label': 'Étiquette',
        'remove_label': 'Supprimer l\'étiquette',
        'tip_assign': 'Assigner des étiquettes de couleur aux fichiers',
        'tip_remove': 'Supprimer l\'étiquette de couleur des fichiers',
        'colors': {
            'blueberry': 'Myrtille',
            'mint': 'Menthe',
            'lime': 'Citron vert',
            'banana': 'Banane',
            'orange': 'Orange',
            'strawberry': 'Fraise',
            'bubblegum': 'Chewing-gum',
            'grape': 'Raisin',
            'cocoa': 'Cacao',
            'slate': 'Ardoise'
        }
    },
    'de': {
        'label': 'Etikett',
        'remove_label': 'Etikett entfernen',
        'tip_assign': 'Farbetiketten zu Dateien hinzufügen',
        'tip_remove': 'Farbetikett von Dateien entfernen',
        'colors': {
            'blueberry': 'Heidelbeere',
            'mint': 'Minze',
            'lime': 'Limette',
            'banana': 'Banane',
            'orange': 'Orange',
            'strawberry': 'Erdbeere',
            'bubblegum': 'Kaugummi',
            'grape': 'Traube',
            'cocoa': 'Kakao',
            'slate': 'Schiefer'
        }
    },
    'nl': {
        'label': 'Label',
        'remove_label': 'Label verwijderen',
        'tip_assign': 'Kleurlabels toewijzen aan bestanden',
        'tip_remove': 'Kleurlabel verwijderen van bestanden',
        'colors': {
            'blueberry': 'Bosbes',
            'mint': 'Munt',
            'lime': 'Limoen',
            'banana': 'Banaan',
            'orange': 'Sinaasappel',
            'strawberry': 'Aardbei',
            'bubblegum': 'Kauwgom',
            'grape': 'Druif',
            'cocoa': 'Cacao',
            'slate': 'Leisteen'
        }
    },
    'pl': {
        'label': 'Etykieta',
        'remove_label': 'Usuń etykietę',
        'tip_assign': 'Przypisz kolorowe etykiety do plików',
        'tip_remove': 'Usuń kolorową etykietę z plików',
        'colors': {
            'blueberry': 'Jagoda',
            'mint': 'Mięta',
            'banana': 'Banan',
            'orange': 'Pomarańczowy',
            'strawberry': 'Truskawka',
            'grape': 'Winogrono',
            'cocoa': 'Kakao',
            'slate': 'Łupek'
        }
    },
    'it': {
        'label': 'Etichetta',
        'remove_label': 'Rimuovi etichetta',
        'tip_assign': 'Assegna etichette colorate ai file',
        'tip_remove': 'Rimuovi etichetta colorata dai file',
        'colors': {
            'blueberry': 'Mirtillo',
            'mint': 'Menta',
            'lime': 'Lime',
            'banana': 'Banana',
            'orange': 'Arancia',
            'strawberry': 'Fragola',
            'bubblegum': 'Gomma da masticare',
            'grape': 'Uva',
            'cocoa': 'Cacao',
            'slate': 'Ardesia'
        }
    },
    'es': {
        'label': 'Etiqueta',
        'remove_label': 'Eliminar etiqueta',
        'tip_assign': 'Asignar etiquetas de color a archivos',
        'tip_remove': 'Eliminar etiqueta de color de archivos',
        'colors': {
            'blueberry': 'Arándano',
            'mint': 'Menta',
            'lime': 'Lima',
            'banana': 'Plátano',
            'orange': 'Naranja',
            'strawberry': 'Fresa',
            'bubblegum': 'Chicle',
            'grape': 'Uva',
            'cocoa': 'Cacao',
            'slate': 'Pizarra'
        }
    },
    'ja': {
        'label': 'ラベル',
        'remove_label': 'ラベルを削除',
        'tip_assign': 'ファイルにカラーラベルを設定',
        'tip_remove': 'ファイルからカラーラベルを削除',
        'colors': {
            'blueberry': 'ブルーベリー',
            'mint': 'ミント',
            'lime': 'ライム',
            'banana': 'バナナ',
            'orange': 'オレンジ',
            'strawberry': 'イチゴ',
            'bubblegum': 'バブルガム',
            'grape': 'ブドウ',
            'cocoa': 'ココア',
            'slate': 'スレート'
        }
    },
    'ko': {
        'label': '라벨',
        'remove_label': '라벨 제거',
        'tip_assign': '파일에 색상 라벨 지정',
        'tip_remove': '파일에서 색상 라벨 제거',
        'colors': {
            'blueberry': '블루베리',
            'mint': '민트',
            'banana': '바나나', 
            'orange': '오렌지',
            'strawberry': '딸기',
            'grape': '포도',
            'cocoa': '코코아',
            'slate': '슬레이트'
       }
    },
    'zh-cn': {
        'label': '标签',
        'remove_label': '移除标签',
        'tip_assign': '为文件分配颜色标签',
        'tip_remove': '从文件移除颜色标签',
        'colors': {
            'blueberry': '蓝莓',
            'mint': '薄荷',
            'lime': '酸橙',
            'banana': '香蕉',
            'orange': '橙子',
            'strawberry': '草莓',
            'bubblegum': '泡泡糖',
            'grape': '葡萄',
            'cocoa': '可可',
            'slate': '石板'
        }
    },
    'zh-tw': {
        'label': '標籤',
        'remove_label': '移除標籤',
        'tip_assign': '為檔案分配顏色標籤',
        'tip_remove': '從檔案移除顏色標籤',
        'colors': {
            'blueberry': '藍莓',
            'mint': '薄荷',
            'lime': '萊姆',
            'banana': '香蕉',
            'orange': '橘子',
            'strawberry': '草莓',
            'bubblegum': '泡泡糖',
            'grape': '葡萄',
            'cocoa': '可可',
            'slate': '石板'
        }
    },
    'ru': {
        'label': 'Метка',
        'remove_label': 'Удалить метку',
        'tip_assign': 'Назначить цветные метки файлам',
        'tip_remove': 'Удалить цветную метку с файлов',
        'colors': {
            'blueberry': 'Черника',
            'mint': 'Мята',
            'lime': 'Лайм',
            'banana': 'Банан',
            'orange': 'Апельсин',
            'strawberry': 'Клубника',
            'bubblegum': 'Жвачка',
            'grape': 'Виноград',
            'cocoa': 'Какао',
            'slate': 'Сланец'
        }
    }
}

def get_system_language():
    """Détecte la langue du système"""
    try:
        # Essayer d'abord la variable d'environnement LANGUAGE
        lang = os.environ.get('LANGUAGE', '').split(':')[0]
        if not lang:
            # Puis essayer LANG
            lang = os.environ.get('LANG', '').split('.')[0]
        if not lang:
            # En dernier recours, utiliser locale
            lang = locale.getlocale()[0]

        if lang:
            # Normaliser le code de langue
            lang_lower = lang.lower().replace('_', '-')
            if lang_lower.startswith('fr'):
                return 'fr'
            elif lang_lower.startswith('de'):
                return 'de'
            elif lang_lower.startswith('nl'):
                return 'nl'
            elif lang_lower.startswith('it'):
                return 'it'
            elif lang_lower.startswith('es'):
                return 'es'
            elif lang_lower.startswith('ja'):
                return 'ja'
            elif lang_lower.startswith('zh-cn') or lang_lower == 'zh-hans':
                return 'zh-cn'
            elif lang_lower.startswith('zh-tw') or lang_lower == 'zh-hant':
                return 'zh-tw'
            elif lang_lower.startswith('zh'):
                return 'zh-cn'  # Par défaut chinois simplifié
            elif lang_lower.startswith('ru'):
                return 'ru'
    except Exception as e:
        print(f"Error detecting language: {e}")

    return 'en'  # Par défaut anglais

class ColorLabelsExtension(GObject.GObject, Nautilus.MenuProvider, Nautilus.InfoProvider):

    COLORS = {
        'blueberry': {
            'name': 'Blueberry',
            'emoji': '🔵',
            'hex': '#3689e6',
            'emblem': 'label-blueberry'
        },
        'mint': {
            'name': 'Mint',
            'emoji': '🟢',
            'hex': '#28bca3',
            'emblem': 'label-mint'
        },
        'banana': {
            'name': 'Banana',
            'emoji': '🟡',
            'hex': '#f9c440',
            'emblem': 'label-banana'
        },
        'orange': {
            'name': 'Orange',
            'emoji': '🟠',
            'hex': '#ffa154',
            'emblem': 'label-orange'
        },
        'strawberry': {
            'name': 'Strawberry',
            'emoji': '🔴',
            'hex': '#ed5353',
            'emblem': 'label-strawberry'
        },
        'grape': {
            'name': 'Grape',
            'emoji': '🟣',
            'hex': '#a56de2',
            'emblem': 'label-grape'
        },
        'cocoa': {
            'name': 'Cocoa',
            'emoji': '🟤',
            'hex': '#8a715e',
            'emblem': 'label-cocoa'
        },
        'slate': {
            'name': 'Slate',
            'emoji': '⚪',
            'hex': '#667885',
            'emblem': 'label-slate'
        }
    }

    def __init__(self):
        super().__init__()
        self.current_language = get_system_language()
        self.translations = TRANSLATIONS.get(self.current_language, TRANSLATIONS['en'])
        
        # Vérifier et créer les emblèmes si nécessaire
        self.ensure_emblems_exist()

    def ensure_emblems_exist(self):
        """Vérifie et crée les emblèmes SVG s'ils n'existent pas"""
        emblem_dir = Path.home() / '.local' / 'share' / 'icons' / 'hicolor' / '16x16' / 'emblems'
        
        try:
            # Créer le répertoire s'il n'existe pas
            emblem_dir.mkdir(parents=True, exist_ok=True)
            
            # Vérifier si tous les emblèmes existent
            missing_emblems = []
            for color_id, color_info in self.COLORS.items():
                emblem_file = emblem_dir / f"{color_info['emblem']}.svg"
                if not emblem_file.exists():
                    missing_emblems.append((color_id, color_info))
            
            # Créer les emblèmes manquants
            if missing_emblems:
                print(f"Creating {len(missing_emblems)} missing color emblems...")
                for color_id, color_info in missing_emblems:
                    self.create_emblem_svg(color_info['emblem'], color_info['hex'], emblem_dir)
                
                # Mettre à jour le cache d'icônes
                self.update_icon_cache()
                
        except Exception as e:
            print(f"Error ensuring emblems exist: {e}")

    def create_emblem_svg(self, emblem_name, hex_color, emblem_dir):
        """Crée un fichier SVG d'emblème coloré"""
        svg_content = f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   width="16"
   height="16"
   viewBox="0 0 4.233333 4.233333"
   version="1.1"
   id="svg1"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:svg="http://www.w3.org/2000/svg">
  <defs
     id="defs1" />
  <g
     id="layer1">
    <ellipse
       style="fill:{hex_color};fill-opacity:1;stroke-width:0.264999"
       id="path1"
       cx="2.1166666"
       cy="2.1166666"
       rx="2.1170001"
       ry="2.1166666" />
  </g>
</svg>'''
        
        try:
            svg_file = emblem_dir / f"{emblem_name}.svg"
            svg_file.write_text(svg_content)
            print(f"✓ Created: {svg_file}")
        except Exception as e:
            print(f"Error creating {emblem_name}.svg: {e}")

    def update_icon_cache(self):
        """Met à jour le cache d'icônes"""
        try:
            hicolor_dir = Path.home() / '.local' / 'share' / 'icons' / 'hicolor'
            subprocess.run(['gtk-update-icon-cache', str(hicolor_dir)], 
                         check=False, capture_output=True)
            print("✓ Icon cache updated")
        except Exception as e:
            print(f"Warning: Could not update icon cache: {e}")

    def get_file_items(self, files):
        """Crée le menu Label avec sous-menu de couleurs"""
        if not files:
            return []

        main_item = Nautilus.MenuItem(
            name='ColorLabels::main',
            label=self.translations['label'],
            tip=self.translations['tip_assign']
        )

        submenu = Nautilus.Menu()
        main_item.set_submenu(submenu)

        for color_id, color_info in self.COLORS.items():
            color_name = self.translations['colors'].get(color_id, color_info['name'])
            color_item = Nautilus.MenuItem(
                name=f'ColorLabels::{color_id}',
                label=f"{color_info['emoji']} {color_name}",
                tip=f"Label files as {color_name}"
            )
            color_item.connect('activate', self.apply_color_label, files, color_id)
            submenu.append_item(color_item)

        # Ajouter une vraie ligne de séparation
        try:
            # Essayer d'abord la méthode native pour les séparateurs
            submenu.append_separator()
        except AttributeError:
            # Si append_separator n'existe pas, utiliser un MenuItem séparateur
            separator = Nautilus.MenuItem(
                name='ColorLabels::separator',
                label=None,
                sensitive=False
            )
            try:
                # Essayer de définir comme séparateur
                separator.set_property('separator', True)
            except:
                # Dernier recours : utiliser une ligne fine discrète
                separator.set_property('label', '————————————————')

            submenu.append_item(separator)

        remove_item = Nautilus.MenuItem(
            name='ColorLabels::remove',
            label=f'{self.translations["remove_label"]}',
            tip=self.translations['tip_remove']
        )
        remove_item.connect('activate', self.remove_color_label, files)
        submenu.append_item(remove_item)

        return [main_item]

    def apply_color_label(self, menu, files, color_id):
        """Applique un label de couleur aux fichiers sélectionnés"""
        color_info = self.COLORS.get(color_id)
        if not color_info:
            return

        for file_info in files:
            try:
                uri = file_info.get_uri()
                file_path = unquote(uri.replace('file://', ''))

                # 1. Supprimer l'emblème actuel
                self.remove_emblem_metadata(file_path)

                # 2. Ajouter le nouvel emblème directement via Nautilus (affichage immédiat)
                file_info.add_emblem(color_info['emblem'])

                # 3. Stocker le nouvel emblème dans les métadonnées pour la persistance
                self.set_emblem_metadata(file_path, color_info['emblem'])

                # 4. Rafraîchir immédiatement le fichier
                self.refresh_file(file_path)

            except Exception as e:
                print(f"Error applying label: {e}")
                continue

    def remove_color_label(self, menu, files):
        """Supprime le label de couleur des fichiers sélectionnés"""
        for file_info in files:
            try:
                uri = file_info.get_uri()
                file_path = unquote(uri.replace('file://', ''))

                # 1. Supprimer l'emblème des métadonnées
                self.remove_emblem_metadata(file_path)

                # 2. Rafraîchir le fichier
                self.refresh_file(file_path)

            except Exception as e:
                print(f"Error removing label: {e}")
                continue

    def set_emblem_metadata(self, file_path, emblem):
        """Stocke l'emblème dans les métadonnées du fichier"""
        try:
            file = Gio.File.new_for_path(file_path)
            file.set_attribute_string(
                'metadata::emblems',
                emblem,
                Gio.FileQueryInfoFlags.NONE,
                None
            )
        except Exception as e:
            print(f"Failed to set emblem metadata: {e}")

    def remove_emblem_metadata(self, file_path):
        """Supprime l'emblème des métadonnées du fichier"""
        try:
            file = Gio.File.new_for_path(file_path)
            file.set_attribute_string(
                'metadata::emblems',
                '',
                Gio.FileQueryInfoFlags.NONE,
                None
            )
        except Exception as e:
            print(f"Failed to remove emblem metadata: {e}")

    def refresh_file(self, file_path):
        """Force le rafraîchissement du fichier dans Nautilus"""
        try:
            # Utiliser Gio pour déclencher un événement de changement
            file = Gio.File.new_for_path(file_path)
            file.monitor_file(Gio.FileMonitorFlags.NONE, None)
            # Toucher le fichier pour forcer le rafraîchissement
            os.utime(file_path, None)
        except Exception as e:
            print(f"Failed to refresh file: {e}")

    def update_file_info(self, file):
        """Recharge les emblèmes depuis les métadonnées à chaque affichage"""
        try:
            uri = file.get_uri()
            if not uri.startswith('file://'):
                return

            file_path = unquote(uri.replace('file://', ''))
            if not os.path.exists(file_path):
                return

            # Récupérer l'emblème depuis les métadonnées
            file_gio = Gio.File.new_for_path(file_path)
            info = file_gio.query_info(
                'metadata::emblems',
                Gio.FileQueryInfoFlags.NONE,
                None
            )
            emblem = info.get_attribute_as_string('metadata::emblems')

            if emblem:
                file.add_emblem(emblem)

        except Exception as e:
            print(f"Error updating file info: {e}")

def main():
    pass

if __name__ == "__main__":
    main()
