import json
import os


class SettingsService:
    def __init__(self, settings_path="Data/settings.txt"):
        self.__settings_path = settings_path
        self.__default_settings = {
            "tema": "light",
            "last_user": "",
            "window_size": "400x500"
        }
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
        os.makedirs(os.path.dirname(self.__settings_path), exist_ok=True)
        with open(self.__settings_path, "w") as f:
            json.dump(self.settings, f, indent=4)

    def get_theme(self):
        return self.settings.get("tema", "light")

    # --- LOGICA DE TEMĂ CENTRALIZATĂ ---
    def get_colors(self):
        """Returnează paleta de culori în funcție de temă."""
        theme = self.get_theme()

        if theme == "dark":
            return {
                "bg": "#121212",
                "sidebar_bg": "#1E1E1E",
                "fg": "#FFFFFF",
                "card_bg": "#1E1E1E",
                "input_bg": "#2C2C2C",  # Gri închis pentru input-uri în Dark Mode
                "hover": "#333333",
                "grid_line": "#333333",
                "accent": "#4A90E2",
                "success": "#2ECC71",
                "danger": "#E74C3C"
            }

        # Tema Light cu fundalul de input gri-deschis solicitat
        return {
            "bg": "#F8F9FA",
            "sidebar_bg": "#FFFFFF",
            "fg": "#2D3436",
            "card_bg": "#FFFFFF",
            "input_bg": "#F0F2F5",  # Nuanța de gri pentru vizibilitate sporită
            "hover": "#EEEEEE",
            "grid_line": "#D1D8E0",  # Liniile tabelului pe care le-am discutat
            "accent": "#4A90E2",
            "success": "#2ECC71",
            "danger": "#E74C3C"
        }