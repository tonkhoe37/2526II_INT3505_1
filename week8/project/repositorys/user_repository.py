from data.database import users, User
from data.role_enum import Role


def get_all_users():
    return users


def find_user_by_id(id):
    for u in users:
        if u.id == id:
            return u
    return None


def add_user(user):
    users.append(user)


def update_user(id, name, email, password):
    for i, u in enumerate(users):
        if u.id == id:
            users[i] = User(id, name, email, password)
            return users[i]
    return None


def delete_user(id):
    for i, u in enumerate(users):
        if str(u.id) == str(id):
            users.pop(i)
            return True
    return False


def login(email, password):
    for u in users:
        if u.email == email and u.password == password:
            return u
    return None


def create_user(data):

    # kiểm tra id đã tồn tại chưa
    for user in users:
        if user.id == data["id"]:
            return None

    role = Role[data["role"]]

    user = User(data["id"], data["name"], data["email"], data["password"], role)

    add_user(user)

    return user
