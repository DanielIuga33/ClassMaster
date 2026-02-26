import json
import os
import sys
from Internal.utils.utils import get_colors_by_name


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class SettingsService:
    def __init__(self):
        self.__settings_path = None
        self.__default_user_config = {
            "tema": "light",
            "language": "en",
            "rows_count": 5
        }
        self.__global_settings_path = resource_path("Internal/Resources/Settings.json")
        self.all_users_settings = self.load_settings()

    def load_settings(self):
        # Folosește calea calculată prin resource_path
        path_to_open = self.__settings_path if self.__settings_path and os.path.exists(
            self.__settings_path) else self.__global_settings_path

        try:
            with open(path_to_open, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def set_settings_path(self, new_data_path: str):
        if new_data_path:
            os.makedirs(new_data_path, exist_ok=True)
            self.__settings_path = os.path.join(new_data_path, "Settings.json")
            # Dacă fișierul nu există în noua locație, îl creăm
            if not os.path.exists(self.__settings_path):
                with open(self.__settings_path, "w") as f:
                    json.dump({}, f)
            # Reîncărcăm lista din noua locație
            self.all_users_settings = self.load_settings()

    def get_user_settings(self, user_id):
        if user_id == "global":
            try:
                with open(self.__global_settings_path, "r") as f:
                    return json.load(f)
            except:
                return self.__default_user_config.copy()

        self.all_users_settings = self.load_settings()
        return self.all_users_settings.get(user_id, self.__default_user_config.copy())

    def get_theme(self, user_id=None):
        """Detectează tema: ID Utilizator -> Global -> Classic Light."""
        target_id = user_id if user_id and user_id != "global" else "global"
        settings = self.get_user_settings(target_id)
        return settings.get("tema", "light")

    def save_user_setting(self, user_id, key, value):
        self.all_users_settings = self.load_settings()

        if user_id not in self.all_users_settings:
            self.all_users_settings[user_id] = self.__default_user_config.copy()

        self.all_users_settings[user_id][key] = value
        if not self.__settings_path:
            self.__settings_path = "Internal/Resources/Settings.json"
        if user_id == "global":
            self.save_for_global(key, value)
        os.makedirs(os.path.dirname(self.__settings_path), exist_ok=True)
        with open(self.__settings_path, "w") as f:
            json.dump(self.all_users_settings, f, indent=4)
        # Sincronizăm memoria locală imediat după salvare
        self.all_users_settings = self.load_settings()

    def save_for_global(self, key, value):
        # Folosim variabila care conține resource_path
        path = self.__global_settings_path

        os.makedirs(os.path.dirname(path), exist_ok=True)

        # 1. Citire sigură
        global_user = {}
        if os.path.exists(path) and os.path.getsize(path) > 0:
            try:
                with open(path, "r") as f:
                    global_user = json.load(f)
            except json.JSONDecodeError:
                global_user = {}  # Dacă e corupt sau gol, începem de la zero

        # 2. Modificare
        global_user[key] = value

        # 3. Salvare sigură
        with open(path, "w") as f:
            json.dump(global_user, f, indent=4)

    def get_colors(self, user_id=None):
        """Metodă sigură care returnează întotdeauna un dicționar valid."""
        theme = self.get_theme(user_id)
        colors = get_colors_by_name(theme)

        # Dacă tema salvată nu este găsită, forțăm Classic Light
        if colors is None:
            return get_colors_by_name("classic_light")
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
