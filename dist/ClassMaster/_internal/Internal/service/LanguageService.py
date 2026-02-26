import json
import os


class LanguageService:
    def __init__(self, settings_service):
        self.settings_service = settings_service
        current_dir = os.path.dirname(os.path.abspath(__file__))
        internal_dir = os.path.dirname(current_dir)
        self.lang_file = os.path.join(internal_dir, 'Resources', 'translations.json')

        self.translations = self._load_translations()

    def _load_translations(self):
        if not os.path.exists(self.lang_file):
            print(f"ATENȚIE: Fișierul de limbi nu a fost găsit la: {self.lang_file}")
            return {}

        try:
            with open(self.lang_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Eroare la citirea fișierului JSON: {e}")
            return {}

    def get_text(self, user_id, key):
        user_settings = self.settings_service.get_user_settings(user_id)
        raw_lang = user_settings.get("language", "ro")
        lang_mapping = {
            "Română": "ro",
            "English": "en",
            "ro": "ro",
            "en": "en"
        }
        user_lang = lang_mapping.get(raw_lang, "ro")
        lang_dict = self.translations.get(user_lang, {})
        return lang_dict.get(key, key)
