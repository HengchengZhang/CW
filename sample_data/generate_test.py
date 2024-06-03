import csv
import random
import datetime
from faker import Faker
import names
random.seed("2024")
fake = Faker("en_AU")
fake.seed_instance("2024")


data_list = []
with open('au_postcode.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
for row in reader:
    data_list.append(row)
print(data_list)

def generate_property_info():
    property_id = f"{random.randint(1, 99)}{random.randint(1000, 9999)}"
    property_capacity = f"{random.randint(2, 8)}"
    property_address = f"{fake.address()}".replace("\n", ", ")
    return property_id, property_capacity, property_address


def random_date(start, end):
    return start + datetime.timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )


def generate_order_info(start_date, end_date):
    booking_id = f"{random.randint(10000000, 99999999)}"
    check_in_date = random_date(start_date, end_date)
    days = random.randint(1, 15) // 1
    days_of_stay = datetime.timedelta(days)
    check_out_date = (check_in_date + days_of_stay).strftime('%d-%m-%Y')
    base_fee = days * random.randint(40, 160)
    service_fee = round(base_fee * 0.15, 2)
    cleaning_fee = round(random.uniform(0.8, 2) * base_fee / days, 2)
    gst = round((base_fee + service_fee + cleaning_fee) * 0.1, 2)
    total_price = round(gst * 11, 2)
    return booking_id, check_in_date.strftime('%d-%m-%Y'), check_out_date, \
        base_fee, service_fee, cleaning_fee, gst, total_price


def generate_owner_info():
    owner_id = f"{random.randint(1, 99)}{random.randint(100, 999)}"
    abn = f"{random.randint(10, 99)} {random.randint(100, 999)} {random.randint(100, 999)} {random.randint(100, 999)}"
    tin = f"{random.randint(100000000, 999999999)}"
    dob = random_date(datetime.datetime.strptime(
        '01-01-1940', '%d-%m-%Y'), datetime.datetime.strptime('31-12-1999', '%d-%m-%Y')).strftime('%d-%m-%Y')
    if random.random() > 0.2:
        owner_location = "Australia"
        owner_address = f"{fake.address()}".replace("\n", ", ")
        bank_name = "Commonwealth Bank of Australia"
    else:
        owner_location = "New Zealand"
        owner_address = "Auckland, NZ"
        bank_name = "ANZ Bank"
    contact_number = f"+614{random.randint(10000000, 99999999)}"
    # email = "example@gmail.com" if random.random() > 0.2 else None #80% chance have email address
    email = "example@gmail.com"
    name = names.get_full_name()
    rating = f"{random.randint(0, 10)}"
    bank_account_name = name
    bank_account_number = f"{random.randint(1000, 9999)}{random.randint(1000, 99999)}"
    return owner_id, abn, tin, dob, contact_number, email, rating, owner_location, \
        owner_address, bank_account_name, bank_account_number, bank_name


def generate_order_status(price):
    i = random.random()
    if i > 0.2:
        order_status = "Completed"
        final_price = price
    elif i > 0.12:
        order_status = "Cancelled"
        final_price = 0
    elif i > 0.04:
        order_status = "Refunded"
        final_price = 0
    else:
        order_status = "Partially Refunded"
        final_price = round(price * random.uniform(0.5, 0.9), 2)
    payment_refernce_number = f"{random.randint(1000000000, 9999999999)}"
    final_gst = round(final_price / 11, 2)
    final_price = round(final_gst * 11, 2)
    return order_status, final_price, final_gst, payment_refernce_number


def introduce_error(value, error_rate):
    if random.random() < error_rate:
        if isinstance(value, str):
            # Introduce error in strings by either removing or altering characters
            return value[:-1] if len(value) > 1 else ""
        elif isinstance(value, float) or isinstance(value, int):
            # Introduce error in numbers by setting them to None or a clearly incorrect value
            return None if random.random() < 0.5 else "error"
    return value


def generate_data(num_entries, error_rate=0):
    data = []
    start_date = datetime.datetime.strptime('01-01-2023', '%d-%m-%Y')
    end_date = datetime.datetime.strptime('30-06-2023', '%d-%m-%Y')

    for _ in range(num_entries):
        # transaction_date = random_date(start_date, end_date).strftime('%Y-%m-%d')
        property_id, property_capacity, property_address = generate_property_info()
        booking_id, check_in_date, check_out_date, base_fee, service_fee, cleaning_fee, \
            gst, total_price = generate_order_info(start_date, end_date)
        owner_id, abn, tin, dob, contact_number, email, rating, owner_location, \
            owner_address, bank_account_name, bank_account_number, bank_name = generate_owner_info()
        order_status, final_price, final_gst, payment_refernce_number = generate_order_status(
            total_price)
        abn = abn if random.random() > 0.2 else None  # 80% chance of having ABN
        tin = tin if abn is None else None  # If no ABN, generate TIN
        # # Introduce errors based on error rate
        # transaction_id = introduce_error(transaction_id, error_rate)
        # participant_id = introduce_error(participant_id, error_rate)
        # transaction_date = introduce_error(transaction_date, error_rate)
        # amount = introduce_error(amount, error_rate)
        # gst = introduce_error(gst, error_rate)
        # service_type = introduce_error(service_type, error_rate)
        # abn = introduce_error(abn, error_rate) if abn else ""
        # tin = introduce_error(tin, error_rate) if tin else ""
        # name = introduce_error(name, error_rate)
        # address = introduce_error(address, error_rate)
        # postcode = introduce_error(postcode, error_rate)
        data.append([property_id, property_capacity, property_address, booking_id,
                    check_in_date, check_out_date, base_fee, service_fee, cleaning_fee,
                    gst, total_price, owner_id, abn, tin, dob, contact_number, email,
                    rating, owner_location, owner_address, bank_account_name,
                    bank_account_number, bank_name, order_status, final_price, final_gst, 
                    payment_refernce_number])

    return data


# Number of sample entries to generate
num_entries = 2500000
# Error rate
error_rate = 0.05  # 5% error rate

# Generate sample data
sample_data = generate_data(num_entries, error_rate=error_rate)

# Write data to CSV file
with open('serr_sample_data.csv', 'w', newline='') as csvfile:
    fieldnames = ['property_id', 'property_capacity', 'property_address', 'booking_id',
                  'check_in_date', 'check_out_date', 'base_fee', 'service_fee', 'cleaning_fee',
                  'gst', 'total_price', 'owner_id', 'abn', 'tin', 'dob', 'contact_number',
                  'email', 'rating', 'owner_location', 'owner_address', 'bank_account_name',
                  'bank_account_number', 'bank_name', 'order_status', 'final_price', 'final_gst', 
                  'payment_refernce_number']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for row in sample_data:
        writer.writerow({
            'property_id': row[0],
            'property_capacity': row[1],
            'property_address': row[2],
            'booking_id': row[3],
            'check_in_date': row[4],
            'check_out_date': row[5],
            'base_fee': row[6],
            'service_fee': row[7],
            'cleaning_fee': row[8],
            'gst': row[9],
            'total_price': row[10],
            'owner_id': row[11],
            'abn': row[12] if row[12] else '',
            'tin': row[13] if row[13] else '',
            'dob': row[14],
            'contact_number': row[15],
            'email': row[16],
            'rating': row[17],
            'owner_location': row[18],
            'owner_address': row[19],
            'bank_account_name': row[20],
            'bank_account_number': row[21],
            'bank_name': row[22],
            'order_status': row[23],
            'final_price': row[24],
            'final_gst': row[25],
            'payment_refernce_number': row[26]
        })

print(f'Sample data with {num_entries} entries.')
