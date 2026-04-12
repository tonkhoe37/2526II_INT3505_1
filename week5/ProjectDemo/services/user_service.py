from repositorys import user_repository


# GET USERS (3 loại pagination)
def get_users(type, page=None, size=10, last_id=None, offset=None):

    if type == "page":
        return user_repository.get_users_page(page, size)

    elif type == "offset":
        return user_repository.get_users_offset(offset, size)

    elif type == "cursor":
        return user_repository.get_users_cursor(last_id, size)

    else:
        raise ValueError("Invalid pagination type")


# CREATE USER
def create_user(data):
    return user_repository.create_user(data["name"], data["email"], data["password"])


# UPDATE USER
def update_user(user_id, data):
    return user_repository.update_user(user_id, data["name"], data["email"])


# DELETE USER
def delete_user(user_id):
    return user_repository.delete_user(user_id)


# FIND USER
def find_user(user_id):
    return user_repository.find_user_by_id(user_id)


# LOGIN
def login(email, password):
    return user_repository.login(email, password)


"""
def get_users_with_meta(type, page, size, last_id, offset):

    users = get_users(type, page, size, last_id, offset)

    if type == "page":
        total = user_repository.count_users()
        total_pages = (total + size - 1) // size

        return users, total, total_pages

    return users, None, None
"""
