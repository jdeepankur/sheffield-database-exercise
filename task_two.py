from task_one import Database
import utilities.api as api


@api.optionalParam("pretty", False, type=bool)
def fetchCustomer(id):
    data = Database.getRow("customers", "UniqueID", id)
    customer = data[0] if data else None

    if fetchCustomer.pretty:
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
            <tr><td>Date of Birth</td><td>{customer[4]}</td></tr>
            <tr><td>Phone Number</td><td>{customer[5]}</td></tr>
            <tr><td>Town</td><td>{customer[6]}</td></tr>
            <tr><td>County</td><td>{customer[7]}</td></tr>
            <tr><td>Status</td><td>{customer[8]}</td></tr>
            </table>
            </body>
            </html>
            """

            orderlist = ""
            if (
                orders := Database.getRow("orders", "CustomerID", customer[0])
            ) is not None:
                orderlist += "<h2>Orders</h2>"
                for order in orders:
                    orderlist += f"""
                    <h3>Order ID: {order[0]}</h3>
                    <table border="1">
                    <tr><td>Product</td><td>{order[2]}</td></tr>
                    <tr><td>Quantity</td><td>{order[3]}</td></tr>
                    <tr><td>Unit Price</td><td>{order[4]}</td></tr>
                    <tr><td>Delivery Method</td><td>{order[5]}</td></tr>
                    </table>
                    """

            return profile + orderlist
        else:
            return "<html><body><h2>Error: Customer not found</h2></body></html>"

    else:
        if customer:
            orderlist = []
            if (
                orders := Database.getRow("orders", "CustomerID", customer[0])
            ) is not None:
                for order in orders:
                    orderlist.append(
                        {
                            "order_id": order[0],
                            "product": order[2],
                            "quantity": order[3],
                            "unit_price": order[4],
                            "delivery_method": order[5],
                        }
                    )

            response = {
                "Customer Profile": {
                    "customer_id": customer[0],
                    "first_name": customer[1],
                    "last_name": customer[2],
                    "email": customer[3],
                    "dob": customer[4],
                    "phone_number": customer[5],
                    "town": customer[6],
                    "county": customer[7],
                    "status": customer[8],
                }
            }

            if orderlist:
                print(orderlist[0])
                response["Orders"] = {
                    order["order_id"]: {
                        field: value
                        for field, value in order.items()
                        if field != "order_id"
                    }
                    for order in orderlist
                }  # Use the OrderID as the key for the orders

            return response
        else:
            return {"error": "Customer not found"}


api.new_endpoint("/customer/<id>", fetchCustomer)
api.start()
