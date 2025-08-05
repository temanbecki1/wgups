from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import datetime
import os
from hash_table import ChainingHashTable

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Global variables to store data
package_hash_table = None
distance_matrix = None
address_list = None
trucks = []

def load_package_data(filename, hash_table):
    """Load package data from CSV file into the hash table."""
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        for row in reader:
            package_id = int(row[0])
            package_data = [
                row[1],  # address
                row[5],  # deadline
                row[2],  # city
                row[4],  # zip
                row[6],  # weight
                "At the hub",  # initial status
                None,  # departure_time
                None   # delivery_time
            ]
            hash_table.insert(package_id, package_data)

def load_distance_data(filename):
    """Load distance data from CSV file into a 2D matrix."""
    distance_matrix = []
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            distance_row = []
            for distance in row:
                if distance.strip():
                    distance_row.append(float(distance))
                else:
                    distance_row.append(0.0)
            distance_matrix.append(distance_row)
    return distance_matrix

def load_address_data(filename):
    """Load address data from CSV file into a list."""
    addresses = []
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        for row in reader:
            addresses.append(row[1])
    return addresses

def get_address_index(address, address_list):
    """Get the index of an address in the address list."""
    try:
        return address_list.index(address)
    except ValueError:
        for i, addr in enumerate(address_list):
            if address.lower() in addr.lower() or addr.lower() in address.lower():
                return i
        return 0

def get_distance(from_index, to_index, distance_matrix):
    """Get distance between two locations from the distance matrix."""
    if from_index < len(distance_matrix) and to_index < len(distance_matrix[from_index]):
        distance = distance_matrix[from_index][to_index]
        if distance == 0.0 and from_index != to_index:
            distance = distance_matrix[to_index][from_index]
        return distance
    return 0.0

def deliver_packages(truck, package_hash_table, distance_matrix, address_list, current_time):
    """Implement nearest neighbor algorithm to deliver packages for a single truck."""
    truck_time = current_time
    
    # Set departure time for all packages on this truck
    for package_id in truck['packages']:
        package_data = package_hash_table.lookup(package_id)
        if package_data:
            package_data[6] = truck_time
    
    # Continue until all packages are delivered
    packages_to_deliver = truck['packages'].copy()
    while packages_to_deliver:
        nearest_distance = float('inf')
        nearest_package_id = None
        nearest_package_index = None
        
        for package_id in packages_to_deliver:
            package_data = package_hash_table.lookup(package_id)
            if package_data:
                package_address = package_data[0]
                
                # Handle Package #9 constraint
                if package_id == 9:
                    time_1020 = datetime.timedelta(hours=10, minutes=20)
                    if truck_time >= time_1020:
                        package_data[0] = "410 S State St"
                        package_address = package_data[0]
                    elif len(packages_to_deliver) > 1:
                        continue
                
                package_index = get_address_index(package_address, address_list)
                distance = get_distance(truck['current_location'], package_index, distance_matrix)
                
                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_package_id = package_id
                    nearest_package_index = package_index
        
        if nearest_package_id is not None:
            truck['mileage'] += nearest_distance
            truck['current_location'] = nearest_package_index
            
            travel_time_hours = nearest_distance / 18
            travel_time = datetime.timedelta(hours=travel_time_hours)
            truck_time += travel_time
            
            package_data = package_hash_table.lookup(nearest_package_id)
            if package_data:
                package_data[5] = "Delivered"
                package_data[7] = truck_time
            
            packages_to_deliver.remove(nearest_package_id)
    
    return truck_time

def initialize_data():
    """Initialize the routing data and run simulation."""
    global package_hash_table, distance_matrix, address_list, trucks
    
    try:
        package_hash_table = ChainingHashTable()
        load_package_data('WGUPS_Package_File.csv', package_hash_table)
        distance_matrix = load_distance_data('WGUPS_Distance_Table.csv')
        address_list = load_address_data('WGUPS_Address_File.csv')
        
        # Create trucks with package assignments
        trucks = [
            {
                'id': 1,
                'packages': [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40],
                'mileage': 0.0,
                'current_location': 0,
                'departure_time': datetime.timedelta(hours=8, minutes=0)
            },
            {
                'id': 2,
                'packages': [3, 6, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39],
                'mileage': 0.0,
                'current_location': 0,
                'departure_time': datetime.timedelta(hours=9, minutes=5)
            },
            {
                'id': 3,
                'packages': [2, 4, 5, 7, 8, 9, 10, 11, 25, 28, 32, 33],
                'mileage': 0.0,
                'current_location': 0,
                'departure_time': None
            }
        ]
        
        # Run simulation
        truck1_return = deliver_packages(trucks[0], package_hash_table, distance_matrix, address_list, trucks[0]['departure_time'])
        truck2_return = deliver_packages(trucks[1], package_hash_table, distance_matrix, address_list, trucks[1]['departure_time'])
        trucks[2]['departure_time'] = truck1_return
        truck3_return = deliver_packages(trucks[2], package_hash_table, distance_matrix, address_list, trucks[2]['departure_time'])
        
        return True
    except Exception as e:
        print(f"Error initializing data: {e}")
        return False

@app.route('/api/package/<int:package_id>')
def get_package(package_id):
    """Get package information by ID."""
    if not package_hash_table:
        return jsonify({'error': 'Data not initialized'}), 500
    
    package_data = package_hash_table.lookup(package_id)
    if not package_data:
        return jsonify({'error': 'Package not found'}), 404
    
    return jsonify({
        'id': package_id,
        'address': package_data[0],
        'deadline': package_data[1],
        'city': package_data[2],
        'zip': package_data[3],
        'weight': package_data[4],
        'status': package_data[5],
        'departure_time': str(package_data[6]) if package_data[6] else None,
        'delivery_time': str(package_data[7]) if package_data[7] else None
    })

@app.route('/api/package/<int:package_id>/status')
def get_package_status_at_time(package_id):
    """Get package status at a specific time."""
    time_str = request.args.get('time')
    if not time_str:
        return jsonify({'error': 'Time parameter required (HH:MM format)'}), 400
    
    try:
        hour, minute = map(int, time_str.split(':'))
        query_time = datetime.timedelta(hours=hour, minutes=minute)
    except:
        return jsonify({'error': 'Invalid time format. Use HH:MM'}), 400
    
    if not package_hash_table:
        return jsonify({'error': 'Data not initialized'}), 500
    
    package_data = package_hash_table.lookup(package_id)
    if not package_data:
        return jsonify({'error': 'Package not found'}), 404
    
    departure_time = package_data[6] if package_data[6] else datetime.timedelta(hours=8)
    delivery_time = package_data[7] if package_data[7] else datetime.timedelta(hours=17)
    
    if query_time < departure_time:
        status = "At the hub"
    elif departure_time <= query_time < delivery_time:
        status = "En route"
    else:
        status = f"Delivered at {delivery_time}"
    
    return jsonify({
        'id': package_id,
        'status': status,
        'query_time': time_str,
        'departure_time': str(departure_time),
        'delivery_time': str(delivery_time) if package_data[7] else None
    })

@app.route('/api/packages/status')
def get_all_packages_status():
    """Get status of all packages at a specific time."""
    time_str = request.args.get('time')
    if not time_str:
        return jsonify({'error': 'Time parameter required (HH:MM format)'}), 400
    
    try:
        hour, minute = map(int, time_str.split(':'))
        query_time = datetime.timedelta(hours=hour, minutes=minute)
    except:
        return jsonify({'error': 'Invalid time format. Use HH:MM'}), 400
    
    if not package_hash_table:
        return jsonify({'error': 'Data not initialized'}), 500
    
    packages = []
    for package_id in range(1, 41):
        package_data = package_hash_table.lookup(package_id)
        if package_data:
            departure_time = package_data[6] if package_data[6] else datetime.timedelta(hours=8)
            delivery_time = package_data[7] if package_data[7] else datetime.timedelta(hours=17)
            
            if query_time < departure_time:
                status = "At the hub"
            elif departure_time <= query_time < delivery_time:
                status = "En route"
            else:
                status = f"Delivered at {delivery_time}"
            
            # Find which truck this package is on
            truck_id = None
            for truck in trucks:
                if package_id in truck['packages']:
                    truck_id = truck['id']
                    break
            
            packages.append({
                'id': package_id,
                'address': package_data[0],
                'deadline': package_data[1],
                'city': package_data[2],
                'zip': package_data[3],
                'weight': package_data[4],
                'status': status,
                'truck_id': truck_id,
                'departure_time': str(departure_time),
                'delivery_time': str(delivery_time) if package_data[7] else None
            })
    
    return jsonify({
        'packages': packages,
        'query_time': time_str
    })

@app.route('/api/trucks')
def get_trucks():
    """Get information about all trucks."""
    if not trucks:
        return jsonify({'error': 'Data not initialized'}), 500
    
    truck_info = []
    for truck in trucks:
        truck_info.append({
            'id': truck['id'],
            'packages': truck['packages'],
            'mileage': truck['mileage'],
            'departure_time': str(truck['departure_time']) if truck['departure_time'] else None
        })
    
    return jsonify({'trucks': truck_info})

@app.route('/api/total-mileage')
def get_total_mileage():
    """Get total mileage for all trucks."""
    if not trucks:
        return jsonify({'error': 'Data not initialized'}), 500
    
    total_mileage = sum(truck['mileage'] for truck in trucks)
    return jsonify({
        'total_mileage': total_mileage,
        'individual_mileage': [{'truck_id': truck['id'], 'mileage': truck['mileage']} for truck in trucks]
    })

@app.route('/api/initialize')
def initialize():
    """Initialize or reinitialize the routing data."""
    success = initialize_data()
    if success:
        return jsonify({'message': 'Data initialized successfully'})
    else:
        return jsonify({'error': 'Failed to initialize data'}), 500

if __name__ == '__main__':
    print("Initializing WGUPS routing data...")
    if initialize_data():
        print("Data initialized successfully!")
        print("Starting Flask server...")
        app.run(debug=True, port=5000)
    else:
        print("Failed to initialize data. Please check your CSV files.") 