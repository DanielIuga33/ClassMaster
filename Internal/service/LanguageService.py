import json
import os


class LanguageService:
    def __init__(self, settings_service):
        self.settings_service = settings_service

        # --- CALCULARE CALE DINAMICĂ ---
        # __file__ este calea către acest script (Internal/service/LanguageService.py)
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Urcăm un nivel din 'service' în 'Internal'
        internal_dir = os.path.dirname(current_dir)

        # Construim calea către Internal/Resources/translations.json
        self.lang_file = os.path.join(internal_dir, 'Resources', 'translations.json')

        self.translations = self._load_translations()

    def _load_translations(self):
        """Încarcă fișierul JSON cu encodare UTF-8 pentru diacritice."""
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
        """Returnează traducerea, gestionând conversia de la nume lung la cod scurt."""
        user_settings = self.settings_service.get_user_settings(user_id)
        raw_lang = user_settings.get("language", "ro")

        # Mapare pentru a asigura compatibilitatea cu interfața de setări
        lang_mapping = {
            "Română": "ro",
            "English": "en",
            "ro": "ro",
            "en": "en"
        }

        # Convertim valoarea sau folosim 'ro' implicit dacă nu există în mapare
        user_lang = lang_mapping.get(raw_lang, "ro")

        # Extragem dicționarul pentru limba respectivă
        lang_dict = self.translations.get(user_lang, {})

        # Debug opțional: elimină după ce verifici că funcționează
        # print(f"DEBUG: Caut '{key}' în '{user_lang}'. Rezultat: {lang_dict.get(key, 'NOT FOUND')}")

        return lang_dict.get(key, key)