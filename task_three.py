from utilities.database import Database
from operator import add, mul

def getOrdersByCustomerID(customer_id):
    orders = Database.getRow("orders", "CustomerID", customer_id)
    return orders

def fetchCustomersByField(field, value):
    customers = Database.getRow("customers", field, value)
    return customers

def fetchCustomersByStatus(status):
    customers = fetchCustomersByField("Status", status)
    return customers

def addNewField(customers, headers, new_field_name, fields_to_combine, operation):
    headers.append(new_field_name)
    for i, customer in enumerate(customers):
        new_field_value = operation(*[customer[headers.index(field)] for field in fields_to_combine])
        customers[i] = customer + (new_field_value,)

customer_headers = Database.getHeaders("customers")
active_customers = fetchCustomersByStatus("Active")        
addNewField(active_customers, customer_headers, "Full Name", ["FirstName", "Surname"], add)

customer_orders = {customer[0]: getOrdersByCustomerID(customer[0]) for customer in active_customers}
order_headers = Database.getHeaders("orders")
number_fields = ["UnitPrice", "Quantity"]

for customer, orders in customer_orders.items():
    for i in range(len(orders)):
        for field in number_fields:
            orders[i] = orders[i][:order_headers.index(field)] + (float(orders[i][order_headers.index(field)]),) + orders[i][order_headers.index(field)+1:]

    addNewField(orders, order_headers, "Total Price", number_fields, mul)