import os
import json


class RepositoryUser:
    def __init__(self, user_data_path: str):
        # 1. Inițializăm ÎNTOTDEAUNA variabilele cu valori sigure la început
        self.__user_list = []
        self.__filename = None  # Folosim None pentru a indica lipsa unei căi

        if user_data_path:
            os.makedirs(user_data_path, exist_ok=True)
            self.__filename = os.path.join(user_data_path, "Users.json")

            # 2. Verificăm dacă fișierul NU există și îl creăm gol
            if not os.path.exists(self.__filename):
                with open(self.__filename, "w") as f:
                    json.dump([], f)

                # 3. Abia acum citim datele
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
        """Schimbă locația fișierului la înregistrare."""
        if new_data_path:
            os.makedirs(new_data_path, exist_ok=True)
            self.__filename = os.path.join(new_data_path, "Users.json")
            # Dacă fișierul nu există în noua locație, îl creăm
            if not os.path.exists(self.__filename):
                with open(self.__filename, "w") as f:
                    json.dump([], f)
            # Reîncărcăm lista din noua locație
            self.__user_list = self.__read()

    def __save(self):
        # Verificăm dacă avem o cale validă înainte de a deschide fișierul
        if not self.__filename:
            print("Eroare: Calea către Users.json nu a fost configurată!")
            return

        with open(self.__filename, "w") as f:
            temp = []
            for u in self.__user_list:
                temp.append({
                    "id_entity": u.get_id_entity(),
                    "username": u.get_username(),
                    "first_name": u.get_first_name(),
                    "last_name": u.get_last_name(),
                    "email": u.get_email(),
                    "password": u.get_password(),
                    "data_path": u.get_data_path(),
                    "street_address": u.get_street_address(),
                    "city": u.get_city(),
                    "state": u.get_state(),
                    "birthday": u.get_birthday()
                })
            json.dump(temp, f, indent=4)

    def __read(self):
        if not os.path.exists(self.__filename):
            return []
        try:
            with open(self.__filename, "r") as f:
                temp = json.load(f)
                from Internal.entity.User import User
                # Folosim unpacking (**) pentru a recrea obiectele
                return [User(**date) for date in temp]
        except json.JSONDecodeError:
            return []

    def get_all(self):
        return self.__user_list
