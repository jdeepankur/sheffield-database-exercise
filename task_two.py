from task_one import Database
import utilities.api as api

def fetchCustomer(id):
    customer = Database.getRow("customers", "UniqueID", id)

    if customer:
        return {
            "UniqueID": customer[0],
            "First_Name": customer[1],
            "Last_Name": customer[2],
            "Email": customer[3],
            "status": customer[4]
        }
    else:
        return {"error": "Customer not found"}

api.new_endpoint("/customer/<id>", fetchCustomer)
api.start()