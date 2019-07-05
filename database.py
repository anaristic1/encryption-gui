import sqlite3 as sql


def create_database():
    try:
        connection = sql.connect('data.db')
        cursor = connection.cursor()
        sql_command = """
          CREATE TABLE data(
          id INTEGER PRIMARY KEY, 
          filename VARCHAR(50),
          filetype VARCHAR(10),
          key VARCHAR(30),
          iv VARCHAR(50) );
        """
        connection.execute(sql_command)
    except sql.Error as err:
        print(f"Error: {err.args[0]}")
    finally:
        connection.close()


def insert(file_name, file_type, key, iv):
    try:
        connection = sql.connect('data.db')
        cursor = connection.cursor()
        sql_command= f"""
        INSERT INTO data (id, filename, filetype, key, iv)
        VALUES(NULL,"{file_name}","{file_type}","{key}","{iv}");
        """
        cursor.execute(sql_command)
        connection.commit()
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
    pass