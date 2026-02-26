import uuid


class Entity:
    def __init__(self):
        self.__id_entity = str(uuid.uuid4())

    def get_id_entity(self):
        return self.__id_entity


