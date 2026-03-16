import utilities.dbsetup as dbsetup, mysql.connector as mysqldb
from utilities.environment import env

dbname = env("DB_NAME")


# Wrapper method that guards against SQL injection
def sql_guard(func):
    def wrapper(*args, **kwargs):
        for arg in args:
            if isinstance(arg, str) and (";" in arg or "--" in arg):
                raise ValueError("Potential SQL injection detected.")
        for value in kwargs.values():
            if isinstance(value, str) and (";" in value or "--" in value):
                raise ValueError("Potential SQL injection detected.")
        return func(*args, **kwargs)

    return wrapper


# First we make sure that mySQL is running
dbsetup.run()
dbsetup.wait(mysqldb)

# Next a connection has to be established to the mySQL database
try:
    db = mysqldb.connect(
        host=env("DB_HOST"), user=env("DB_USER"), password=env("DB_PASSWORD")
    )
    cursor = db.cursor(buffered=True)
except mysqldb.Error as err:
    print(f"Error connecting to MySQL: {err}")
    exit(1)

# Now the database can be created and entered if it doesn't already exist
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {dbname}")
cursor.execute(f"USE {dbname}")


def tablecheck(func):
    def wrapper(table, *args, **kwargs):
        if not Database.isTable(table):
            return None
        return func(table, *args, **kwargs)

    return wrapper


class Database:
    @staticmethod
    @sql_guard
    def reset():
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        for table in tables:
            cursor.execute(f"DROP TABLE {table[0]}")

        db.commit()

    @staticmethod
    @sql_guard
    def ensureTable(table, columns):
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {table} ({', '.join(f'{column} VARCHAR(255)' for column in columns)});"
        )

    @staticmethod
    @sql_guard
    def isTable(table):
        cursor.execute(f"SHOW TABLES LIKE '{table}'")
        return cursor.fetchone() is not None

    @staticmethod
    @sql_guard
    def insert(table, columns, row):
        Database.ensureTable(table, columns)

        columns = ", ".join(columns)
        values = ", ".join(f"'{value}'" for value in row)
        cursor.execute(f"INSERT INTO {table} ({columns}) VALUES ({values})")

        db.commit()

    @staticmethod
    @tablecheck
    @sql_guard
    def getColumn(table, column):
        cursor.execute(f"SELECT {column} FROM {table}")
        return cursor.fetchall()

    @staticmethod
    @tablecheck
    @sql_guard
    def getRow(table, column, value):
        cursor.execute(f"SELECT * FROM {table} WHERE {column} = '{value}'")
        return cursor.fetchall()

    @staticmethod
    @tablecheck
    @sql_guard
    def getHeaders(table):
        cursor.execute(f"SHOW COLUMNS FROM {table}")
        return [column[0] for column in cursor.fetchall()]
