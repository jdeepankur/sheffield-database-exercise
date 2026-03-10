# A helper program that can be run from the command-line
# It will quickly generate a unique set of both Customer and Order records.

import names

rows = 50
random_string = lambda length: ''.join(random.choice(string.ascii_letters) for i in range(length))

with open('customer_data.csv', 'w') as file:
    file.write('UniqueID,FirstName,Surname,Email,Status\n')

    for i in range(rows):
        customer_id = f"CUS{str(i+1).zfill(4)}"
        first_name = random_string(random.randint(5, 8))
        surname = random_string(random.randint(6, 15))
        email = f"{first_name.lower()}.{surname.lower()}@example.com"
        status = random.choice(['active', 'archived', 'suspended'])
        file.write(f"{customer_id},{first_name},{surname},{email},{status}\n")

