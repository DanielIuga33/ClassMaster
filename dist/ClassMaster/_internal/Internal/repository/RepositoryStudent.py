import os
import json
from Internal.security.EncryptionManager import EncryptionManager


class RepositoryStudent:
    def __init__(self, user_data_path: str, session_password: str):
        self.__student_list = []
        self.__filename = None
        # Aceasta este parola în format text clar, venită de la Login
        self.__current_password = session_password

        if user_data_path:
            os.makedirs(user_data_path, exist_ok=True)
            self.__filename = os.path.join(user_data_path, "Students.enc")

            if not os.path.exists(self.__filename):
                # Inițializăm fișierul criptat cu o listă goală []
                EncryptionManager.encrypt_to_file(self.__filename, [], self.__current_password)

            # Citirea va reuși doar dacă session_password este identică
            # cu cea folosită la salvare
            self.__student_list = self.__read(self.__current_password)

    def add_student(self, student):
        if not self.__exist(student):
            self.__student_list.append(student)  # Folosim __student_list
            self.__save()  # SALVĂM PE DISC
            return [201, "CREATED"]
        return [400, "Student already exists"]

    def remove_student(self, student):
        if self.__exist(student):
            self.__student_list.remove(student)
            self.__save()  # SALVĂM PE DISC
            return [200, "OK"]
        return [404, "Student not found!"]

    def modify_student(self, student_old, student_new):
        if self.__exist(student_old):
            # Căutăm indexul pentru a-l înlocui exact în același loc
            index = self.__student_list.index(student_old)
            self.__student_list[index] = student_new
            self.__save()  # SALVĂM PE DISC
            return [200, "OK"]
        return [404, "Student not found!"]


    def size(self):
        return len(self.__student_list)

    def __exist(self, student):
        return student in self.__student_list

    def get_stud_by_id(self, id_stud):
        for student in self.__student_list:
            if student.get_id_entity() == id_stud:
                return student

    def __save(self):
        """Salvează lista de studenți folosind criptarea AES."""
        temp = []
        for s in self.__student_list:
            data = {
                "id_entity": s.get_id_entity(),
                "first_name": s.get_first_name(),
                "last_name": s.get_last_name(),
                "grade": s.get_grade(),
                "price": s.get_price(),
                "teacher_id": s.get_teacher_id(),
            }
            temp.append(data)

        # Folosim managerul în loc de json.dump direct
        EncryptionManager.encrypt_to_file(self.__filename, temp, self.__current_password)

    def __read(self, password):
        """Decriptează datele de pe disc."""
        if not os.path.exists(self.__filename):
            return []

        # Managerul returnează None dacă parola este greșită
        temp = EncryptionManager.decrypt_from_file(self.__filename, password)

        if temp is None:
            # Aici poți ridica o eroare personalizată sau returna listă goală
            # Ideal ar fi ca LoginController să verifice parola înainte
            return []

        from Internal.entity.Student import Student
        return [Student(**date) for date in temp]

    def get_all(self):
        return self.__student_list

    def set_new_path(self, new_data_path: str, password: str):
        """Schimbă locația fișierului și inițializează formatul criptat .enc"""
        if new_data_path:
            # 1. Actualizăm parola în memorie pentru a putea decripta/cripta ulterior
            self.__current_password = password

            # 2. Creăm folderul dacă nu există
            os.makedirs(new_data_path, exist_ok=True)

            # 3. Schimbăm calea către noul fișier binari (.enc)
            self.__filename = os.path.join(new_data_path, "Students.enc")

            # 4. Dacă fișierul NU există în noua locație, îl creăm CRIPTAT
            if not os.path.exists(self.__filename):
                # Salvăm o listă goală [] folosind EncryptionManager
                from Internal.security.EncryptionManager import EncryptionManager
                EncryptionManager.encrypt_to_file(self.__filename, [], self.__current_password)

            # 5. Reîncărcăm lista din noua locație (acum decriptarea va merge)
            self.__student_list = self.__read(self.__current_password)

    def update_encryption_password(self, new_password):
        """
        Re-criptează datele actuale cu o nouă parolă.
        """
        # 1. Actualizăm parola în variabila privată a repository-ului
        self.__current_password = new_password

        # 2. Forțăm o salvare. Metoda __save() va folosi automat
        # noua valoare din self.__current_password pentru criptare.
        self.__save()

