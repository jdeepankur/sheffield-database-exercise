import csv, rich
from utilities.database import Database

tables = ["customers", "orders"]

for name in tables:
    raw_data = f"data/{name}_data.csv"

    with open(raw_data, "r") as f:
        rows = csv.reader(f)
        columns = next(rows)

        for row in rows:
            if not Database.getRow(name, columns[0], row[0]):
                Database.insert(name, columns, row)