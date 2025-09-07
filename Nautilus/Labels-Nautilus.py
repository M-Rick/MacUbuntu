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

def get_localized_text():
    """Returns texts according to system language"""
    
    # Translations
    translations = {
        'en': {  # English (default)
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
        'de': {  # German
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
        'nl': {  # Dutch
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
        'sv': {  # Swedish
            'label': 'Etikett',
            'remove_label': 'Ta bort etikett',
            'tip_assign': 'Tilldela färgetiketter till filer',
            'tip_remove': 'Ta bort färgetikett från filer',
            'colors': {
                'blueberry': 'Blåbär',
                'mint': 'Mynta',
                'lime': 'Lime',
                'banana': 'Banan',
                'orange': 'Apelsin',
                'strawberry': 'Jordgubbe',
                'bubblegum': 'Tuggummi',
                'grape': 'Druva',
                'cocoa': 'Kakao',
                'slate': 'Skiffer'
            }
        },
        'da': {  # Danish
            'label': 'Etiket',
            'remove_label': 'Fjern etiket',
            'tip_assign': 'Tildel farveetiketter til filer',
            'tip_remove': 'Fjern farveetiket fra filer',
            'colors': {
                'blueberry': 'Blåbær',
                'mint': 'Mynte',
                'lime': 'Lime',
                'banana': 'Banan',
                'orange': 'Orange',
                'strawberry': 'Jordbær',
                'bubblegum': 'Tyggegummi',
                'grape': 'Drue',
                'cocoa': 'Kakao',
                'slate': 'Skifer'
            }
        },
        'no': {  # Norwegian
            'label': 'Etikett',
            'remove_label': 'Fjern etikett',
            'tip_assign': 'Tildel fargetiketter til filer',
            'tip_remove': 'Fjern fargetikett fra filer',
            'colors': {
                'blueberry': 'Blåbær',
                'mint': 'Mynte',
                'lime': 'Lime',
                'banana': 'Banan',
                'orange': 'Appelsin',
                'strawberry': 'Jordbær',
                'bubblegum': 'Tyggegummi',
                'grape': 'Drue',
                'cocoa': 'Kakao',
                'slate': 'Skifer'
            }
        },
        'fi': {  # Finnish
            'label': 'Tunniste',
            'remove_label': 'Poista tunniste',
            'tip_assign': 'Määritä värillisiä tunnisteita tiedostoille',
            'tip_remove': 'Poista värillinen tunniste tiedostoista',
            'colors': {
                'blueberry': 'Mustikka',
                'mint': 'Minttu',
                'lime': 'Limetti',
                'banana': 'Banaani',
                'orange': 'Appelsiini',
                'strawberry': 'Mansikka',
                'bubblegum': 'Purukumi',
                'grape': 'Rypäle',
                'cocoa': 'Kaakao',
                'slate': 'Liuske'
            }
        },
        'fr': {  # French
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
        'it': {  # Italian
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
        'es': {  # Spanish
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
        'pt': {  # Portuguese
            'label': 'Etiqueta',
            'remove_label': 'Remover etiqueta',
            'tip_assign': 'Atribuir etiquetas coloridas a arquivos',
            'tip_remove': 'Remover etiqueta colorida de arquivos',
            'colors': {
                'blueberry': 'Mirtilo',
                'mint': 'Hortelã',
                'lime': 'Lima',
                'banana': 'Banana',
                'orange': 'Laranja',
                'strawberry': 'Morango',
                'bubblegum': 'Chiclete',
                'grape': 'Uva',
                'cocoa': 'Cacau',
                'slate': 'Ardósia'
            }
        },
        'ro': {  # Romanian
            'label': 'Etichetă',
            'remove_label': 'Șterge eticheta',
            'tip_assign': 'Atribuie etichete colorate fișierelor',
            'tip_remove': 'Șterge eticheta colorată de pe fișiere',
            'colors': {
                'blueberry': 'Afină',
                'mint': 'Mentă',
                'lime': 'Lămâie verde',
                'banana': 'Banană',
                'orange': 'Portocală',
                'strawberry': 'Căpșună',
                'bubblegum': 'Gumă de mestecat',
                'grape': 'Strugure',
                'cocoa': 'Cacao',
                'slate': 'Ardezie'
            }
        },
        'pl': {  # Polish
            'label': 'Etykieta',
            'remove_label': 'Usuń etykietę',
            'tip_assign': 'Przypisz kolorowe etykiety do plików',
            'tip_remove': 'Usuń kolorową etykietę z plików',
            'colors': {
                'blueberry': 'Jagoda',
                'mint': 'Mięta',
                'lime': 'Limonka',
                'banana': 'Banan',
                'orange': 'Pomarańcza',
                'strawberry': 'Truskawka',
                'bubblegum': 'Guma do żucia',
                'grape': 'Winogrono',
                'cocoa': 'Kakao',
                'slate': 'Łupek'
            }
        },
        'hu': {  # Hungarian
            'label': 'Címke',
            'remove_label': 'Címke eltávolítása',
            'tip_assign': 'Színes címkék hozzárendelése fájlokhoz',
            'tip_remove': 'Színes címke eltávolítása fájlokról',
            'colors': {
                'blueberry': 'Áfonya',
                'mint': 'Menta',
                'lime': 'Lime',
                'banana': 'Banán',
                'orange': 'Narancs',
                'strawberry': 'Eper',
                'bubblegum': 'Rágógumi',
                'grape': 'Szőlő',
                'cocoa': 'Kakaó',
                'slate': 'Pala'
            }
        },
        'ru': {  # Russian
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
        },
        'zh_CN': {  # Simplified Chinese
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
        'zh_TW': {  # Traditional Chinese
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
        'ja': {  # Japanese
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
        'ko': {  # Korean
            'label': '라벨',
            'remove_label': '라벨 제거',
            'tip_assign': '파일에 컬러 라벨 할당',
            'tip_remove': '파일에서 컬러 라벨 제거',
            'colors': {
                'blueberry': '블루베리',
                'mint': '민트',
                'lime': '라임',
                'banana': '바나나',
                'orange': '오렌지',
                'strawberry': '딸기',
                'bubblegum': '버블껌',
                'grape': '포도',
                'cocoa': '코코아',
                'slate': '슬레이트'
            }
        },
        'ar': {  # Arabic
            'label': 'تسمية',
            'remove_label': 'إزالة التسمية',
            'tip_assign': 'تعيين تسميات ملونة للملفات',
            'tip_remove': 'إزالة التسمية الملونة من الملفات',
            'colors': {
                'blueberry': 'توت أزرق',
                'mint': 'نعناع',
                'lime': 'ليمون أخضر',
                'banana': 'موز',
                'orange': 'برتقال',
                'strawberry': 'فراولة',
                'bubblegum': 'علكة',
                'grape': 'عنب',
                'cocoa': 'كاكاو',
                'slate': 'أردواز'
            }
        },
        'he': {  # Hebrew
            'label': 'תווית',
            'remove_label': 'הסר תווית',
            'tip_assign': 'הקצה תוויות צבעוניות לקבצים',
            'tip_remove': 'הסר תווית צבעונית מקבצים',
            'colors': {
                'blueberry': 'אוכמנית',
                'mint': 'נענע',
                'lime': 'ליים',
                'banana': 'בננה',
                'orange': 'כתום',
                'strawberry': 'תות שדה',
                'bubblegum': 'מסטיק',
                'grape': 'ענב',
                'cocoa': 'קקאו',
                'slate': 'צפחה'
            }
        },
        'tr': {  # Turkish
            'label': 'Etiket',
            'remove_label': 'Etiketi kaldır',
            'tip_assign': 'Dosyalara renkli etiketler ata',
            'tip_remove': 'Dosyalardan renkli etiketi kaldır',
            'colors': {
                'blueberry': 'Yaban mersini',
                'mint': 'Nane',
                'lime': 'Misket limonu',
                'banana': 'Muz',
                'orange': 'Portakal',
                'strawberry': 'Çilek',
                'bubblegum': 'Sakız',
                'grape': 'Üzüm',
                'cocoa': 'Kakao',
                'slate': 'Arduvaz'
            }
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
        # Check and create emblems if necessary
        self.ensure_emblems_exist()

    def ensure_emblems_exist(self):
        """Check and create SVG emblems if they don't exist"""
        emblem_dir = Path.home() / '.local' / 'share' / 'icons' / 'hicolor' / '16x16' / 'emblems'

        try:
            # Create directory if it doesn't exist
            emblem_dir.mkdir(parents=True, exist_ok=True)

            # Check if all emblems exist
            missing_emblems = []
            for color_id, color_info in self.COLORS.items():
                emblem_file = emblem_dir / f"{color_info['emblem']}.svg"
                if not emblem_file.exists():
                    missing_emblems.append((color_id, color_info))

            # Create missing emblems
            if missing_emblems:
                print(f"Creating {len(missing_emblems)} missing color emblems...")
                for color_id, color_info in missing_emblems:
                    self.create_emblem_svg(color_info['emblem'], color_info['hex'], emblem_dir)

                # Update icon cache
                self.update_icon_cache()

        except Exception as e:
            print(f"Error ensuring emblems exist: {e}")

    def create_emblem_svg(self, emblem_name, hex_color, emblem_dir):
        """Create a colored emblem SVG file"""
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
        """Update icon cache"""
        try:
            hicolor_dir = Path.home() / '.local' / 'share' / 'icons' / 'hicolor'
            subprocess.run(['gtk-update-icon-cache', str(hicolor_dir)],
                         check=False, capture_output=True)
            print("✓ Icon cache updated")
        except Exception as e:
            print(f"Warning: Could not update icon cache: {e}")

    def get_file_items(self, files):
        """Create Label menu with color submenu"""
        if not files:
            return []

        main_item = Nautilus.MenuItem(
            name='ColorLabels::main',
            label=TEXTS['label'],
            tip=TEXTS['tip_assign']
        )

        submenu = Nautilus.Menu()
        main_item.set_submenu(submenu)

        for color_id, color_info in self.COLORS.items():
            color_name = TEXTS['colors'].get(color_id, color_info['name'])
            color_item = Nautilus.MenuItem(
                name=f'ColorLabels::{color_id}',
                label=f"{color_info['emoji']} {color_name}",
                tip=f"Label files as {color_name}"
            )
            color_item.connect('activate', self.apply_color_label, files, color_id)
            submenu.append_item(color_item)

        # Add separator
        try:
            # Try native method for separators first
            submenu.append_separator()
        except AttributeError:
            # If append_separator doesn't exist, use separator MenuItem
            separator = Nautilus.MenuItem(
                name='ColorLabels::separator',
                label=None,
                sensitive=False
            )
            try:
                # Try to set as separator
                separator.set_property('separator', True)
            except:
                # Last resort: use thin discrete line
                separator.set_property('label', '————————————————')

            submenu.append_item(separator)

        remove_item = Nautilus.MenuItem(
            name='ColorLabels::remove',
            label=TEXTS["remove_label"],
            tip=TEXTS['tip_remove']
        )
        remove_item.connect('activate', self.remove_color_label, files)
        submenu.append_item(remove_item)

        return [main_item]

    def apply_color_label(self, menu, files, color_id):
        """Apply color label to selected files"""
        color_info = self.COLORS.get(color_id)
        if not color_info:
            return

        for file_info in files:
            try:
                uri = file_info.get_uri()
                file_path = unquote(uri.replace('file://', ''))

                # 1. Remove current emblem
                self.remove_emblem_metadata(file_path)

                # 2. Add new emblem directly via Nautilus (immediate display)
                file_info.add_emblem(color_info['emblem'])

                # 3. Store new emblem in metadata for persistence
                self.set_emblem_metadata(file_path, color_info['emblem'])

                # 4. Refresh file immediately
                self.refresh_file(file_path)

            except Exception as e:
                print(f"Error applying label: {e}")
                continue

    def remove_color_label(self, menu, files):
        """Remove color label from selected files"""
        for file_info in files:
            try:
                uri = file_info.get_uri()
                file_path = unquote(uri.replace('file://', ''))

                # 1. Remove emblem from metadata
                self.remove_emblem_metadata(file_path)

                # 2. Refresh file
                self.refresh_file(file_path)

            except Exception as e:
                print(f"Error removing label: {e}")
                continue

    def set_emblem_metadata(self, file_path, emblem):
        """Store emblem in file metadata"""
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
        """Remove emblem from file metadata"""
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
        """Force file refresh in Nautilus"""
        try:
            # Use Gio to trigger change event
            file = Gio.File.new_for_path(file_path)
            file.monitor_file(Gio.FileMonitorFlags.NONE, None)
            # Touch file to force refresh
            os.utime(file_path, None)
        except Exception as e:
            print(f"Failed to refresh file: {e}")

    def update_file_info(self, file):
        """Reload emblems from metadata on each display"""
        try:
            uri = file.get_uri()
            if not uri.startswith('file://'):
                return

            file_path = unquote(uri.replace('file://', ''))
            if not os.path.exists(file_path):
                return

            # Get emblem from metadata
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
