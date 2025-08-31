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

# Dictionnaire des traductions
TRANSLATIONS = {
    'en': {
        'create_link': 'Create Link',
        'tip_create_link': 'Create a symbolic link to the selected item',
        'link_suffix': ' - Link',
        'error_title': 'Error Creating Link',
        'error_exists': 'A file with this name already exists',
        'error_permission': 'Permission denied',
        'error_generic': 'Failed to create symbolic link'
    },
    'fr': {
        'create_link': 'Créer un lien',
        'tip_create_link': 'Créer un lien symbolique vers l\'élément sélectionné',
        'link_suffix': ' - Lien',
        'error_title': 'Erreur lors de la création du lien',
        'error_exists': 'Un fichier avec ce nom existe déjà',
        'error_permission': 'Permission refusée',
        'error_generic': 'Échec de la création du lien symbolique'
    },
    'de': {
        'create_link': 'Link erstellen',
        'tip_create_link': 'Einen symbolischen Link zum ausgewählten Element erstellen',
        'link_suffix': ' - Link',
        'error_title': 'Fehler beim Erstellen des Links',
        'error_exists': 'Eine Datei mit diesem Namen existiert bereits',
        'error_permission': 'Zugriff verweigert',
        'error_generic': 'Fehler beim Erstellen des symbolischen Links'
    },
    'nl': {
        'create_link': 'Link maken',
        'tip_create_link': 'Een symbolische link naar het geselecteerde item maken',
        'link_suffix': ' - Link',
        'error_title': 'Fout bij maken van link',
        'error_exists': 'Een bestand met deze naam bestaat al',
        'error_permission': 'Toegang geweigerd',
        'error_generic': 'Fout bij maken van symbolische link'
    },
    'pl': {
        'create_link': 'Utwórz link',
        'tip_create_link': 'Utwórz dowiązanie symboliczne do wybranego elementu',
        'link_suffix': ' - Link',
        'error_title': 'Błąd tworzenia linku',
        'error_exists': 'Plik o tej nazwie już istnieje',
        'error_permission': 'Brak uprawnień',
        'error_generic': 'Nie udało się utworzyć dowiązania symbolicznego'
    },
    'it': {
        'create_link': 'Crea collegamento',
        'tip_create_link': 'Crea un collegamento simbolico all\'elemento selezionato',
        'link_suffix': ' - Collegamento',
        'error_title': 'Errore nella creazione del collegamento',
        'error_exists': 'Esiste già un file con questo nome',
        'error_permission': 'Permesso negato',
        'error_generic': 'Impossibile creare il collegamento simbolico'
    },
    'es': {
        'create_link': 'Crear enlace',
        'tip_create_link': 'Crear un enlace simbólico al elemento seleccionado',
        'link_suffix': ' - Enlace',
        'error_title': 'Error al crear enlace',
        'error_exists': 'Ya existe un archivo con este nombre',
        'error_permission': 'Permiso denegado',
        'error_generic': 'Error al crear el enlace simbólico'
    },
    'ja': {
        'create_link': 'リンクを作成',
        'tip_create_link': '選択したアイテムへのシンボリックリンクを作成',
        'link_suffix': ' - リンク',
        'error_title': 'リンク作成エラー',
        'error_exists': 'この名前のファイルは既に存在します',
        'error_permission': 'アクセス拒否',
        'error_generic': 'シンボリックリンクの作成に失敗しました'
    },
    'pt': {
        'create_link': 'Criar link',
        'tip_create_link': 'Criar um link simbólico para o item selecionado',
        'link_suffix': ' - Link',
        'error_title': 'Erro ao criar link',
        'error_exists': 'Um arquivo com este nome já existe',
        'error_permission': 'Permissão negada',
        'error_generic': 'Falha ao criar link simbólico'
    },
    'ar': {
        'create_link': 'إنشاء رابط',
        'tip_create_link': 'إنشاء رابط رمزي للعنصر المحدد',
        'link_suffix': ' - رابط',
        'error_title': 'خطأ في إنشاء الرابط',
        'error_exists': 'يوجد ملف بهذا الاسم بالفعل',
        'error_permission': 'تم رفض الإذن',
        'error_generic': 'فشل في إنشاء الرابط الرمزي'
    },
    'tr': {
        'create_link': 'Bağlantı oluştur',
        'tip_create_link': 'Seçilen öğeye sembolik bağlantı oluştur',
        'link_suffix': ' - Bağlantı',
        'error_title': 'Bağlantı oluşturma hatası',
        'error_exists': 'Bu isimde bir dosya zaten var',
        'error_permission': 'İzin reddedildi',
        'error_generic': 'Sembolik bağlantı oluşturulamadı'
    },
    'sv': {
        'create_link': 'Skapa länk',
        'tip_create_link': 'Skapa en symbolisk länk till det valda objektet',
        'link_suffix': ' - Länk',
        'error_title': 'Fel vid skapande av länk',
        'error_exists': 'En fil med detta namn finns redan',
        'error_permission': 'Åtkomst nekad',
        'error_generic': 'Misslyckades att skapa symbolisk länk'
    },
    'hi': {
        'create_link': 'लिंक बनाएं',
        'tip_create_link': 'चयनित आइटम के लिए एक सिंबॉलिक लिंक बनाएं',
        'link_suffix': ' - लिंक',
        'error_title': 'लिंक बनाने में त्रुटि',
        'error_exists': 'इस नाम की फाइल पहले से मौजूद है',
        'error_permission': 'अनुमति अस्वीकृत',
        'error_generic': 'सिंबॉलिक लिंक बनाने में विफल'
    },
    'ko': {
        'create_link': '링크 생성',
        'tip_create_link': '선택한 항목에 대한 심볼릭 링크 생성',
        'link_suffix': ' - 링크',
        'error_title': '링크 생성 오류',
        'error_exists': '이 이름의 파일이 이미 존재합니다',
        'error_permission': '권한 거부됨',
        'error_generic': '심볼릭 링크 생성에 실패했습니다'
    },
    'zh-cn': {
        'create_link': '创建链接',
        'tip_create_link': '为选定项目创建符号链接',
        'link_suffix': ' - 链接',
        'error_title': '创建链接错误',
        'error_exists': '已存在此名称的文件',
        'error_permission': '权限被拒绝',
        'error_generic': '创建符号链接失败'
    },
    'zh-tw': {
        'create_link': '建立連結',
        'tip_create_link': '為選定項目建立符號連結',
        'link_suffix': ' - 連結',
        'error_title': '建立連結錯誤',
        'error_exists': '已存在此名稱的檔案',
        'error_permission': '權限被拒絕',
        'error_generic': '建立符號連結失敗'
    },
    'ru': {
        'create_link': 'Создать ссылку',
        'tip_create_link': 'Создать символическую ссылку на выбранный элемент',
        'link_suffix': ' - Ссылка',
        'error_title': 'Ошибка создания ссылки',
        'error_exists': 'Файл с таким именем уже существует',
        'error_permission': 'Доступ запрещен',
        'error_generic': 'Не удалось создать символическую ссылку'
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
            elif lang_lower.startswith('ko'):
                return 'ko'
            elif lang_lower.startswith('pl'):
                return 'pl'
            elif lang_lower.startswith('pt'):
                return 'pt'
            elif lang_lower.startswith('ar'):
                return 'ar'
            elif lang_lower.startswith('tr'):
                return 'tr'
            elif lang_lower.startswith('sv'):
                return 'sv'
            elif lang_lower.startswith('hi'):
                return 'hi'
    except Exception as e:
        print(f"Error detecting language: {e}")

    return 'en'  # Par défaut anglais

class CreateLinkExtension(GObject.GObject, Nautilus.MenuProvider):

    def __init__(self):
        super().__init__()
        self.current_language = get_system_language()
        self.translations = TRANSLATIONS.get(self.current_language, TRANSLATIONS['en'])

    def get_file_items(self, files):
        """Crée le menu Create Link"""
        if not files:
            return []

        # Ne permettre que pour un seul fichier/dossier à la fois
        if len(files) != 1:
            return []

        file_item = files[0]
        
        # Vérifier que c'est un fichier local
        if file_item.get_uri_scheme() != "file":
            return []

        create_link_item = Nautilus.MenuItem(
            name='CreateLink::create',
            label=self.translations['create_link'],
            tip=self.translations['tip_create_link']
        )
        
        create_link_item.connect('activate', self.create_link, file_item)
        return [create_link_item]

    def create_link(self, menu, file_item):
        """Crée un lien symbolique vers le fichier/dossier sélectionné"""
        try:
            # Obtenir le chemin du fichier source
            uri = file_item.get_uri()
            source_path = unquote(uri.replace('file://', ''))
            source_path_obj = Path(source_path)
            
            # Déterminer le répertoire parent
            parent_dir = source_path_obj.parent
            
            # Créer le nom du lien
            original_name = source_path_obj.name
            link_name = self.generate_link_name(parent_dir, original_name)
            link_path = parent_dir / link_name
            
            # Créer le lien symbolique
            os.symlink(source_path, str(link_path))
            print(f"✓ Created symbolic link: {link_path} -> {source_path}")
            
        except FileExistsError:
            self.show_error(self.translations['error_exists'])
        except PermissionError:
            self.show_error(self.translations['error_permission'])
        except Exception as e:
            print(f"Error creating symbolic link: {e}")
            self.show_error(self.translations['error_generic'])

    def generate_link_name(self, parent_dir, original_name):
        """Génère un nom unique pour le lien"""
        # Séparer le nom et l'extension
        path_obj = Path(original_name)
        name_without_ext = path_obj.stem
        extension = path_obj.suffix
        
        # Nom de base avec le suffixe de lien
        base_name = name_without_ext + self.translations['link_suffix']
        link_name = base_name + extension
        
        # Vérifier si le nom existe déjà et ajouter un numéro si nécessaire
        counter = 1
        while (parent_dir / link_name).exists():
            link_name = f"{base_name} ({counter}){extension}"
            counter += 1
            
        return link_name

    def show_error(self, message):
        """Affiche un message d'erreur (fallback vers la console)"""
        print(f"CreateLink Error: {message}")
        # Dans une implémentation plus avancée, on pourrait utiliser une notification
        # ou une boîte de dialogue GTK

def main():
    pass

if __name__ == "__main__":
    main()

