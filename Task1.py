import csv, itertools
from utilities.database import Database

customerRawData = 'data/customer_data.csv'
orderRawData = 'data/order_data.csv'

# First the table of all the customers will have to be set up
with open(customerRawData, 'r') as file:
    rawdata = itertools.islice(csv.reader(file), 1, None)
    columns = ['UniqueID', 'FirstName', 'Surname', 'Email', 'Status']
    for row in rawdata:
        # To help make the program re-runnable, we have to ensure that duplicates are excluded 
        if not Database.getRow('customers', 'UniqueID', row[0]):
            Database.insert('customers', columns, row)

# Second the table of the orders, which is linked to the customers through the CustomerID, will have to be set up
with open(orderRawData, 'r') as file:
    rawdata = itertools.islice(csv.reader(file), 1, None)
    columns = ['UniqueID', 'CustomerID', 'ProductName', 'Quantity', 'UnitPrice']
    for row in rawdata:
        if not Database.getRow('orders', 'UniqueID', row[0]):
            Database.insert('orders', columns, row)