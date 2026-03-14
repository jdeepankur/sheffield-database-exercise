from task_one import Database
import utilities.api as api

@api.optionalParam("pretty", False, type=bool)
def fetchCustomer(id):
    if fetchCustomer.pretty:
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
        
    else:
        customer = Database.getRow("customers", "UniqueID", id)
        if customer:
            orderlist = []
            if (orders := Database.getRow("orders", "CustomerID", customer[0][0])) is not None:
                for order in orders:
                    orderlist.append({
                        "OrderID": order[0],
                        "Product": order[2],
                        "Quantity": order[3],
                        "Price": order[4]
                    })

            response = {
            "Customer Profile":{
                "CustomerID": customer[0][0],
                "FirstName": customer[0][1],
                "LastName": customer[0][2],
                "Email": customer[0][3],
                "Status": customer[0][4]
                }
            }

            if orderlist:
                response["Orders"] = {order["OrderID"]:{field: value for field, value in order.items() if field != 'OrderID'} for order in orderlist} # Use the OrderID as the key for the orders

            return response
        else:
            return {"error": "Customer not found"}

api.new_endpoint("/customer/<id>", fetchCustomer)
api.start()