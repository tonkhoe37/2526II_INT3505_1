from data.user_database import User
from config.ConnectSQL import get_connection


# HELPER: map row -> User
def map_to_user(row):
    return User(row[0], row[1], row[2], row[3])


# PAGE-BASED PAGINATION
def get_users_page(page: int, size: int):
    conn = get_connection()
    cursor = conn.cursor()

    offset = (page - 1) * size

    query = """
        SELECT id, name, email, password
        FROM dbo.users
        ORDER BY id
        OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
    """

    cursor.execute(query, (offset, size))
    rows = cursor.fetchall()

    return [map_to_user(row) for row in rows]


# OFFSET-BASED PAGINATION
def get_users_offset(offset: int, size: int):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT id, name, email, password
        FROM dbo.users
        ORDER BY id
        OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
    """

    cursor.execute(query, (offset, size))
    rows = cursor.fetchall()

    return [map_to_user(row) for row in rows]


# CURSOR-BASED PAGINATION
def get_users_cursor(last_id: int, size: int):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT id, name, email, password
        FROM dbo.users
        WHERE id > ?
        ORDER BY id
        OFFSET 0 ROWS FETCH NEXT ? ROWS ONLY
    """

    cursor.execute(query, (last_id, size))
    rows = cursor.fetchall()

    return [map_to_user(row) for row in rows]


# FIND BY ID
def find_user_by_id(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT id, name, email, password
        FROM dbo.users
        WHERE id = ?
    """

    cursor.execute(query, (user_id,))
    row = cursor.fetchone()

    return map_to_user(row) if row else None


# CREATE USER
def create_user(name: str, email: str, password: str):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO dbo.users (name, email, password)
        VALUES (?, ?, ?)
    """

    cursor.execute(query, (name, email, password))
    conn.commit()

    return True


# UPDATE USER
def update_user(user_id: int, name: str, email: str):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        UPDATE dbo.users
        SET name = ?, email = ?
        WHERE id = ?
    """

    cursor.execute(query, (name, email, user_id))
    conn.commit()

    return cursor.rowcount > 0


# DELETE USER
def delete_user(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    query = "DELETE FROM dbo.users WHERE id = ?"

    cursor.execute(query, (user_id,))
    conn.commit()

    return cursor.rowcount > 0


def count_users():
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT COUNT(*) FROM users"
    cursor.execute(query)

    return cursor.fetchone()[0]
