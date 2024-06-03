import csv
import random
import pandas as pd
import datetime
from faker import Faker
import names

# Set seeds for reproducibility
random.seed(2024)
fake = Faker("en_AU")
fake.seed_instance(2024)

# Constants
NUM_ENTRIES = 300
BATCH_SIZE = 10000  # Adjust based on memory capacity and performance

df = pd.read_csv('au_postcode.csv')
postcode = df[['postcode', 'place_name', 'state_code']].values
postcode_data_length = len(postcode) - 1

def generate_property_info():
    property_id = f"{random.randint(1, 99):02d}{random.randint(1000, 9999)}"
    property_capacity = random.randint(2, 8)
    property_address = postcode[random.randint(0, postcode_data_length) // 1].tolist()
    property_address = f"{property_address[0]}, {property_address[1]}, {property_address[2]}"
    return property_id, property_capacity, property_address

def random_date(start, end):
    return start + datetime.timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

def generate_order_info(start_date, end_date):
    booking_id = f"{random.randint(10000000, 99999999)}"
    check_in_date = random_date(start_date, end_date)
    days = random.randint(1, 15)
    check_out_date = (check_in_date + datetime.timedelta(days)).strftime('%d-%m-%Y')
    base_fee = days * random.randint(40, 160)
    service_fee = round(base_fee * 0.15, 2)
    cleaning_fee = round(random.uniform(0.8, 2) * base_fee / days, 2)
    gst = round((base_fee + service_fee + cleaning_fee) * 0.1, 2)
    total_price = round(gst * 11, 2)
    return booking_id, check_in_date.strftime('%d-%m-%Y'), check_out_date, base_fee, service_fee, cleaning_fee, gst, total_price

def generate_owner_info():
    owner_id = f"{random.randint(1, 99):02d}{random.randint(100, 999)}"
    abn = f"{random.randint(10, 99)} {random.randint(100, 999)} {random.randint(100, 999)} {random.randint(100, 999)}"
    tin = f"{random.randint(100000000, 999999999)}"
    dob = random_date(datetime.datetime(1940, 1, 1), datetime.datetime(1999, 12, 31)).strftime('%d-%m-%Y')
    bsb = ""
    bank_account_number = ""
    contact_number = f"+614{random.randint(10000000, 99999999)}"
    email = "example@gmail.com"
    name = names.get_full_name()
    rating = random.randint(0, 10)
    bank_account_name = name
    paypal_id = ""
    iban = ""
    swift_code = ""
    if random.random() > 0.2:
        owner_location = "Australia"
        owner_address = postcode[random.randint(0, postcode_data_length) // 1].tolist()
        owner_address = f"{owner_address[0]}, {owner_address[1]}, {owner_address[2]}"
        bank_name = "Commonwealth Bank of Australia"
        bsb = f"062{random.randint(100, 999)}"
        bank_account_number = f"1{random.randint(100, 999)}{random.randint(1000, 9999)}"
        i = random.random()
        if i > 0.55:
            paypal_id = f"{name.replace(' ', '.')}@paypal.com"
        elif i > 0.1:
            paypal_id = f"{contact_number[3:]}@paypal.com"
    else:
        owner_location = "New Zealand"
        owner_address = "Auckland, NZ"
        bank_name = "ANZ Bank"
        iban = f"AU{bank_account_number}"
        swift_code = "CTBAAU2S" #Example
    return owner_id, abn, tin, dob, contact_number, email, rating, owner_location, owner_address, bank_account_name, bsb, bank_account_number, bank_name, paypal_id, iban, swift_code

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
    final_gst = round(final_price / 11, 2)
    final_price = round(final_gst * 11, 2)
    return order_status, final_price, final_gst

def generate_data(num_entries):
    data = []
    start_date = datetime.datetime(2023, 1, 1)
    end_date = datetime.datetime(2023, 6, 30)

    for i in range(num_entries):
        if i % 10000 == 0:
            print(i // 10000)
        property_id, property_capacity, property_address = generate_property_info()
        booking_id, check_in_date, check_out_date, base_fee, service_fee, cleaning_fee, gst, total_price = generate_order_info(start_date, end_date)
        owner_id, abn, tin, dob, contact_number, email, rating, owner_location, owner_address, bank_account_name, bsb, bank_account_number, bank_name, paypal_id, iban, swift_code = generate_owner_info()
        order_status, final_price, final_gst = generate_order_status(total_price)
        abn = abn if random.random() > 0.2 else None  # 80% chance of having ABN
        tin = tin if abn is None else None  # If no ABN, generate TIN

        data.append({
            'property_id': property_id,
            'property_capacity': property_capacity,
            'property_address': property_address,
            'booking_id': booking_id,
            'check_in_date': check_in_date,
            'check_out_date': check_out_date,
            'base_fee': base_fee,
            'service_fee': service_fee,
            'cleaning_fee': cleaning_fee,
            'gst': gst,
            'total_price': total_price,
            'owner_id': owner_id,
            'abn': abn or '',
            'tin': tin or '',
            'dob': dob,
            'contact_number': contact_number,
            'email': email,
            'rating': rating,
            'owner_location': owner_location,
            'owner_address': owner_address,
            'bank_account_name': bank_account_name,
            'bsb': bsb,
            'bank_account_number': bank_account_number,
            'bank_name': bank_name,
            'paypal_id': paypal_id,
            'iban': iban,
            'swift_code': swift_code,
            'order_status': order_status,
            'final_price': final_price,
            'final_gst': final_gst,
        })
        
        # Write batch to CSV
        if len(data) >= BATCH_SIZE:
            write_to_csv(data)
            data = []

    # Write any remaining data
    if data:
        write_to_csv(data)

def write_to_csv(data):
    with open('sample_data1.csv', 'a', newline='') as csvfile:
        fieldnames = ['property_id', 'property_capacity', 'property_address', 'booking_id',
                      'check_in_date', 'check_out_date', 'base_fee', 'service_fee', 'cleaning_fee',
                      'gst', 'total_price', 'owner_id', 'abn', 'tin', 'dob', 'contact_number',
                      'email', 'rating', 'owner_location', 'owner_address', 'bank_account_name',
                      'bsb', 'bank_account_number', 'bank_name','paypal_id', 'iban', 'swift_code', 
                      'order_status', 'final_price', 'final_gst']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if csvfile.tell() == 0:  # Check if file is empty to write the header
            writer.writeheader()

        writer.writerows(data)

# Generate sample data
generate_data(NUM_ENTRIES)

print(f'Sample data with {NUM_ENTRIES} entries.')
