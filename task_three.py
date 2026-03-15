from utilities.database import Database
from operator import mul
from utilities.environment import env
import os


def wordjoin(*args):
    return " ".join(args)


def getOrdersByCustomerID(customer_id):
    orders = Database.getRow("orders", "CustomerID", customer_id)
    return orders


def fetchCustomersByField(field, value):
    customers = Database.getRow("customers", field, value)
    return customers


def fetchCustomersByStatus(status):
    customers = fetchCustomersByField("Status", status)
    return customers


def addNewField(
    customers, headers, new_field_name, fields_to_combine, operation, format=None
):
    if new_field_name not in headers:
        headers.append(new_field_name)
    for i, customer in enumerate(customers):
        new_field_value = operation(
            *[customer[headers.index(field)] for field in fields_to_combine]
        )
        if format:
            new_field_value = f"{new_field_value:{format}}"
        customers[i] = customer + (new_field_value,)


customer_headers = Database.getHeaders("customers")
active_customers = fetchCustomersByStatus("Active")
addNewField(
    active_customers, customer_headers, "Full Name", ["FirstName", "Surname"], wordjoin
)

customer_orders = {
    customer[0]: getOrdersByCustomerID(customer[0]) for customer in active_customers
}
order_headers = Database.getHeaders("orders")
number_fields = ["UnitPrice", "Quantity"]

for customer, orders in customer_orders.items():
    for i in range(len(orders)):
        for field in number_fields:
            orders[i] = (
                orders[i][: order_headers.index(field)]
                + (eval(orders[i][order_headers.index(field)]),)
                + orders[i][order_headers.index(field) + 1 :]
            )

    addNewField(orders, order_headers, "Total Price", number_fields, mul, format=".2f")

if not os.path.exists(env("OUTPUT_DIR")):
    os.makedirs(env("OUTPUT_DIR"))

with open(env("OUTPUT_DIR") + "/active_customers.csv", "w") as f:
    f.write(",".join(customer_headers) + "\n")
    for customer in active_customers:
        f.write(",".join(map(str, customer)) + "\n")

with open(env("OUTPUT_DIR") + "/active_customer_orders.csv", "w") as f:
    f.write(",".join(order_headers) + "\n")
    for orders in customer_orders.values():
        for order in orders:
            f.write(",".join(map(str, order)) + "\n")
