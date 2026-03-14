from utilities.database import Database

def fetchCustomersByField(field, value):
    customers = Database.getRow("customers", field, value)
    return customers

def fetchCustomersByStatus(status):
    customers = fetchCustomersByField("Status", status)
    return customers

# first we need to get all customers who are active and their orders
def fetchActiveCustomers():
    active_customers = fetchCustomersByStatus("Active")
    # next collate their orders