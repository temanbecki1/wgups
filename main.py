# Student ID: 012172824

import csv
import datetime
from hash_table import ChainingHashTable


def load_package_data(filename, hash_table):
    """
    Load package data from CSV file into the hash table.
    
    Args:
        filename (str): Path to the package CSV file
        hash_table (ChainingHashTable): Hash table instance to store data
    """
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        for row in reader:
            package_id = int(row[0])
            # Create package data list: [address, deadline, city, zip, weight, status, departure_time, delivery_time]
            package_data = [
                row[1],  # address
                row[5],  # deadline
                row[2],  # city
                row[4],  # zip
                row[6],  # weight
                "At the hub",  # initial status
                None,  # departure_time (to be set later)
                None   # delivery_time (to be set later)
            ]
            hash_table.insert(package_id, package_data)


def load_distance_data(filename):
    """
    Load distance data from CSV file into a 2D matrix.
    
    Args:
        filename (str): Path to the distance CSV file
        
    Returns:
        list: 2D list representing distance matrix
    """
    distance_matrix = []
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # Convert string distances to float, handle empty cells
            distance_row = []
            for distance in row:
                if distance.strip():
                    distance_row.append(float(distance))
                else:
                    distance_row.append(0.0)
            distance_matrix.append(distance_row)
    return distance_matrix


def load_address_data(filename):
    """
    Load address data from CSV file into a list.
    
    Args:
        filename (str): Path to the address CSV file
        
    Returns:
        list: List of addresses where index corresponds to location ID
    """
    addresses = []
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        for row in reader:
            # Address is in the second column (index 1)
            addresses.append(row[1])
    return addresses


class Truck:
    """
    Model for delivery trucks in the WGUPS system.
    """
    
    def __init__(self, truck_id):
        """
        Initialize a truck with default values.
        
        Args:
            truck_id (int): Unique identifier for the truck
        """
        self.id = truck_id
        self.packages = []  # List of package IDs assigned to this truck
        self.mileage = 0.0  # Total miles traveled
        self.current_location = 0  # Current location index (0 = hub)
        self.departure_time = None  # When truck leaves the hub
        self.speed = 18  # Miles per hour


def get_address_index(address, address_list):
    """
    Get the index of an address in the address list.
    
    Args:
        address (str): Address to find
        address_list (list): List of addresses
        
    Returns:
        int: Index of the address, or 0 if not found
    """
    try:
        return address_list.index(address)
    except ValueError:
        # If exact match not found, try partial matching
        for i, addr in enumerate(address_list):
            if address.lower() in addr.lower() or addr.lower() in address.lower():
                return i
        return 0  # Default to hub if not found


def get_distance(from_index, to_index, distance_matrix):
    """
    Get distance between two locations from the distance matrix.
    
    Args:
        from_index (int): Starting location index
        to_index (int): Destination location index
        distance_matrix (list): 2D distance matrix
        
    Returns:
        float: Distance between locations
    """
    # Distance matrix is symmetric, so we can use either direction
    if from_index < len(distance_matrix) and to_index < len(distance_matrix[from_index]):
        distance = distance_matrix[from_index][to_index]
        if distance == 0.0 and from_index != to_index:
            # Try the other direction if one is 0
            distance = distance_matrix[to_index][from_index]
        return distance
    return 0.0


def deliver_packages(truck, package_hash_table, distance_matrix, address_list, current_time):
    """
    Implement nearest neighbor algorithm to deliver packages for a single truck.
    
    Args:
        truck (Truck): Truck object with packages to deliver
        package_hash_table (ChainingHashTable): Hash table containing package data
        distance_matrix (list): 2D distance matrix
        address_list (list): List of addresses
        current_time (datetime.timedelta): Current simulation time
        
    Returns:
        datetime.timedelta: Time when truck finishes deliveries
    """
    truck_time = current_time
    
    # Set departure time for all packages on this truck
    for package_id in truck.packages:
        package_data = package_hash_table.lookup(package_id)
        if package_data:
            package_data[6] = truck_time  # Set departure_time
    
    # Continue until all packages are delivered
    while truck.packages:
        nearest_distance = float('inf')
        nearest_package_id = None
        nearest_package_index = None
        
        # Find the nearest undelivered package
        for package_id in truck.packages:
            package_data = package_hash_table.lookup(package_id)
            if package_data:
                package_address = package_data[0]  # address
                
                # Handle Package #9 constraint (wrong address until 10:20 AM)
                if package_id == 9:
                    time_1020 = datetime.timedelta(hours=10, minutes=20)
                    if truck_time >= time_1020:
                        # Update to correct address after 10:20 AM
                        package_data[0] = "410 S State St"
                        package_address = package_data[0]
                    elif len(truck.packages) > 1:
                        # Skip package 9 if it's not the last one and before 10:20 AM
                        continue
                
                # Get address index and calculate distance
                package_index = get_address_index(package_address, address_list)
                distance = get_distance(truck.current_location, package_index, distance_matrix)
                
                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_package_id = package_id
                    nearest_package_index = package_index
        
        # Deliver the nearest package
        if nearest_package_id is not None:
            # Update truck mileage and location
            truck.mileage += nearest_distance
            truck.current_location = nearest_package_index
            
            # Calculate travel time and update current time
            travel_time_hours = nearest_distance / truck.speed
            travel_time = datetime.timedelta(hours=travel_time_hours)
            truck_time += travel_time
            
            # Update package status to delivered
            package_data = package_hash_table.lookup(nearest_package_id)
            if package_data:
                package_data[5] = "Delivered"  # status
                package_data[7] = truck_time   # delivery_time
            
            # Remove package from truck
            truck.packages.remove(nearest_package_id)
    
    return truck_time


if __name__ == "__main__":
    print("WGUPS Routing Program")
    print("Initializing data structures...")
    
    # Initialize hash table and load data
    package_hash_table = ChainingHashTable()
    
    # Load data from CSV files
    try:
        load_package_data('WGUPS_Package_File.csv', package_hash_table)
        distance_matrix = load_distance_data('WGUPS_Distance_Table.csv')
        address_list = load_address_data('WGUPS_Address_File.csv')
        print("Data loaded successfully from CSV files!")
    except FileNotFoundError as e:
        print(f"Error: Could not find CSV file - {e}")
        print("Please ensure all CSV files are in the current directory.")
        exit(1)
    
    # Create three truck instances
    truck1 = Truck(1)
    truck2 = Truck(2)
    truck3 = Truck(3)
    
    # Manual truck loading based on package constraints
    # Strategy: Early deadlines on Truck 1, special constraints on Truck 2, rest on Truck 3
    
    # Truck 1: Packages with early deadlines (8:00 AM departure)
    truck1.packages = [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40]
    truck1.departure_time = datetime.timedelta(hours=8, minutes=0)
    
    # Truck 2: "Must be on truck 2" and delayed packages (9:05 AM departure)
    truck2.packages = [3, 6, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39]
    truck2.departure_time = datetime.timedelta(hours=9, minutes=5)
    
    # Truck 3: Remaining packages including wrong address package #9
    truck3.packages = [2, 4, 5, 7, 8, 9, 10, 11, 25, 28, 32, 33]
    # Truck 3 departure time will be set after Truck 1 returns
    
    print("Truck loading complete:")
    print(f"Truck 1: {len(truck1.packages)} packages, departure: 8:00 AM")
    print(f"Truck 2: {len(truck2.packages)} packages, departure: 9:05 AM") 
    print(f"Truck 3: {len(truck3.packages)} packages, departure: TBD")
    
    # Simulate the delivery day
    print("\nStarting delivery simulation...")
    
    # Deliver packages for Truck 1
    print("Truck 1 departing...")
    truck1_return_time = deliver_packages(truck1, package_hash_table, distance_matrix, address_list, truck1.departure_time)
    print(f"Truck 1 completed route at {truck1_return_time}, mileage: {truck1.mileage:.2f}")
    
    # Deliver packages for Truck 2
    print("Truck 2 departing...")
    truck2_return_time = deliver_packages(truck2, package_hash_table, distance_matrix, address_list, truck2.departure_time)
    print(f"Truck 2 completed route at {truck2_return_time}, mileage: {truck2.mileage:.2f}")
    
    # Truck 3 departs when driver from Truck 1 returns
    truck3.departure_time = truck1_return_time
    print(f"Truck 3 departing at {truck3.departure_time}...")
    truck3_return_time = deliver_packages(truck3, package_hash_table, distance_matrix, address_list, truck3.departure_time)
    print(f"Truck 3 completed route at {truck3_return_time}, mileage: {truck3.mileage:.2f}")
    
    # Calculate total mileage
    total_mileage = truck1.mileage + truck2.mileage + truck3.mileage
    print(f"\nTotal mileage for all trucks: {total_mileage:.2f} miles")
    
    if total_mileage < 140:
        print("SUCCESS: Total mileage is under 140 miles!")
    else:
        print("WARNING: Total mileage exceeds 140 miles - optimization needed")
    
    print("\nDelivery simulation complete!")
    
    # Step 5: CLI Interface for Package Status Lookups
    print("\n" + "="*50)
    print("WGUPS Package Tracking System")
    print("="*50)
    
    while True:
        print("\nMenu Options:")
        print("1. Look up a single package")
        print("2. View all packages at a specific time")
        print("3. Exit")
        
        try:
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == '3':
                print("Thank you for using WGUPS Package Tracking System!")
                break
            elif choice == '1':
                # Single package lookup
                try:
                    package_id = int(input("Enter package ID (1-40): "))
                    if package_id < 1 or package_id > 40:
                        print("Invalid package ID. Please enter a number between 1 and 40.")
                        continue
                    
                    time_input = input("Enter time in HH:MM format (24-hour): ").strip()
                    hour, minute = map(int, time_input.split(':'))
                    input_time = datetime.timedelta(hours=hour, minutes=minute)
                    
                    # Get package data from hash table
                    package_data = package_hash_table.lookup(package_id)
                    if package_data:
                        # Calculate status based on time
                        departure_time = package_data[6] if package_data[6] else datetime.timedelta(hours=8)
                        delivery_time = package_data[7] if package_data[7] else datetime.timedelta(hours=17)
                        
                        if input_time < departure_time:
                            status = "At the hub"
                        elif departure_time <= input_time < delivery_time:
                            status = "En route"
                        else:
                            status = f"Delivered at {delivery_time}"
                        
                        # Display package information
                        print(f"\n--- Package {package_id} Status ---")
                        print(f"Address: {package_data[0]}")
                        print(f"Deadline: {package_data[1]}")
                        print(f"City: {package_data[2]}")
                        print(f"Zip: {package_data[3]}")
                        print(f"Weight: {package_data[4]} kg")
                        print(f"Status at {time_input}: {status}")
                    else:
                        print("Package not found in system.")
                        
                except ValueError:
                    print("Invalid input format. Please use HH:MM format for time.")
                except Exception as e:
                    print(f"Error: {e}")
            
            elif choice == '2':
                # All packages at specific time
                try:
                    time_input = input("Enter time in HH:MM format (24-hour): ").strip()
                    hour, minute = map(int, time_input.split(':'))
                    input_time = datetime.timedelta(hours=hour, minutes=minute)
                    
                    print(f"\n--- All Package Status at {time_input} ---")
                    print(f"{'ID':<4} {'Address':<25} {'Deadline':<10} {'Weight':<8} {'Status':<20}")
                    print("-" * 75)
                    
                    for package_id in range(1, 41):
                        package_data = package_hash_table.lookup(package_id)
                        if package_data:
                            # Calculate status based on time
                            departure_time = package_data[6] if package_data[6] else datetime.timedelta(hours=8)
                            delivery_time = package_data[7] if package_data[7] else datetime.timedelta(hours=17)
                            
                            if input_time < departure_time:
                                status = "At the hub"
                            elif departure_time <= input_time < delivery_time:
                                status = "En route"
                            else:
                                status = f"Delivered at {delivery_time}"
                            
                            # Truncate address for display
                            address = package_data[0][:24] if len(package_data[0]) > 24 else package_data[0]
                            
                            print(f"{package_id:<4} {address:<25} {package_data[1]:<10} {package_data[4]:<8} {status:<20}")
                        else:
                            print(f"{package_id:<4} {'Not found':<25} {'':<10} {'':<8} {'Error':<20}")
                            
                except ValueError:
                    print("Invalid input format. Please use HH:MM format for time.")
                except Exception as e:
                    print(f"Error: {e}")
            
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
                
        except KeyboardInterrupt:
            print("\nExiting WGUPS Package Tracking System...")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            print("Please try again.") 