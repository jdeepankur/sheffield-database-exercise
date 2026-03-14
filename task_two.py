from task_one import Database
import utilities.api as api

def fetchCustomer(id):
    customer = Database.getRow("customers", "UniqueID", id)

    if customer:
        html = f"""
        <html>
        <body>
        <h2>Customer Details</h2>
        <table border="1">
        <tr><th>UniqueID</th><th>{customer[0]}</th></tr>
        <tr><td>First Name</td><td>{customer[1]}</td></tr>
        <tr><td>Last Name</td><td>{customer[2]}</td></tr>
        <tr><td>Email</td><td>{customer[3]}</td></tr>
        <tr><td>Status</td><td>{customer[4]}</td></tr>
        </table>
        </body>
        </html>
        """
        return html
    else:
        return "<html><body><h2>Error: Customer not found</h2></body></html>"

api.new_endpoint("/customer/<id>", fetchCustomer)
api.start()