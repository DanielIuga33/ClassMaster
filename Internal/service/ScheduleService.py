import json
import os
from Internal.security.EncryptionManager import EncryptionManager


class ScheduleService:
    def __init__(self):
        self.__filename = None
        self.__schedule_data = []
        self.__current_password = None

    def set_schedule_path(self, new_data_path: str, password: str):
        if new_data_path:
            self.__current_password = password
            os.makedirs(new_data_path, exist_ok=True)

            # 1. Schimbăm extensia în .enc
            self.__filename = os.path.join(new_data_path, "Schedule.enc")

            # 2. Dacă nu există, creăm un fișier criptat cu un dicționar gol
            if not os.path.exists(self.__filename):
                EncryptionManager.encrypt_to_file(self.__filename, {}, self.__current_password)

            # 3. Reîncărcăm datele (acum decriptate)
            self.__schedule_data = self.load_schedule_data()

    def load_schedule_data(self):
        if not self.__filename or not os.path.exists(self.__filename):
            return {}  # Returnăm dicționar pentru orar

        # 4. Folosim decriptarea în loc de json.load
        data = EncryptionManager.decrypt_from_file(self.__filename, self.__current_password)

        return data if data is not None else {}

    def get_schedule_data(self):
        return self.__schedule_data

    def save_schedule_data(self):
        if not self.__filename:
            return
        EncryptionManager.encrypt_to_file(self.__filename, self.__schedule_data, self.__current_password)

    def delete_cascade(self, id_group):
        # Facem o listă cu cheile pe care trebuie să le ștergem
        # Nu putem șterge direct din dicționar în timp ce îl parcurgem
        keys_to_delete = []

        current_data = self.get_schedule_data()

        for key, value in current_data.items():
            # Verificăm dacă valoarea este un dicționar și are group_id
            if isinstance(value, dict) and value.get('group_id') == id_group:
                keys_to_delete.append(key)

        # Dacă am găsit ceva de șters
        if keys_to_delete:
            for key in keys_to_delete:
                del self.__schedule_data[key]

            # Salvăm o singură dată la final, nu în interiorul for-ului (pentru performanță)
            self.save_schedule_data()
