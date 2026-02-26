import os
from Internal.entity.Group import Group
from Internal.security.EncryptionManager import EncryptionManager


class RepositoryGroup:
    def __init__(self, user_data_path: str, session_password: str):
        # 1. Inițializăm variabilele
        self.__group_list = []
        self.__filename = None
        self.__current_password = session_password  # Parola din RAM

        if user_data_path:
            os.makedirs(user_data_path, exist_ok=True)
            # Modificăm extensia în .enc
            self.__filename = os.path.join(user_data_path, "Groups.enc")

            # 2. Dacă fișierul nu există, îl creăm criptat cu o listă goală
            if not os.path.exists(self.__filename):
                EncryptionManager.encrypt_to_file(self.__filename, [], self.__current_password)

            # 3. Citim datele folosind decriptarea
            self.__group_list = self.__read()

    def __read(self):
        """Decriptează fișierul binar în obiecte Group."""
        if not self.__filename or not os.path.exists(self.__filename):
            return []

        # Managerul returnează None dacă parola e greșită
        temp = EncryptionManager.decrypt_from_file(self.__filename, self.__current_password)

        if temp is None:
            return []

        # Reconstruim obiectele folosind datele decriptate
        return [Group(**date) for date in temp]

    def __save(self):
        """Salvează grupele folosind criptarea AES."""
        if not self.__filename:
            return

        temp = []
        for g in self.__group_list:
            data = {
                "id_entity": g.get_id_entity(),
                "group_name": g.get_group_name(),
                "student_ids": g.get_student_ids(),
                "day": g.get_day(),
                "time_interval": g.get_time_interval(),
                "teacher_id": g.get_teacher_id(),
            }
            temp.append(data)

        # Scriem binar pe disc via EncryptionManager
        EncryptionManager.encrypt_to_file(self.__filename, temp, self.__current_password)

    # --- Metodele de business rămân identice, ele apelează self.__save() care e acum securizată ---
    def add_or_update_group(self, cell_id, group_obj):
        self.__group_list[cell_id] = group_obj
        self.__save()

    def add_group(self, name, ids, teacher_id):
        self.__group_list.append(Group(group_name=name, student_ids=ids, day="", time_interval="",
                                       teacher_id=teacher_id, ))
        self.__save()

    def find_by_id(self, id_group):
        for g in self.__group_list:
            if g.get_id_entity() == id_group:
                return g
        return None

    def delete_group(self, cell_id):
        group = self.find_by_id(cell_id)
        if group:
            self.__group_list.remove(group)
            self.__save()

    def modify_group(self, group_old, group_new):
        if group_old in self.__group_list:
            self.__group_list.remove(group_old)
            self.__group_list.append(group_new)
            self.__save()

    def get_all(self):
        return self.__group_list

    def size(self):
        return len(self.__group_list)

    def set_new_path(self, new_data_path: str, password: str):
        if new_data_path:
            # Aici salvăm parola primită de la login!
            self.__current_password = password

            os.makedirs(new_data_path, exist_ok=True)
            self.__filename = os.path.join(new_data_path, "Groups.enc")

            # Acum, când apelăm encrypt_to_file, self.__current_password nu mai este None
            if not os.path.exists(self.__filename):
                EncryptionManager.encrypt_to_file(self.__filename, [], self.__current_password)

            self.__group_list = self.__read()

    def update_encryption_password(self, new_password):
        """
        Re-criptează datele actuale cu o nouă parolă.
        """
        # 1. Actualizăm parola în variabila privată a repository-ului
        self.__current_password = new_password

        # 2. Forțăm o salvare. Metoda __save() va folosi automat
        # noua valoare din self.__current_password pentru criptare.
        self.__save()
