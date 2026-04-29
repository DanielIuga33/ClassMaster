from Internal.entity.Entity import Entity


class Group(Entity):
    def __init__(self, group_name, grade, student_ids, day, time_interval, teacher_id, **kwargs):
        super().__init__()
        if 'id_entity' in kwargs:
            self._Entity__id_entity = kwargs['id_entity']
        self.__group_name = group_name           # Numele grupei
        self.__grade = grade
        self.__student_ids = student_ids     # Listă cu ID-urile studenților (din Students.json)
        self.__day = day                     # Luni, Marți etc.
        self.__time_interval = time_interval  # ex: 14:00 - 16:00
        self.__teacher_id = teacher_id

    def get_group_name(self):
        return self.__group_name

    def set_group_name(self, group_name):
        self.__group_name = group_name

    def get_grade(self):
        return self.__grade

    def set_grade(self, grade):
        self.__grade = grade

    def get_student_ids(self):
        return self.__student_ids

    def set_student_ids(self, student_ids):
        self.__student_ids = student_ids

    def get_day(self):
        return self.__day

    def set_day(self, day):
        return self.__day

    def get_time_interval(self):
        return self.__time_interval

    def set_time_interval(self, time_interval):
        self.__time_interval = time_interval

    def get_teacher_id(self):
        return self.__teacher_id

    def set_teacher_id(self, teacher_id):
        self.__teacher_id = teacher_id

    def to_dict(self):
        """Transformă obiectul în dicționar pentru salvarea în JSON."""
        return {
            "id_entity": self._Entity__id_entity,
            "group_grade": self.__grade,
            "student_ids": self.__student_ids,
            "day": self.__day,
            "time_interval": self.__time_interval,
        }

    def get_display_name(self):
        return f"{self.__group_name} - {self.__grade}"
