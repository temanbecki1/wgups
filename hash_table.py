class ChainingHashTable:
    """
    Custom hash table implementation using chaining for collision resolution.
    Designed specifically for WGUPS package data storage.
    """
    
    def __init__(self, initial_capacity=40):
        """
        Initialize hash table with specified capacity.
        Creates empty buckets (lists) for chaining collision resolution.
        
        Args:
            initial_capacity (int): Number of buckets in the hash table
        """
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])
    
    def insert(self, key, value):
        """
        Insert or update a key-value pair in the hash table.
        
        Args:
            key: The package ID (used for hashing)
            value: List containing all package details
        """
        # Calculate hash to determine bucket
        bucket_index = hash(key) % len(self.table)
        bucket = self.table[bucket_index]
        
        # Check if key already exists in bucket
        for i, key_value_pair in enumerate(bucket):
            if key_value_pair[0] == key:
                # Update existing value
                key_value_pair[1] = value
                return
        
        # Key doesn't exist, append new key-value pair
        bucket.append([key, value])
    
    def lookup(self, key):
        """
        Retrieve value associated with given key.
        
        Args:
            key: The package ID to search for
            
        Returns:
            The value (package details) if found, None otherwise
        """
        # Calculate hash to determine bucket
        bucket_index = hash(key) % len(self.table)
        bucket = self.table[bucket_index]
        
        # Search through bucket for matching key
        for key_value_pair in bucket:
            if key_value_pair[0] == key:
                return key_value_pair[1]
        
        # Key not found
        return None 