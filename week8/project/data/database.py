from data.role_enum import Role


class User:
    def __init__(self, id, name, email, password, role=Role.USER):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.role = role

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role.value,
        }


users = [
    User("1", "Ton Thien Khoe", "khoe@gmail.com", "password1", Role.ADMIN),
    User("2", "Nguyen Van A", "vana@gmail.com", "password2", Role.USER),
    User("3", "Le Thi B", "lethib@gmail.com", "password3", Role.USER),
]
