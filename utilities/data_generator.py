# A helper program that can be run from the command-line
# It will quickly generate a unique set of both Customer and Order records.

import names, random, rstr

rows = 50
location = "data"
randomcase = lambda s: "".join(
    c.upper() if random.random() < 0.5 else c.lower() for c in s 
) # A helper function to introduce additional variation in the email addresses
uids = [i for i in range(max(100 + rows, 9999))]
random.shuffle(uids)
counties =[
    "Bedfordshire", "Berkshire", "Bristol", "Buckinghamshire", "Cambridgeshire",
    "Cheshire", "City of London", "Cornwall", "County Durham", "Cumbria",
    "Derbyshire", "Devon", "Dorset", "East Riding of Yorkshire", "East Sussex",
    "Essex", "Gloucestershire", "Middlesex", "Greater Manchester",
    "Hampshire", "Herefordshire", "Hertfordshire", "Isle of Wight", "Kent",
    "Lancashire", "Leicestershire", "Lincolnshire", "Merseyside", "Norfolk",
    "North Yorkshire", "Northamptonshire", "Northumberland", "Nottinghamshire",
    "Oxfordshire", "Rutland", "Shropshire", "Somerset", "South Yorkshire",
    "Staffordshire", "Suffolk", "Surrey", "Tyne and Wear", "Warwickshire",
    "West Midlands", "West Sussex", "West Yorkshire", "Wiltshire", "Worcestershire",
    "Aberdeenshire", "Angus", "Argyll and Bute", "Clackmannanshire", "Dumfries and Galloway",
    "Dundee City", "East Ayrshire", "East Dunbartonshire", "East Lothian", "East Renfrewshire",
    "West Lothian", "Falkirk", "Fife", "Strathclyde", "Highland", "Inverclyde", "Tayside", "North Lanarkshire"]
towns = [
    "Bedford", "Luton", "Reading", "Slough", "Bristol", "Buckingham", "Cambridge",
    "Chester", "City of London", "Truro", "Durham", "Carlisle", "Derby",
    "Exeter", "Poole", "Hull", "Brighton", "Chelmsford", "Gloucester",
    "Manchester", "Southampton", "Hereford", "St Albans", "Isle of Wight",
    "Maidstone", "Lancaster", "Leicester", "Lincoln", "Liverpool", "Norwich",
    "York", "Northampton", "Newcastle", "Nottingham", "Oxford", "Rutland",
    "Shrewsbury", "Taunton", "Sheffield", "Stafford", "Ipswich", "Guildford",
    "Newcastle upon Tyne", "Warwick", "Birmingham", "Chichester", "Bradford",
    "Wolverhampton", "Chesterfield", "Worcester", "Aberdeen", "Dundee",
    "Dumfries", "Kirkcaldy", "Glasgow", "Inverness", "Greenock"
]

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
            f"{random.choice(['gmail', 'yahoo', 'yandex', 'hotmail', 'outlook'])}."
            f"{random.choice(['org', 'com', 'net', 'co.uk', 'gov'])}"
        )
        phone = rstr.xeger(fr'\+44 {r'\d' * 4} {r'\d' * 3} {r'\d' * 3}')
        dob = f'{random.randrange(1, 32)}/{random.randrange(1, 13)}/{random.randrange(1900, 2010)}'
        town = random.choice(towns)
        #Obviously some towns are gonna be in the wrong county, but this is okay for our purposes
        county = random.choice(counties)
        status = random.choice(["active", "archived", "suspended"])

        file.write(
            f"{uniqueID},{firstname},{surname},{email},{phone},{dob},{town},{county},{status}{"\n" if i != rows - 1 else ""}"
        )

with open(f"{location}/orders_data.csv", "w") as file:
    file.write("UniqueID,CustomerID,Product Name,Quantity,Unit Price,Delivery Method\n")

    for i in range(rows):
        uniqueID = f"ORD{str(uids[i + rows]).zfill(4)}"
        customerID = random.choice(validIDs)
        productName = (
            f"{random.choice(['Flight', 'Taxi', 'Train', 'Bus', 'Coach', 'Tube', 'Gondola', 'Ship'])} Ticket from "
            f"{random.choice(['London', 'Paris', 'New York', 'Tokyo', 'Sydney', 'Berlin', 'Moscow'])} to "
            f"{random.choice(['Rome', 'Madrid', 'Dubai', 'Singapore', 'Hong Kong', 'Los Angeles'])}"
        )
        quantity = random.randint(1, 10)
        unitPrice = round(random.uniform(10.0, 400.0), 2)
        delivery = random.choice(['Mobile', 'Pick-up at Station', 'Postage', 'Fax', 'Carrier Pigeon'])

        file.write(
            f"{uniqueID},{customerID},{productName},{quantity},{unitPrice},{delivery}{"\n" if i != rows - 1 else ""}"
        )