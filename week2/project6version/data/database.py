class User:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}


users = [
    User("1", "Ton Thien Khoe", "khoe@gmail.com"),
    User("2", "Nguyen Van A", "vana@gmail.com"),
]
