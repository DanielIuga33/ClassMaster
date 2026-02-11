from Internal.entity.Entity import Entity


class Student(Entity):
    def __init__(self, first_name: str, last_name: str, grade: str, price: int, teacher_id: str, **kwargs):
        super().__init__()
        if 'id_entity' in kwargs:
            self._Entity__id_entity = kwargs['id_entity']
        self.__first_name = first_name
        self.__last_name = last_name
        self.__grade = grade
        self.__price = price
        self.__teacher_id = teacher_id

    def get_full_name(self):
        return f"{self.__first_name} {self.__last_name}"

    def get_first_name(self):
        return self.__first_name

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def get_last_name(self):
        return self.__last_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def get_grade(self):
        return self.__grade

    def set_grade(self, grade):
        self.__grade = grade

    def get_price(self):
        return self.__price

    def get_teacher_id(self):
        return self.__teacher_id

    def set_teacher_id(self, teacher_id):
        self.__teacher_id = teacher_id
