import os
from Internal.entity.Preset import Preset
from Internal.security.EncryptionManager import EncryptionManager  # Importul necesar


class RepositoryPreset:
    def __init__(self, user_data_path: str, session_password: str):
        self.__preset_list = []
        self.__filename = None
        # Păstrăm parola de sesiune în RAM pentru criptare/decriptare
        self.__current_password = session_password

        if user_data_path:
            os.makedirs(user_data_path, exist_ok=True)
            # Schimbăm extensia în .enc
            self.__filename = os.path.join(user_data_path, "Presets.enc")

            # Creăm fișierul criptat dacă nu există
            if not os.path.exists(self.__filename):
                EncryptionManager.encrypt_to_file(self.__filename, [], self.__current_password)

            self.__preset_list = self.__read()

    def add_preset(self, preset):
        if not self.__exist(preset):
            self.__preset_list.append(preset)
            self.__save()
            return [201, "CREATED"]
        return [400, "Preset name already exists for this teacher"]

    def remove_preset(self, preset):
        if self.__exist(preset):
            self.__preset_list.remove(preset)
            self.__save()
            return [200, "OK"]
        return [404, "Preset not found!"]

    def __exist(self, preset):
        for p in self.__preset_list:
            if p.get_name() == preset.get_name() and p.get_teacher_id() == preset.get_teacher_id():
                return True
        return False

    def get_presets_by_teacher(self, teacher_id):
        return [p for p in self.__preset_list if p.get_teacher_id() == teacher_id]

    def __save(self):
        """Salvează presetările folosind criptarea AES."""
        if not self.__filename:
            return

        temp = []
        for p in self.__preset_list:
            data = {
                "id_entity": p.get_id_entity(),
                "teacher_id": p.get_teacher_id(),
                "name": p.get_name(),
                "data": p.get_data()
            }
            temp.append(data)

        # Folosim managerul de criptare în loc de json.dump
        EncryptionManager.encrypt_to_file(self.__filename, temp, self.__current_password)

    def __read(self):
        """Decriptează datele binare înapoi în obiecte Preset."""
        if not self.__filename or not os.path.exists(self.__filename):
            return []

        # Managerul returnează None dacă decriptarea eșuează (parolă greșită)
        temp = EncryptionManager.decrypt_from_file(self.__filename, self.__current_password)

        if temp is None:
            return []

        return [Preset(**date) for date in temp]

    def get_all(self):
        return self.__preset_list

    def set_new_path(self, new_data_path: str, password: str):  # Adăugăm password ca argument
        """Schimbă locația fișierului la înregistrare și menține formatul criptat."""
        if new_data_path:
            # 1. Actualizăm parola în memorie pentru acest repository
            self.__current_password = password

            # 2. Asigurăm existența folderului
            os.makedirs(new_data_path, exist_ok=True)

            # 3. Setăm calea către fișierul .enc
            self.__filename = os.path.join(new_data_path, "Presets.enc")

            # 4. Dacă fișierul nu există, îl creăm criptat cu parola primită
            if not os.path.exists(self.__filename):
                # Asigură-te că EncryptionManager este importat la începutul fișierului
                EncryptionManager.encrypt_to_file(self.__filename, [], self.__current_password)

            # 5. Reîncărcăm lista de presetări (metoda __read va folosi noua parolă)
            self.__preset_list = self.__read()

    def update_encryption_password(self, new_password):
        """
        Re-criptează datele actuale cu o nouă parolă.
        """
        # 1. Actualizăm parola în variabila privată a repository-ului
        self.__current_password = new_password

        # 2. Forțăm o salvare. Metoda __save() va folosi automat
        # noua valoare din self.__current_password pentru criptare.
        self.__save()
