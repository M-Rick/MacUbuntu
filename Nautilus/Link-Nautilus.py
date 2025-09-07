#!/usr/bin/env python3
"""
A Nautilus Extension to create symbolic links, like in Nemo
Place in: ~/.local/share/nautilus-python/extensions/create_link.py
"""
import os
import locale
from pathlib import Path
from gi.repository import Nautilus, GObject, Gio
from urllib.parse import unquote

def get_localized_text():
    """Returns texts according to system language"""
    
    # Translations
    translations = {
        'en': {  # English (default)
            'create_link': 'Create Link',
            'tip_create_link': 'Create a symbolic link to the selected item',
            'link_suffix': ' - Link',
            'error_title': 'Error Creating Link',
            'error_exists': 'A file with this name already exists',
            'error_permission': 'Permission denied',
            'error_generic': 'Failed to create symbolic link'
        },
        'de': {  # German
            'create_link': 'Link erstellen',
            'tip_create_link': 'Einen symbolischen Link zum ausgewählten Element erstellen',
            'link_suffix': ' - Link',
            'error_title': 'Fehler beim Erstellen des Links',
            'error_exists': 'Eine Datei mit diesem Namen existiert bereits',
            'error_permission': 'Zugriff verweigert',
            'error_generic': 'Fehler beim Erstellen des symbolischen Links'
        },
        'nl': {  # Dutch
            'create_link': 'Link maken',
            'tip_create_link': 'Een symbolische link naar het geselecteerde item maken',
            'link_suffix': ' - Link',
            'error_title': 'Fout bij maken van link',
            'error_exists': 'Een bestand met deze naam bestaat al',
            'error_permission': 'Toegang geweigerd',
            'error_generic': 'Fout bij maken van symbolische link'
        },
        'sv': {  # Swedish
            'create_link': 'Skapa länk',
            'tip_create_link': 'Skapa en symbolisk länk till det valda objektet',
            'link_suffix': ' - Länk',
            'error_title': 'Fel vid skapande av länk',
            'error_exists': 'En fil med detta namn finns redan',
            'error_permission': 'Åtkomst nekad',
            'error_generic': 'Misslyckades att skapa symbolisk länk'
        },
        'da': {  # Danish
            'create_link': 'Opret link',
            'tip_create_link': 'Opret et symbolsk link til det valgte element',
            'link_suffix': ' - Link',
            'error_title': 'Fejl ved oprettelse af link',
            'error_exists': 'En fil med dette navn findes allerede',
            'error_permission': 'Adgang nægtet',
            'error_generic': 'Kunne ikke oprette symbolsk link'
        },
        'no': {  # Norwegian
            'create_link': 'Opprett lenke',
            'tip_create_link': 'Opprett en symbolsk lenke til det valgte elementet',
            'link_suffix': ' - Lenke',
            'error_title': 'Feil ved oppretting av lenke',
            'error_exists': 'En fil med dette navnet finnes allerede',
            'error_permission': 'Tilgang nektet',
            'error_generic': 'Kunne ikke opprette symbolsk lenke'
        },
        'fi': {  # Finnish
            'create_link': 'Luo linkki',
            'tip_create_link': 'Luo symbolinen linkki valittuun kohteeseen',
            'link_suffix': ' - Linkki',
            'error_title': 'Virhe linkin luomisessa',
            'error_exists': 'Tämän niminen tiedosto on jo olemassa',
            'error_permission': 'Käyttöoikeus evätty',
            'error_generic': 'Symbolisen linkin luominen epäonnistui'
        },
        'fr': {  # French
            'create_link': 'Créer un lien',
            'tip_create_link': 'Créer un lien symbolique vers l\'élément sélectionné',
            'link_suffix': ' - Lien',
            'error_title': 'Erreur lors de la création du lien',
            'error_exists': 'Un fichier avec ce nom existe déjà',
            'error_permission': 'Permission refusée',
            'error_generic': 'Échec de la création du lien symbolique'
        },
        'it': {  # Italian
            'create_link': 'Crea collegamento',
            'tip_create_link': 'Crea un collegamento simbolico all\'elemento selezionato',
            'link_suffix': ' - Collegamento',
            'error_title': 'Errore nella creazione del collegamento',
            'error_exists': 'Esiste già un file con questo nome',
            'error_permission': 'Permesso negato',
            'error_generic': 'Impossibile creare il collegamento simbolico'
        },
        'es': {  # Spanish
            'create_link': 'Crear enlace',
            'tip_create_link': 'Crear un enlace simbólico al elemento seleccionado',
            'link_suffix': ' - Enlace',
            'error_title': 'Error al crear enlace',
            'error_exists': 'Ya existe un archivo con este nombre',
            'error_permission': 'Permiso denegado',
            'error_generic': 'Error al crear el enlace simbólico'
        },
        'pt': {  # Portuguese
            'create_link': 'Criar link',
            'tip_create_link': 'Criar um link simbólico para o item selecionado',
            'link_suffix': ' - Link',
            'error_title': 'Erro ao criar link',
            'error_exists': 'Um arquivo com este nome já existe',
            'error_permission': 'Permissão negada',
            'error_generic': 'Falha ao criar link simbólico'
        },
        'ro': {  # Romanian
            'create_link': 'Creează legătură',
            'tip_create_link': 'Creează o legătură simbolică către elementul selectat',
            'link_suffix': ' - Legătură',
            'error_title': 'Eroare la crearea legăturii',
            'error_exists': 'Există deja un fișier cu acest nume',
            'error_permission': 'Permisiune refuzată',
            'error_generic': 'Nu s-a putut crea legătura simbolică'
        },
        'pl': {  # Polish
            'create_link': 'Utwórz link',
            'tip_create_link': 'Utwórz dowiązanie symboliczne do wybranego elementu',
            'link_suffix': ' - Link',
            'error_title': 'Błąd tworzenia linku',
            'error_exists': 'Plik o tej nazwie już istnieje',
            'error_permission': 'Brak uprawnień',
            'error_generic': 'Nie udało się utworzyć dowiązania symbolicznego'
        },
        'hu': {  # Hungarian
            'create_link': 'Link létrehozása',
            'tip_create_link': 'Szimbolikus link létrehozása a kiválasztott elemhez',
            'link_suffix': ' - Link',
            'error_title': 'Hiba a link létrehozásakor',
            'error_exists': 'Már létezik fájl ezzel a névvel',
            'error_permission': 'Hozzáférés megtagadva',
            'error_generic': 'Szimbolikus link létrehozása sikertelen'
        },
        'ru': {  # Russian
            'create_link': 'Создать ссылку',
            'tip_create_link': 'Создать символическую ссылку на выбранный элемент',
            'link_suffix': ' - Ссылка',
            'error_title': 'Ошибка создания ссылки',
            'error_exists': 'Файл с таким именем уже существует',
            'error_permission': 'Доступ запрещен',
            'error_generic': 'Не удалось создать символическую ссылку'
        },
        'zh_CN': {  # Simplified Chinese
            'create_link': '创建链接',
            'tip_create_link': '为选定项目创建符号链接',
            'link_suffix': ' - 链接',
            'error_title': '创建链接错误',
            'error_exists': '已存在此名称的文件',
            'error_permission': '权限被拒绝',
            'error_generic': '创建符号链接失败'
        },
        'zh_TW': {  # Traditional Chinese
            'create_link': '建立連結',
            'tip_create_link': '為選定項目建立符號連結',
            'link_suffix': ' - 連結',
            'error_title': '建立連結錯誤',
            'error_exists': '已存在此名稱的檔案',
            'error_permission': '權限被拒絕',
            'error_generic': '建立符號連結失敗'
        },
        'ja': {  # Japanese
            'create_link': 'リンクを作成',
            'tip_create_link': '選択したアイテムへのシンボリックリンクを作成',
            'link_suffix': ' - リンク',
            'error_title': 'リンク作成エラー',
            'error_exists': 'この名前のファイルは既に存在します',
            'error_permission': 'アクセス拒否',
            'error_generic': 'シンボリックリンクの作成に失敗しました'
        },
        'ko': {  # Korean
            'create_link': '링크 생성',
            'tip_create_link': '선택한 항목에 대한 심볼릭 링크 생성',
            'link_suffix': ' - 링크',
            'error_title': '링크 생성 오류',
            'error_exists': '이 이름의 파일이 이미 존재합니다',
            'error_permission': '권한 거부됨',
            'error_generic': '심볼릭 링크 생성에 실패했습니다'
        },
        'hi': {  # Hindi
            'create_link': 'लिंक बनाएं',
            'tip_create_link': 'चयनित आइटम के लिए एक सिंबॉलिक लिंक बनाएं',
            'link_suffix': ' - लिंक',
            'error_title': 'लिंक बनाने में त्रुटि',
            'error_exists': 'इस नाम की फाइल पहले से मौजूद है',
            'error_permission': 'अनुमति अस्वीकृत',
            'error_generic': 'सिंबॉलिक लिंक बनाने में विफल'
        },
        'ar': {  # Arabic
            'create_link': 'إنشاء رابط',
            'tip_create_link': 'إنشاء رابط رمزي للعنصر المحدد',
            'link_suffix': ' - رابط',
            'error_title': 'خطأ في إنشاء الرابط',
            'error_exists': 'يوجد ملف بهذا الاسم بالفعل',
            'error_permission': 'تم رفض الإذن',
            'error_generic': 'فشل في إنشاء الرابط الرمزي'
        },
        'he': {  # Hebrew
            'create_link': 'צור קישור',
            'tip_create_link': 'צור קישור סימבולי לפריט הנבחר',
            'link_suffix': ' - קישור',
            'error_title': 'שגיאה ביצירת קישור',
            'error_exists': 'קיים כבר קובץ בשם זה',
            'error_permission': 'הרשאה נדחתה',
            'error_generic': 'יצירת קישור סימבולי נכשלה'
        },
        # Turkic
        'tr': {  # Turkish
            'create_link': 'Bağlantı oluştur',
            'tip_create_link': 'Seçilen öğeye sembolik bağlantı oluştur',
            'link_suffix': ' - Bağlantı',
            'error_title': 'Bağlantı oluşturma hatası',
            'error_exists': 'Bu isimde bir dosya zaten var',
            'error_permission': 'İzin reddedildi',
            'error_generic': 'Sembolik bağlantı oluşturulamadı'
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

class CreateLinkExtension(GObject.GObject, Nautilus.MenuProvider):

    def __init__(self):
        super().__init__()

    def get_file_items(self, files):
        """Create the Create Link menu"""
        if not files:
            return []

        # Only allow for a single file/folder at a time
        if len(files) != 1:
            return []

        file_item = files[0]
        
        # Check that it's a local file
        if file_item.get_uri_scheme() != "file":
            return []

        create_link_item = Nautilus.MenuItem(
            name='CreateLink::create',
            label=TEXTS['create_link'],
            tip=TEXTS['tip_create_link']
        )
        
        create_link_item.connect('activate', self.create_link, file_item)
        return [create_link_item]

    def create_link(self, menu, file_item):
        """Create a symbolic link to the selected file/folder"""
        try:
            # Get source file path
            uri = file_item.get_uri()
            source_path = unquote(uri.replace('file://', ''))
            source_path_obj = Path(source_path)
            
            # Determine parent directory
            parent_dir = source_path_obj.parent
            
            # Create link name
            original_name = source_path_obj.name
            link_name = self.generate_link_name(parent_dir, original_name)
            link_path = parent_dir / link_name
            
            # Create symbolic link
            os.symlink(source_path, str(link_path))
            print(f"✓ Created symbolic link: {link_path} -> {source_path}")
            
        except FileExistsError:
            self.show_error(TEXTS['error_exists'])
        except PermissionError:
            self.show_error(TEXTS['error_permission'])
        except Exception as e:
            print(f"Error creating symbolic link: {e}")
            self.show_error(TEXTS['error_generic'])

    def generate_link_name(self, parent_dir, original_name):
        """Generate a unique name for the link"""
        # Separate name and extension
        path_obj = Path(original_name)
        name_without_ext = path_obj.stem
        extension = path_obj.suffix
        
        # Base name with link suffix
        base_name = name_without_ext + TEXTS['link_suffix']
        link_name = base_name + extension
        
        # Check if name already exists and add number if necessary
        counter = 1
        while (parent_dir / link_name).exists():
            link_name = f"{base_name} ({counter}){extension}"
            counter += 1
            
        return link_name

    def show_error(self, message):
        """Show error message (fallback to console)"""
        print(f"CreateLink Error: {message}")
        # In a more advanced implementation, we could use a notification
        # or GTK dialog box

def main():
    pass

if __name__ == "__main__":
    main()
