import os
import json
from Internal.entity.Preset import Preset


class RepositoryPreset:
    def __init__(self, user_data_path: str):
        self.__preset_list = []
        self.__filename = None

        if user_data_path:
            os.makedirs(user_data_path, exist_ok=True)
            self.__filename = os.path.join(user_data_path, "Presets.json")

            # Creăm fișierul dacă nu există
            if not os.path.exists(self.__filename):
                with open(self.__filename, "w") as f:
                    json.dump([], f)

            self.__preset_list = self.__read()

    def add_preset(self, preset):
        """Adaugă un preset nou în listă și salvează pe disc."""
        if not self.__exist(preset):
            self.__preset_list.append(preset)
            self.__save()
            return [201, "CREATED"]
        return [400, "Preset name already exists for this teacher"]

    def remove_preset(self, preset):
        """Șterge un preset existent."""
        if self.__exist(preset):
            self.__preset_list.remove(preset)
            self.__save()
            return [200, "OK"]
        return [404, "Preset not found!"]

    def __exist(self, preset):
        """Verifică dacă un preset cu același nume există deja pentru același profesor."""
        for p in self.__preset_list:
            if p.get_name() == preset.get_name() and p.get_teacher_id() == preset.get_teacher_id():
                return True
        return False

    def get_presets_by_teacher(self, teacher_id):
        """Returnează doar preset-urile aparținând unui anumit profesor."""
        return [p for p in self.__preset_list if p.get_teacher_id() == teacher_id]

    def __save(self):
        """Serializarea obiectelor Preset în format JSON."""
        with open(self.__filename, "w") as f:
            temp = []
            for p in self.__preset_list:
                data = {
                    "id_entity": p.get_id_entity(),
                    "teacher_id": p.get_teacher_id(),
                    "name": p.get_name(),
                    "data": p.get_data()  # Dicționarul cu celulele orarului
                }
                temp.append(data)
            json.dump(temp, f, indent=4)

    def __read(self):
        """Deserializarea datelor din JSON în obiecte de tip Preset."""
        if not os.path.exists(self.__filename):
            return []
        try:
            with open(self.__filename, "r") as f:
                temp = json.load(f)
                return [Preset(**date) for date in temp]
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def get_all(self):
        return self.__preset_list

    def set_new_path(self, new_data_path: str):
        """Schimbă locația fișierului la înregistrare."""
        if new_data_path:
            os.makedirs(new_data_path, exist_ok=True)
            self.__filename = os.path.join(new_data_path, "Presets.json")
            # Dacă fișierul nu există în noua locație, îl creăm
            if not os.path.exists(self.__filename):
                with open(self.__filename, "w") as f:
                    json.dump([], f)
            # Reîncărcăm lista din noua locație
            self.__preset_list = self.__read()
