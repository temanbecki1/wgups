WGUPS Routing Program: Incremental Build Guide

This guide breaks down the development of the WGUPS program into five distinct, committable steps. Each step results in a stable, functional addition to the project.

Step 1: Foundational Data Structure (Commit #1)

Goal: Create the custom hash table required by the project constraints. This is the foundation for all data management.

Instructions:

    Create a new file named hash_table.py.

    Inside this file, define a class called ChainingHashTable.

    Implement the __init__ method: This constructor should initialize an empty list to serve as your table. Inside this list, create a set number of "buckets" (e.g., 40), which should also be empty lists.
    Python

    # self.table = []
    # for i in range(initial_capacity):
    #     self.table.append([])

    Implement the insert method: This function should:

        Accept a key (the package ID) and a value (a list of all package details).

        Calculate a hash of the key to determine which bucket to use (e.g., hash(key) % capacity).

        Check if the key already exists in the bucket. If it does, update the existing value.

        If the key doesn't exist, append a new [key, value] pair to the bucket list.

    Implement the lookup method: This function should:

        Accept a key.

        Calculate the hash to find the correct bucket.

        Iterate through the [key, value] pairs in that bucket. If a matching key is found, return its corresponding value.

        If the key is not found after checking the entire bucket, return None.

✅ Commit Point: At this stage, you have a complete, self-contained, and testable hash table module. This is your first commit: "feat: Implement ChainingHashTable for package data storage."

Step 2: Data Loading and Modeling (Commit #2)

Goal: Create the main application file and write the functions necessary to load data from your CSV files into your program's memory.

Instructions:

    Create the main application file, main.py.

    At the very top of main.py, add an identifying comment: # Student ID: [Your Student ID Here].

    Import Python's built-in csv and datetime modules, and import your ChainingHashTable class:
    Python

    from hash_table import ChainingHashTable

    Write load_package_data(): This function takes a filename and your hash table instance as arguments. It should open and read the WGUPS_Package_File.csv, iterate through each row, and use your hash table's insert() method to store the data for all 40 packages. The value for each package should be a list containing all its attributes (address, deadline, weight, status, etc.). Initialize the status as "At the hub".

    Write load_distance_data() and load_address_data(): These helper functions will read the distance and address CSV files. The distance data is best stored as a 2D list (a matrix), and the address data can be a simple list where the index corresponds to the location's ID in the distance matrix.

    Create a Truck class: Define a simple class to model the delivery trucks. It should have attributes like id, packages (a list of package IDs), mileage, current_location, and departure_time.

✅ Commit Point: Your application can now successfully load and structure all necessary data. This is your second commit: "feat: Add data loading from CSV and Truck class model."

Step 3: Implement the Core Routing Algorithm (Commit #3)

Goal: Write the "brains" of the operation—the greedy algorithm that determines the delivery route for a single truck.

Instructions:

    In main.py, define a function called deliver_packages(). This function will accept a truck object, your package_hash_table, and your distance/address data structures.

    Algorithm Logic: Inside this function, implement the nearest neighbor algorithm:

        Start a while loop that continues as long as there are packages on the truck.

        Inside the loop, iterate through every package currently on the truck.

        For each package, calculate the distance from the truck's current_location to the package's delivery address.

        Keep track of the package with the minimum distance. This is your "nearest neighbor."

        Handle the Package #9 constraint: Before choosing the nearest neighbor, check if the current simulation time is past 10:20 AM. If it is, and you are about to deliver package #9, first update its address in the hash table to the correct one. If it's before 10:20 AM, your logic should skip over package #9 unless it's the last one left.

        After the loop finds the nearest package, "travel" to it: update the truck's mileage, advance the simulation time (distance / 18 mph), and set the truck's current_location to the new address.

        Update the delivered package's status in the hash table to "Delivered" and record the delivery time.

        Remove the package from the truck's list of undelivered packages.

✅ Commit Point: You now have a function that can efficiently route one truck. This is your third commit: "feat: Implement nearest neighbor algorithm for package delivery."

Step 4: Orchestrate the Full Simulation (Commit #4)

Goal: Use the algorithm to simulate the entire delivery day for all trucks, ensuring all constraints are met.

Instructions:

    Work within the if __name__ == "__main__": block in main.py.

    Initialize Everything: Create your ChainingHashTable instance, your three Truck instances, and call your data loading functions from Step 2.

    Manual Truck Loading: This is a crucial step that requires a manual heuristic. Based on package constraints (deadlines, "must be on truck 2," delayed flights), manually assign each of the 40 package IDs to one of the three trucks' packages list.

        Strategy Hint: Load packages with early deadlines on Truck 1. Load packages marked "Can only be on truck 2" or "Delayed on flight" on Truck 2 (with a departure after 9:05 AM). The rest, including the packages with the wrong address, can go on Truck 3.

    Set Departure Times: Set the departure_time for Truck 1 (8:00 AM) and Truck 2 (e.g., 9:05 AM).

    Run the Simulation:

        Call deliver_packages() for Truck 1.

        Call deliver_packages() for Truck 2.

        Determine when a driver is free. For simplicity, assume the driver from Truck 1 is free after their route is done. Calculate this return time. Set Truck 3's departure_time to this time.

        Call deliver_packages() for Truck 3.

    Verify the Solution: After all simulations are run, calculate the total mileage from all three trucks and print it to the console to ensure it's under 140 miles.

✅ Commit Point: The core problem is now solved. The application can successfully route all packages and meet constraints. This is your fourth commit: "feat: Orchestrate full-day simulation for all trucks."

Step 5: Build the User Interface (Commit #5)

Goal: Create the user-facing command-line interface (CLI) to look up package status, fulfilling the final project requirement.

Instructions:

    Still inside the if __name__ == "__main__": block, after the simulation completes, start a while True: loop to create a persistent menu.

    Display Menu Options: Print options for the user, such as "1. Look up a single package", "2. View all packages at a specific time", and "3. Exit".

    Handle User Input:

        Prompt the user for their choice and for a specific time (e.g., "Enter time in HH:MM format").

        Convert the user's time string into a datetime.timedelta object for easy comparison.

    Implement Status Logic:

        If the user wants to look up a package, get the package data from the hash table.

        Compare the user's input time against the package's departure_time and delivery_time (which were set during the simulation in Step 4).

            If input_time < departure_time, status is "At the hub".

            If departure_time <= input_time < delivery_time, status is "En route".

            If input_time >= delivery_time, status is "Delivered at [delivery_time]".

        Print the full package details along with its calculated status.

✅ Commit Point: The project is now complete with a functional user interface. This is your final commit: "feat: Add CLI for package status lookups."