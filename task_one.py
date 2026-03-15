import csv
from utilities.database import Database

tables = ["customers", "orders"]

Database.reset()
for name in tables:
    raw_data = f"data/{name}_data.csv"

    with open(raw_data, "r") as f:
        rows = csv.reader(f)
        columns = [column.replace(" ", "") for column in next(rows)]

        for row in rows:
            if not Database.getRow(name, columns[0], row[0]):
                Database.insert(name, columns, row)

if __name__ == "__main__":
    print("Task 1 has run successfully.")
    print("The database has been populated with data from the CSV files.")