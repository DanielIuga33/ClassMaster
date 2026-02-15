from Internal.entity.Entity import Entity


class Preset(Entity):
    def __init__(self, teacher_id, name, data, **kwargs):
        super().__init__()
        if 'id_entity' in kwargs:
            self._Entity__id_entity = kwargs['id_entity']
        self.__teacher_id = teacher_id
        self.__name = name
        self.__data = data  # Dicționarul cu celulele D0_R1 etc.

    def get_teacher_id(self): return self.__teacher_id
    def set_teacher_id(self, teacher_id): self.__teacher_id = teacher_id
    def get_name(self): return self.__name
    def set_name(self, name): self.__name = name
    def get_data(self): return self.__data
    def set_data(self, data): self.__data = data

