from repositorys import user_repository
from data.database import User
from data.database import users


def get_users():
    return user_repository.get_all_users()


def create_user(data):
    return user_repository.create_user(data)


def update_user(id, data):
    return user_repository.update_user(
        id, data["name"], data["email"], data["password"]
    )


def delete_user(id):
    return user_repository.delete_user(id)


def find_user(id):
    return user_repository.find_user_by_id(id)


def login(email, password):
    return user_repository.login(email, password)
