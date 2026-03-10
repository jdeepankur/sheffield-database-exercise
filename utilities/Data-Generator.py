# A helper program that can be run from the command-line
# It will quickly generate a unique set of both Customer and Order records.

import names, random

rows = 50

# The customer records have to be written first to make sure that the order records refer to customers who actually exist
with open('customer_data.csv', 'w') as file:
    file.write('UniqueID,First Name,Surname,Email,Status\n')

    for i in range(rows):
        uniqueID = f"CUS{str(i+1).zfill(4)}"
        firstname = names.get_first_name()
        surname = names.get_last_name()
        email = f"{firstname}.{surname.lower()}{random.randint(100, 999)}@{random.choice(["gmail", "yahoo", "yandex" "hotmail", "outlook"])}.{random.choice(["org", "com", "net", "co.uk", "gov"])}"
        status = random.choice(['active', 'archived', 'suspended'])

        file.write(f"{uniqueID},{firstname},{surname},{email},{status}\n")

