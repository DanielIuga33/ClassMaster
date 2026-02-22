import os
import json
from Internal.security.EncryptionManager import EncryptionManager


class RepositoryUser:
    def __init__(self, user_data_path: str, system_key: str = "SYSTEM_ACCESS_KEY"):
        # 1. Inițializăm variabilele
        self.__user_list = []
        self.__filename = None
        self.__system_key = system_key  # Cheia necesară pentru a citi lista de utilizatori

        if user_data_path:
            os.makedirs(user_data_path, exist_ok=True)
            # Schimbăm extensia în .enc
            self.__filename = os.path.join(user_data_path, "Users.enc")

            # 2. Dacă fișierul nu există, îl creăm criptat cu o listă goală
            if not os.path.exists(self.__filename):
                EncryptionManager.encrypt_to_file(self.__filename, [], self.__system_key)

            # 3. Citim datele folosind cheia de sistem
            self.__user_list = self.__read()

    def add_user(self, user):
        if not self.__exist(user):
            self.__user_list.append(user)
            self.__save()  # <--- Important!
            return [201, "CREATED"]
        return [400, "ALREADY EXISTS"]

    def remove_user(self, user):
        if self.__exist(user):
            self.__user_list.remove(user)
            self.__save()  # <--- Important!
            return [200, "OK"]
        return [404, "User not found!"]

    def modify_user(self, user_old, user_new):
        if self.__exist(user_old):
            idx = self.__user_list.index(user_old)
            self.__user_list[idx] = user_new
            self.__save()
            return [200, "OK"]
        return [404, "User not found!"]

    def __exist(self, user):
        for u in self.__user_list:
            if u.get_email() == user.get_email():
                return True
        return False

    def find_by_email(self, email):
        for user in self.__user_list:
            if user.get_email() == email:
                return user
        return None

    def find_by_username(self, username):
        # Presupunem că username-ul este Prenumele
        for user in self.__user_list:
            if user.get_username() == username:
                return user
        return None

    def set_new_path(self, new_data_path: str):
        """Schimbă locația fișierului la înregistrare și păstrează criptarea."""
        try:
            if new_data_path:
                os.makedirs(new_data_path, exist_ok=True)
                # CORECȚIE: Extensia trebuie să fie .enc
                self.__filename = os.path.join(new_data_path, "Users.enc")

                if not os.path.exists(self.__filename):
                    # CORECȚIE: Creăm fișierul criptat, nu JSON
                    EncryptionManager.encrypt_to_file(self.__filename, [], self.__system_key)

                self.__user_list = self.__read()
                return [200, "OK"]
        except Exception as e:  # Catch general pentru erori de permisiuni/OS
            return [404, str(e)]

    def __save(self):
        """Salvează lista de utilizatori în format binar criptat."""
        if not self.__filename:
            return

        temp = []
        for u in self.__user_list:
            temp.append({
                "id_entity": u.get_id_entity(),
                "username": u.get_username(),
                "first_name": u.get_first_name(),
                "last_name": u.get_last_name(),
                "email": u.get_email(),
                "password": u.get_password(),  # Acesta rămâne HASH SHA-256
                "data_path": u.get_data_path(),
                "street_address": u.get_street_address(),
                "city": u.get_city(),
                "state": u.get_state(),
                "birthday": u.get_birthday()
            })

        # Folosim EncryptionManager pentru a scrie fișierul .enc
        EncryptionManager.encrypt_to_file(self.__filename, temp, self.__system_key)

    def __read(self):
        """Decriptează fișierul de utilizatori la pornirea aplicației."""
        if not os.path.exists(self.__filename):
            return []

        # Încercăm decriptarea cu cheia de sistem
        temp = EncryptionManager.decrypt_from_file(self.__filename, self.__system_key)

        if temp is None:
            # Dacă cheia de sistem este greșită, datele sunt inaccesibile
            print("Eroare Critică: Nu s-a putut accesa baza de date de utilizatori.")
            return []

        from Internal.entity.User import User
        return [User(**date) for date in temp]

    def get_all(self):
        return self.__user_list


