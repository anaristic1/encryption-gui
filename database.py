import sqlite3 as sql
from base64 import b64encode, b64decode

def create_database():
    try:
        connection = sql.connect('data.db')
        cursor = connection.cursor()
        sql_command = """
          CREATE TABLE data(
          id INTEGER PRIMARY KEY,
          algorithm VARCHAR(10),
          path VARCHAR(50),
          filetype VARCHAR(10),
          key VARCHAR(30),
          iv VARCHAR(50) );
        """
        connection.execute(sql_command)
    except sql.Error as err:
        print(f"Error: {err.args[0]}")
    finally:
        connection.close()


def insert(path,algorithm, file_type, key, iv):
    try:
        key = b64encode(key).decode('utf-8')
        # iv = b64encode(iv).decode('utf-8')
        connection = sql.connect('data.db')
        cursor = connection.cursor()
        sql_command= f"""
        INSERT INTO data (id,algorithm, path, filetype, key, iv)
        VALUES(NULL,"{algorithm}","{path}","{file_type}","{key}","{iv}");
        """
        cursor.execute(sql_command)
        connection.commit()
    except sql.Error as err:
        print(f"Error: {err.args[0]}")
    finally:
        connection.close()


def get_specific_rows(path,algorithm):
    try:
        connection = sql.connect('data.db')
        cursor = connection.cursor()
        sql_command= f"""SELECT * FROM data WHERE path="{path}" AND algorithm="{algorithm}" """
        cursor.execute(sql_command)
        return cursor.fetchall()
    except sql.Error as err:
        print(f"Error: {err.args[0]}")
    finally:
        connection.close()


def get_all():
    try:
        connection = sql.connect('data.db')
        cursor = connection.cursor()
        sql_command= """SELECT * FROM data"""
        cursor.execute(sql_command)
        return cursor.fetchall()
    except sql.Error as err:
        print(f"Error: {err.args[0]}")
    finally:
        connection.close()


if __name__ == '__main__':
    create_database()
    # rows = get_specific_rows("C:/Users/Ana/Desktop/plain.enc","salsa20")
    # for row in rows:
    #     print(row)