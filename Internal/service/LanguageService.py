import json
import os


class LanguageService:
    def __init__(self, settings_service, lang_file="Data/Languages.json"):
        self.settings_service = settings_service
        self.lang_file = lang_file
        self.translations = self._load_translations()

    def _load_translations(self):
        if not os.path.exists(self.lang_file):
            return {}
        with open(self.lang_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_text(self, user_id, key):
        """Returnează traducerea pentru cheia dată."""
        user_lang = self.settings_service.get_user_settings(user_id).get("language", "Română")
        return self.translations.get(user_lang, {}).get(key, key)