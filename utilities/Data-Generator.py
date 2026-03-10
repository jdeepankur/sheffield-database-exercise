# A helper program that can be run from the command-line
# It will quickly generate a unique set of both Customer and Order records.

import names, random

rows = 50
location = "../data"
randomcase = lambda s: ''.join(c.upper() if random.random() < 0.5 else c.lower() for c in s) # A helper function to introduce additional variation in the email addresses
uids = [i for i in range(max(100 + rows, 9999))]
random.shuffle(uids)

# The customer records have to be written first to make sure that the order records refer to customers who actually exist
validIDs = []
with open(f'{location}/customer_data.csv', 'w') as file:
    file.write('UniqueID,First Name,Surname,Email,Status\n')

    for i in range(rows):
        validIDs.append(uniqueID := f"CUS{str(uids[i]).zfill(4)}")
        firstname = names.get_first_name()
        surname = names.get_last_name()
        email = f"{randomcase(firstname)}.{randomcase(surname)}{random.randint(100, 999)}@{random.choice(["gmail", "yahoo", "yandex" "hotmail", "outlook"])}.{random.choice(["org", "com", "net", "co.uk", "gov"])}"
        status = random.choice(['active', 'archived', 'suspended'])

        file.write(f"{uniqueID},{firstname},{surname},{email},{status}{"\n" if i != rows - 1 else ""}")

print([ID for ID in validIDs])