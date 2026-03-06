from data.database import users, User


def get_all_users():
    return users


def find_user_by_id(id):
    for u in users:
        if u.id == id:
            return u
    return None


def add_user(user):
    users.append(user)


def update_user(id, name, email):
    for i, u in enumerate(users):
        if u.id == id:
            users[i] = User(id, name, email)
            return users[i]
    return None


def delete_user(id):
    for i, u in enumerate(users):
        if u.id == id:
            users.pop(i)
            return True
    return False
