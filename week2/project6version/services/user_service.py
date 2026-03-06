from repositorys import user_repository
from data.database import User


def get_users():
    return user_repository.get_all_users()


def create_user(data):
    user = User(data["id"], data["name"], data["email"])
    user_repository.add_user(user)
    return user


def update_user(id, data):
    return user_repository.update_user(id, data["name"], data["email"])


def delete_user(id):
    return user_repository.delete_user(id)


def find_user(id):
    return user_repository.find_user_by_id(id)
