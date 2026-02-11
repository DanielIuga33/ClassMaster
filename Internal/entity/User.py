from Internal.entity.Entity import Entity


class User(Entity):
    def __init__(self, username: str, first_name: str, last_name: str, email: str, password: str, data_path: str,
                 street_address: str, city: str, state: str, birthday: str, **kwargs):
        super().__init__()
        if 'id_entity' in kwargs:
            self._Entity__id_entity = kwargs['id_entity']
        self.__username = username
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__password = password
        self.__data_path = data_path
        self.__street_address = street_address
        self.__city = city
        self.__state = state
        self.__birthday = birthday

    def get_username(self):
        return self.__username

    def set_username(self, username: str) -> None:
        self.__username = username

    def get_first_name(self) -> str:
        return self.__first_name

    def set_first_name(self, first_name: str) -> None:
        self.__first_name = first_name

    def get_last_name(self) -> str:
        return self.__last_name

    def set_last_name(self, last_name: str) -> None:
        self.__last_name = last_name

    def get_email(self) -> str:
        return self.__email

    def set_email(self, email: str) -> None:
        self.__email = email

    def get_password(self) -> str:
        return self.__password

    def set_password(self, password: str) -> None:
        self.__password = password

    def get_data_path(self) -> str:
        return self.__data_path

    def set_data_path(self, data_path: str) -> None:
        self.__data_path = data_path

    def get_street_address(self) -> str:
        return self.__street_address

    def set_street_address(self, street_address: str) -> None:
        self.__street_address = street_address

    def get_city(self) -> str:
        return self.__city

    def set_city(self, city: str) -> None:
        self.__city = city

    def get_state(self) -> str:
        return self.__state

    def set_state(self, state: str) -> None:
        self.__state = state

    def get_birthday(self) -> str:
        return self.__birthday

    def set_birthday(self, birthday: str) -> None:
        self.__birthday = birthday

    def __str__(self):
        return (
            f"{self.__first_name},{self.__email},{self.__password},{self.data_path},{street_address}, {self.__city},"
            f"{self.__state},{self.__birthday}\n")
