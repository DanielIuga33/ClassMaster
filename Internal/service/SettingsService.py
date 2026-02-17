import json
import os


class SettingsService:
    def __init__(self, settings_path="Data/Settings.json"):
        self.__settings_path = settings_path
        self.__default_user_config = {
            "tema": "light",
            "language": "Romana",
            "rows_count": 5
        }
        self.all_users_settings = self.load_settings()

    def load_settings(self):
        """Citește baza de date de setări de pe disc."""
        if not os.path.exists(self.__settings_path):
            return {}
        try:
            with open(self.__settings_path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def get_user_settings(self, user_id):
        """Reîncarcă setările pentru a asigura sincronizarea între ecrane."""
        self.all_users_settings = self.load_settings()
        return self.all_users_settings.get(user_id, self.__default_user_config.copy())

    def get_theme(self, user_id=None):
        """Detectează tema: ID Utilizator -> Global -> Classic Light."""
        target_id = user_id if user_id and user_id != "global" else "global"
        settings = self.get_user_settings(target_id)
        return settings.get("tema", "light")

    def save_user_setting(self, user_id, key, value):
        """Salvează o setare pe disc și reîncarcă memoria locală."""
        # Ne asigurăm că avem ultimele date înainte de scriere
        self.all_users_settings = self.load_settings()

        if user_id not in self.all_users_settings:
            self.all_users_settings[user_id] = self.__default_user_config.copy()

        self.all_users_settings[user_id][key] = value

        os.makedirs(os.path.dirname(self.__settings_path), exist_ok=True)
        with open(self.__settings_path, "w") as f:
            json.dump(self.all_users_settings, f, indent=4)

        # Sincronizăm memoria locală imediat după salvare
        self.all_users_settings = self.load_settings()

    def get_colors(self, user_id=None):
        """Metodă sigură care returnează întotdeauna un dicționar valid."""
        theme = self.get_theme(user_id)
        colors = self.get_colors_by_name(theme)

        # Dacă tema salvată nu este găsită, forțăm Classic Light
        if colors is None:
            return self.get_colors_by_name("classic_light")
        return colors

    def save_settings(self, user_id, settings_dict):
        """Salvează un dicționar întreg de setări pentru un utilizator."""
        self.all_users_settings = self.load_settings()
        self.all_users_settings[user_id] = settings_dict

        os.makedirs(os.path.dirname(self.__settings_path), exist_ok=True)
        with open(self.__settings_path, "w") as f:
            json.dump(self.all_users_settings, f, indent=4)

        self.all_users_settings = self.load_settings()

    def save_active_days(self, user_id, days_list):
        """Salvează lista zilelor selectate în profilul utilizatorului."""
        settings = self.get_user_settings(user_id)
        settings["active_days"] = days_list
        # Acum apelul de mai jos va funcționa
        self.save_settings(user_id, settings)

    def get_colors_by_name(self, name):
        """Toate temele salvate, actualizate cu 'schedule_text' pentru contrast maxim."""

        # --- TEME DARK (Alb pe fundal închis) ---
        if name == "classic_dark":
            return {
                "bg": "#121212", "sidebar_bg": "#1E1E1E", "fg": "#FFFFFF",
                "card_bg": "#1E1E1E", "input_bg": "#2C2C2C", "hover": "#333333",
                "grid_line": "#333333", "accent": "#4A90E2", "success": "#2ECC71", "danger": "#E74C3C",
                "schedule_text": "#FFFFFF"
            }
        elif name in ["dark_start", "dark"]:
            return {
                "bg": "#18191A", "sidebar_bg": "#242526", "fg": "#E4E6EB",
                "card_bg": "#242526", "input_bg": "#3A3B3C", "hover": "#3E4042",
                "grid_line": "#3E4042", "accent": "#007BFF", "success": "#059669", "danger": "#E74C3C",
                "schedule_text": "#FFFFFF"
            }
        elif name == "dark_emerald":
            return {
                "bg": "#18191A", "sidebar_bg": "#242526", "fg": "#E4E6EB",
                "card_bg": "#242526", "input_bg": "#3A3B3C", "hover": "#3E4042",
                "grid_line": "#3E4042", "accent": "#374151", "success": "#059669", "danger": "#E74C3C",
                "schedule_text": "#FFFFFF"
            }
        elif name == "midnight_blue":
            return {
                "bg": "#0B0E14", "sidebar_bg": "#151921", "fg": "#D1D5DB",
                "card_bg": "#151921", "input_bg": "#1F2937", "hover": "#2D3748",
                "grid_line": "#2D3748", "accent": "#6366F1", "success": "#10B981", "danger": "#EF4444",
                "schedule_text": "#FFFFFF"
            }
        elif name == "dracula":
            return {
                "bg": "#282A36", "sidebar_bg": "#21222C", "fg": "#F8F8F2",
                "card_bg": "#21222C", "input_bg": "#44475A", "hover": "#6272A4",
                "grid_line": "#44475A", "accent": "#BD93F9", "success": "#50FA7B", "danger": "#FF5555",
                "schedule_text": "#FFFFFF"
            }
        elif name == "tokyo_night":
            return {
                "bg": "#1A1B26", "sidebar_bg": "#16161E", "fg": "#A9B1D6",
                "card_bg": "#16161E", "input_bg": "#24283B", "hover": "#292E42",
                "grid_line": "#292E42", "accent": "#7AA2F7", "success": "#9ECE6A", "danger": "#F7768E",
                "schedule_text": "#FFFFFF"
            }
        elif name == "cyberpunk":
            return {
                "bg": "#000505", "sidebar_bg": "#000000", "fg": "#00FF9F",
                "card_bg": "#0D0D0D", "input_bg": "#1A1A1A", "hover": "#333333",
                "grid_line": "#00FF9F", "accent": "#FF0055", "success": "#00FF9F", "danger": "#FFFF00",
                "schedule_text": "#FFFFFF"
            }
        elif name == "material_ocean":
            return {
                "bg": "#0F111A", "sidebar_bg": "#090B10", "fg": "#8F93A2",
                "card_bg": "#090B10", "input_bg": "#1A1C25", "hover": "#24262E",
                "grid_line": "#1A1C25", "accent": "#82AAFF", "success": "#C3E88D", "danger": "#FF5370",
                "schedule_text": "#FFFFFF", "schedule_text_1": "#000000"
            }
        elif name == "mocha_dark":
            return {
                "bg": "#1E1815", "sidebar_bg": "#2D241E", "fg": "#D4BEB2",
                "card_bg": "#2D241E", "input_bg": "#3D3129", "hover": "#4D3F35",
                "grid_line": "#4D3F35", "accent": "#A67C52", "success": "#829460", "danger": "#B25068",
                "schedule_text": "#FFFFFF"
            }
        elif name == "forest_dark":
            return {
                "bg": "#0D1111", "sidebar_bg": "#161B1B", "fg": "#ECF1F1",
                "card_bg": "#161B1B", "input_bg": "#232A2A", "hover": "#2D3737",
                "grid_line": "#2D3737", "accent": "#00B894", "success": "#55E6C1", "danger": "#FC427B",
                "schedule_text": "#FFFFFF"
            }
        elif name == "dark_oled":
            return {
                "bg": "#000000", "sidebar_bg": "#000000", "fg": "#FFFFFF",
                "card_bg": "#121212", "input_bg": "#1A1A1A", "hover": "#222222",
                "grid_line": "#333333", "accent": "#BB86FC", "success": "#03DAC6", "danger": "#CF6679",
                "schedule_text": "#FFFFFF"
            }

        # --- TEME LIGHT (Negru pe fundal deschis) ---
        elif name in ["classic_light", "light"]:
            return {
                "bg": "#F8F9FA", "sidebar_bg": "#FFFFFF", "fg": "#2D3436",
                "card_bg": "#FFFFFF", "input_bg": "#F0F2F5", "hover": "#EEEEEE",
                "grid_line": "#D1D8E0", "accent": "#4A90E2", "success": "#2ECC71", "danger": "#E74C3C",
                "schedule_text": "#000000"
            }
        elif name == "nordic_frost":
            return {
                "bg": "#F3F9FB", "sidebar_bg": "#E1EBF2", "fg": "#2C3E50",
                "card_bg": "#FFFFFF", "input_bg": "#E1EBF2", "hover": "#D1DEE8",
                "grid_line": "#CAD6E0", "accent": "#3498DB", "success": "#27AE60", "danger": "#E74C3C",
                "schedule_text": "#000000"
            }
        elif name == "github_light":
            return {
                "bg": "#FFFFFF", "sidebar_bg": "#F6F8FA", "fg": "#24292F",
                "card_bg": "#FFFFFF", "input_bg": "#F6F8FA", "hover": "#F3F4F6",
                "grid_line": "#D0D7DE", "accent": "#0969DA", "success": "#1A7F37", "danger": "#CF222E",
                "schedule_text": "#000000"
            }
        elif name == "solarized_light":
            return {
                "bg": "#FDF6E3", "sidebar_bg": "#EEE8D5", "fg": "#657B83",
                "card_bg": "#FCF9ED", "input_bg": "#EEE8D5", "hover": "#E5DFCC",
                "grid_line": "#D5D0BA", "accent": "#268BD2", "success": "#859900", "danger": "#DC322F",
                "schedule_text": "#000000"
            }
        elif name == "light_soft":
            return {
                "bg": "#FDF6E3", "sidebar_bg": "#EEE8D5", "fg": "#586E75",
                "card_bg": "#FDF6E3", "input_bg": "#EEE8D5", "hover": "#E0D9C1",
                "grid_line": "#D5D0BA", "accent": "#B58900", "success": "#859900", "danger": "#DC322F",
                "schedule_text": "#000000"
            }

        return None
