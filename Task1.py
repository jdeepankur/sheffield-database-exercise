import csv, itertools
from utilities.database import Database

customerRawData = 'data/customer_data.csv'

# First the table of all the customers will have to be set up
with open(customerRawData, 'r') as file:
    rawdata = itertools.islice(csv.reader(file), 1, None)
    columns = ['UniqueID', 'FirstName', 'Surname', 'Email', 'Status']
    for row in rawdata: Database.insert('customers', columns, row)