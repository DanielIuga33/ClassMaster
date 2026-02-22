from Internal.entity.Group import Group
from Internal.repository.RepositoryGroup import RepositoryGroup


class GroupService:
    def __init__(self, repository: RepositoryGroup):
        self.__repository = repository

    def set_repository_path(self, path, password):
        # Trimitem atât calea cât și parola către repository
        self.__repository.set_new_path(path, password)

    def add_group(self, name, ids, teacher_id):
        if not name:
            return 400, "Numele și materia sunt obligatorii!"
        self.__repository.add_group(name, ids, teacher_id)
        return 201, "Grupă creată cu succes!"

    def modify_group(self, group_old, group_new):
        self.__repository.modify_group(group_old, group_new)
        return [200, "Modificat cu succes !"]

    def get_group_by_id(self, id_group):
        return self.__repository.find_by_id(id_group)

    def get_group_students(self, id_group):
        return self.get_group_by_id(id_group).get_student_ids()

    def delete_group(self, group_id: str):
        self.__repository.delete_group(group_id)

    def delete_cascade(self, student_id):
        for group in self.__repository.get_all():
            if student_id in self.get_group_students(group.get_id_entity()):
                if len(self.get_group_students(group.get_id_entity())) < 2:
                    self.delete_group(group.get_id_entity())
                else:
                    students = group.get_student_ids()
                    students.remove(student_id)
                    group.set_student_ids(students)
                    self.__repository.modify_group(group, group)

    def get_groups_for_teacher(self, teacher_id):
        result = []
        for group in self.__repository.get_all():
            if group.get_teacher_id() == teacher_id:
                result.append(group)
        return result




