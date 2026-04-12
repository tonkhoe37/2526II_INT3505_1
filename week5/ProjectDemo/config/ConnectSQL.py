import pyodbc


def get_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=LAPTOP-4NPJU0J9\SQLEXPRESS;"
        "DATABASE=LibraryDB;"
        "Trusted_Connection=yes;"
    )
