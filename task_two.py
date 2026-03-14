from task_one import Database
import utilities.api as api

def fetchCustomer(id):
    customer = Database.getRow("customers", "UniqueID", id)[0]

    if customer:
        profile = f"""
        <html>
        <body>
        <h2>Customer Details</h2>
        <table border="1">
        <tr><th>Customer ID</th><th>{customer[0]}</th></tr>
        <tr><td>First Name</td><td>{customer[1]}</td></tr>
        <tr><td>Last Name</td><td>{customer[2]}</td></tr>
        <tr><td>Email</td><td>{customer[3]}</td></tr>
        <tr><td>Status</td><td>{customer[4]}</td></tr>
        </table>
        </body>
        </html>
        """

        orderlist = ""
        if (orders := Database.getRow("orders", "CustomerID", customer[0])) is not None:
            orderlist += "<h2>Orders</h2>"
            for order in orders:
                orderlist += f"""
                <h3>Order ID: {order[0]}</h3>
                <table border="1">
                <tr><td>Product</td><td>{order[2]}</td></tr>
                <tr><td>Quantity</td><td>{order[3]}</td></tr>
                <tr><td>Price</td><td>{order[4]}</td></tr>
                </table>
                """

        return profile + orderlist
    else:
        return "<html><body><h2>Error: Customer not found</h2></body></html>"

api.new_endpoint("/customer/<id>", fetchCustomer)
api.start()