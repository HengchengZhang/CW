import csv
import random
import datetime

# Function to generate random dates
def random_date(start, end):
    return start + datetime.timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )

# Function to generate random ABNs
def generate_abn():
    return f"{random.randint(10, 99)} {random.randint(100, 999)} {random.randint(100, 999)} {random.randint(100, 999)}"

# Function to generate random TINs
def generate_tin():
    return f"{random.randint(100000000, 999999999)}"

# Function to generate random participant names
def generate_name():
    first_names = ['John', 'Jane', 'Alex', 'Emily', 'Michael', 'Sarah', 'David', 'Laura']
    last_names = ['Smith', 'Jones', 'Williams', 'Taylor', 'Brown', 'Lee', 'Wilson', 'Martin']
    return f"{random.choice(first_names)} {random.choice(last_names)}"

# Function to generate random addresses
def generate_address():
    street_names = ['Main St', 'High St', 'Park Ave', 'Church St', 'Market St', 'Victoria Rd']
    suburbs = ['Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide', 'Hobart']
    return f"{random.randint(1, 999)} {random.choice(street_names)}, {random.choice(suburbs)}"

# Function to generate random postcodes
def generate_postcode():
    return f"{random.randint(2000, 7999)}"

# Function to calculate GST (10% of amount if positive)
def calculate_gst(amount):
    return round(amount * 0.1, 2) if amount > 0 else 0.0

# Function to introduce errors into the data
def introduce_error(value, error_rate):
    if random.random() < error_rate:
        if isinstance(value, str):
            # Introduce error in strings by either removing or altering characters
            return value[:-1] if len(value) > 1 else ""
        elif isinstance(value, float) or isinstance(value, int):
            # Introduce error in numbers by setting them to None or a clearly incorrect value
            return None if random.random() < 0.5 else "error"
    return value

# Function to generate random transaction data
def generate_data(num_entries, cancel_rate=0.1, error_rate=0.05):
    data = []
    service_types = [
        'Ride-sharing: Driving passengers to their destinations',
        'Accommodation: Short-term property rental',
        'Freelancing: Web development',
        'Goods Rental: Renting out camera equipment',
        'Task Service: Home cleaning services'
    ]
    start_date = datetime.datetime.strptime('2023-01-01', '%Y-%m-%d')
    end_date = datetime.datetime.strptime('2023-12-31', '%Y-%m-%d')

    for _ in range(num_entries):
        transaction_id = random.randint(100000, 999999)
        participant_id = random.randint(10000, 99999)
        transaction_date = random_date(start_date, end_date).strftime('%Y-%m-%d')
        amount = round(random.uniform(10.0, 500.0), 2)
        gst = calculate_gst(amount)
        service_type = random.choice(service_types)
        abn = generate_abn() if random.random() > 0.2 else None  # 80% chance of having ABN
        tin = generate_tin() if abn is None else None  # If no ABN, generate TIN
        name = generate_name()
        address = generate_address()
        postcode = generate_postcode()

        # Introduce canceled orders with negative amounts
        if random.random() < cancel_rate:
            amount = -amount
        
        # Introduce errors based on error rate
        transaction_id = introduce_error(transaction_id, error_rate)
        participant_id = introduce_error(participant_id, error_rate)
        transaction_date = introduce_error(transaction_date, error_rate)
        amount = introduce_error(amount, error_rate)
        gst = introduce_error(gst, error_rate)
        service_type = introduce_error(service_type, error_rate)
        abn = introduce_error(abn, error_rate) if abn else ""
        tin = introduce_error(tin, error_rate) if tin else ""
        name = introduce_error(name, error_rate)
        address = introduce_error(address, error_rate)
        postcode = introduce_error(postcode, error_rate)

        data.append([transaction_id, participant_id, transaction_date, amount, gst, service_type, abn, tin, name, address, postcode])
    
    return data

# Number of sample entries to generate
num_entries = 100
# Error rate
error_rate = 0.05  # 5% error rate

# Generate sample data
sample_data = generate_data(num_entries, error_rate=error_rate)

# Write data to CSV file
with open('serr_sample_data.csv', 'w', newline='') as csvfile:
    fieldnames = ['TransactionID', 'ParticipantID', 'TransactionDate', 'Amount', 'GST', 'ServiceType', 'ABN', 'TIN', 'ParticipantName', 'Address', 'Postcode']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for row in sample_data:
        writer.writerow({
            'TransactionID': row[0],
            'ParticipantID': row[1],
            'TransactionDate': row[2],
            'Amount': row[3],
            'GST': row[4],
            'ServiceType': row[5],
            'ABN': row[6] if row[6] else '',
            'TIN': row[7] if row[7] else '',
            'ParticipantName': row[8],
            'Address': row[9],
            'Postcode': row[10]
        })

print(f'Sample data with {num_entries} entries and {error_rate*100}% error rate.')
