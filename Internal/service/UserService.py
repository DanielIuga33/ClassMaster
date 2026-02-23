from Internal.repository.RepositoryUser import RepositoryUser
import hashlib


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


class UserService:
    def __init__(self, repository: RepositoryUser):
        self.__repository = repository

    def add_user(self, user):
        # Înainte de a trimite user-ul la repo, îi criptăm parola
        hashed_pass = hash_password(user.get_password())
        user.set_password(hashed_pass)

        # Setăm calea și salvăm
        path_ales = user.get_data_path()
        self.__repository.set_new_path(path_ales)
        return self.__repository.add_user(user)

    def get_user(self, first_name: str, last_name: str):
        for user in self.__repository.get_all():
            if user.first_name == first_name and user.last_name == last_name:
                return [200, user]
        return [404, "User not found"]

    def authenticate(self, identifier, password):
        if "@" in identifier:
            user = self.__repository.find_by_email(identifier)
        else:
            user = self.__repository.find_by_username(identifier)

        if user:
            # Criptăm parola introdusă acum pentru a o compara cu cea din baza de date
            hashed_input = hash_password(password)
            if user.get_password() == hashed_input:
                return user
        return None

    def modify_user(self, user_old, user_new):
        self.__repository.modify_user(user_old, user_new)

    def set_repository_path(self, path):
        return self.__repository.set_new_path(path)

    def delete_user(self, email: str, password: str):
        for user in self.__repository.get_all():
            if user.email == email and user.password == password:
                self.__repository.remove_user(user)
                return [200, "User deleted"]
            elif user.email == email and user.password != password:
                return [400, "Password mismatch"]
        return [404, "User not found"]
