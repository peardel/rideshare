import sqlite3

from student import Pupil

# values
database_name = "students"

def create_database():
    connection = sqlite3.connect(f"{database_name}.db")
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE Pupils(X,Y)")
    connection.close()

def insert_pupil(pupil):
    connection = sqlite3.connect(f"{database_name}.db")
    cursor = connection.cursor()

    cursor.execute("""INSERT INTO Pupils VALUES
    ()
    """)