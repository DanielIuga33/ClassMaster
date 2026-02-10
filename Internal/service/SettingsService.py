import json
import os


class SettingsService:
    def __init__(self, settings_path="Data/settings.txt"):
        self.__settings_path = settings_path
        # Definim setările implicite
        self.__default_settings = {
            "tema": "light",
            "last_user": "",
            "window_size": "400x500"
        }
        # Încărcăm setările existente la inițializare
        self.settings = self.load_settings()

    def load_settings(self):
        """Citește setările din fișier."""
        if not os.path.exists(self.__settings_path):
            return self.__default_settings.copy()

        try:
            with open(self.__settings_path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return self.__default_settings.copy()

    def save_settings(self, new_settings):
        """Actualizează și salvează setările."""
        self.settings.update(new_settings)
        # Ne asigurăm că folderul Data există
        os.makedirs(os.path.dirname(self.__settings_path), exist_ok=True)

        with open(self.__settings_path, "w") as f:
            json.dump(self.settings, f, indent=4)

    def get_theme(self):
        return self.settings.get("tema", "light")