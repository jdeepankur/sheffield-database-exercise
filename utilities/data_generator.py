# A helper program that can be run from the command-line
# It will quickly generate a unique set of both Customer and Order records.

import utilities.bigdata as bd
import names, random, rstr

rows = 50
location = "data"
randomcase = lambda s: "".join(
    c.upper() if random.random() < 0.5 else c.lower() for c in s
)  # A helper function to introduce additional variation in the email addresses
uids = [i for i in range(max(100 + rows, 9999))]
random.shuffle(uids)

# The customer records have to be written first to make sure that the order records refer to customers who actually exist
validIDs = []
with open(f"{location}/customers_data.csv", "w") as file:
    file.write("UniqueID,First Name,Surname,Email,DOB,Phone,Town,County,Status\n")

    for i in range(rows):
        validIDs.append(uniqueID := f"CUS{str(uids[i]).zfill(4)}")
        firstname = names.get_first_name()
        surname = names.get_last_name()
        email = (
            f"{randomcase(firstname)}.{randomcase(surname)}{random.randint(100, 999)}@"
            f"{random.choice(bd.emails)}."
            f"{random.choice(bd.domains)}"
        )
        phone = rstr.xeger(fr'\+44 {r'\d' * 4} {r'\d' * 3} {r'\d' * 3}')
        dob = f"{random.randrange(1, 32)}/{random.randrange(1, 13)}/{random.randrange(1900, 2010)}"
        town = random.choice(bd.towns)
        # Some towns are going to be in the wrong county, but this is okay for our purposes
        county = random.choice(bd.counties)
        status = bd.statuses(rows)[i]

        file.write(
            f"{uniqueID},{firstname},{surname},{email},{phone},{dob},{town},{county},{status}{"\n" if i != rows - 1 else ""}"
        )

with open(f"{location}/orders_data.csv", "w") as file:
    file.write("UniqueID,CustomerID,Product Name,Quantity,Unit Price,Delivery Method\n")

    for i in range(rows):
        uniqueID = f"ORD{str(uids[i + rows]).zfill(4)}"
        customerID = random.choice(validIDs)
        productName = (
            f"{random.choice(bd.transit)} Ticket from "
            f"{random.choice(bd.places)} to "
            f"{random.choice(bd.places)}"
        )
        quantity = random.randint(1, 10)
        unitPrice = round(random.uniform(10.0, 400.0), 2)
        delivery = random.choice(bd.couriers)

        file.write(
            f"{uniqueID},{customerID},{productName},{quantity},{unitPrice},{delivery}{"\n" if i != rows - 1 else ""}"
        )
