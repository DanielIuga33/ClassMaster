import os
import json


class RepositoryStudent:
    def __init__(self, user_data_path: str):
        # 1. Inițializăm ÎNTOTDEAUNA variabilele cu valori sigure la început
        self.__student_list = []
        self.__filename = None  # Folosim None pentru a indica lipsa unei căi

        if user_data_path:
            os.makedirs(user_data_path, exist_ok=True)
            self.__filename = os.path.join(user_data_path, "Students.json")

            # 2. Verificăm dacă fișierul NU există și îl creăm gol
            if not os.path.exists(self.__filename):
                with open(self.__filename, "w") as f:
                    json.dump([], f)

                # 3. Abia acum citim datele
            self.__student_list = self.__read()

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

    def __exist(self, student):
        return student in self.__student_list

    def get_stud_by_id(self, id_stud):
        for student in self.__student_list:
            if student.get_id_entity() == id_stud:
                return student

    def __save(self):
        with open(self.__filename, "w") as f:
            # Folosim o metodă mai sigură de a serializa
            # vars(s) e ok, dar e bine să curățăm numele atributelor private dacă apar
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
            json.dump(temp, f, indent=4)

    def __read(self):
        if not os.path.exists(self.__filename):
            return []
        try:
            with open(self.__filename, "r") as f:
                temp = json.load(f)
                from Internal.entity.Student import Student
                # Reconstruim obiectele
                return [Student(**date) for date in temp]
        except json.JSONDecodeError:
            return []

    def get_all(self):
        return self.__student_list

    def set_new_path(self, new_data_path: str):
        """Schimbă locația fișierului la înregistrare."""
        if new_data_path:
            os.makedirs(new_data_path, exist_ok=True)
            self.__filename = os.path.join(new_data_path, "Students.json")
            # Dacă fișierul nu există în noua locație, îl creăm
            if not os.path.exists(self.__filename):
                with open(self.__filename, "w") as f:
                    json.dump([], f)
            # Reîncărcăm lista din noua locație
            self.__student_list = self.__read()
