import os
import json


class RepositoryStudent:
    def __init__(self, user_data_path: str):
        self.__filename = os.path.join(user_data_path, "Students.json")
        # Ne asigurăm că folderul există
        os.makedirs(user_data_path, exist_ok=True)
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

    def __save(self):
        with open(self.__filename, "w") as f:
            # Folosim o metodă mai sigură de a serializa
            # vars(s) e ok, dar e bine să curățăm numele atributelor private dacă apar
            temp = []
            for s in self.__student_list:
                data = {
                    "first_name": s.first_name,
                    "last_name": s.last_name,
                    "grade": s.grade,
                    "price": s.price
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
