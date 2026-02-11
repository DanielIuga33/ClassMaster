import json
import os
from Internal.entity.Group import Group


class RepositoryGroup:
    def __init__(self, user_data_path: str):
        # 1. Inițializăm ÎNTOTDEAUNA variabilele cu valori sigure la început
        self.__group_list = []
        self.__filename = None  # Folosim None pentru a indica lipsa unei căi

        if user_data_path:
            os.makedirs(user_data_path, exist_ok=True)
            self.__filename = os.path.join(self.__user_data_path, "Groups.json")

            # 2. Verificăm dacă fișierul NU există și îl creăm gol
            if not os.path.exists(self.__filename):
                with open(self.__filename, "w") as f:
                    json.dump([], f)

                # 3. Abia acum citim datele
            self.__group_list = self.__read()

    def __read(self):
        if not os.path.exists(self.__filename):
            return []
        try:
            with open(self.__filename, "r") as f:
                temp = json.load(f)
                from Internal.entity.Student import Student
                # Reconstruim obiectele
                return [Group(**date) for date in temp]
        except json.JSONDecodeError:
            return []

    def __save(self):
        with open(self.__filename, "w") as f:
            # Folosim o metodă mai sigură de a serializa
            # vars(s) e ok, dar e bine să curățăm numele atributelor private dacă apar
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
            json.dump(temp, f, indent=4)

    def add_or_update_group(self, cell_id, group_obj):
        self.__group_list[cell_id] = group_obj
        self.__save()

    def add_group(self, name, ids, teacher_id):
        self.__group_list.append(Group(group_name=name, student_ids=ids, day="", time_interval="",
                                       teacher_id=teacher_id,))
        self.__save()

    def find_by_id(self, id_group):
        for g in self.__group_list:
            if g.get_id_entity() == id_group:
                return g

    def delete_group(self, cell_id):
        self.__group_list.remove(self.find_by_id(cell_id))
        self.__save()

    def get_all(self):
        return self.__group_list

    def get_by_cell(self, cell_id):
        return self.__group_list.get(cell_id)

    def set_new_path(self, new_data_path: str):
        """Schimbă locația fișierului la înregistrare."""
        if new_data_path:
            os.makedirs(new_data_path, exist_ok=True)
            self.__filename = os.path.join(new_data_path, "Groups.json")
            # Dacă fișierul nu există în noua locație, îl creăm
            if not os.path.exists(self.__filename):
                with open(self.__filename, "w") as f:
                    json.dump([], f)
            # Reîncărcăm lista din noua locație
            self.__group_list = self.__read()
