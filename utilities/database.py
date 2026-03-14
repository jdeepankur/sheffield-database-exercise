import mysql.connector as mysqldb
from utilities.environment import env

dbname = env("DB_NAME")

# First a connection has to be established to the mySQL database
db = mysqldb.connect(
    host=env("DB_HOST"), user=env("DB_USER"), password=env("DB_PASSWORD")
)
cursor = db.cursor(buffered=True)

# Now the database can be created and entered if it doesn't already exist
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {dbname}")
cursor.execute(f"USE {dbname}")


class Database:
    @staticmethod
    def reset():
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        for table in tables:
            cursor.execute(f"DROP TABLE {table[0]}")

        db.commit()

    @staticmethod
    def ensureTable(table, columns):
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {table} ({', '.join(f'{column} VARCHAR(255)' for column in columns)});"
        )

    @staticmethod
    def isTable(table):
        cursor.execute(f"SHOW TABLES LIKE '{table}'")
        return cursor.fetchone() is not None

    @staticmethod
    def insert(table, columns, row):
        Database.ensureTable(table, columns)

        columns = ", ".join(columns)
        values = ", ".join(f"'{value}'" for value in row)
        cursor.execute(f"INSERT INTO {table} ({columns}) VALUES ({values})")

        db.commit()

    @staticmethod
    def getColumn(table, column):
        if not Database.isTable(table):
            return None
        else:
            cursor.execute(f"SELECT {column} FROM {table}")
            return cursor.fetchall()

    @staticmethod
    def getRow(table, column, value):
        if not Database.isTable(table):
            return None
        else:
            cursor.execute(f"SELECT * FROM {table} WHERE {column} = '{value}'")
            return cursor.fetchone()
