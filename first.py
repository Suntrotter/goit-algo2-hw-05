# Task 1: Password Uniqueness Check Using Bloom Filter

import hashlib
from typing import List, Dict

class BloomFilter:
    def __init__(self, size: int, num_hashes: int):
        # Initialize Bloom filter with given size and number of hash functions
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def _get_hashes(self, item: str) -> List[int]:
        # Generate multiple hash values for the given item
        hashes = []
        for i in range(self.num_hashes):
            hash_val = int(hashlib.md5((item + str(i)).encode()).hexdigest(), 16)
            hashes.append(hash_val % self.size)
        return hashes

    def add(self, item: str):
        # Add item to Bloom filter
        if not isinstance(item, str) or not item.strip():
            return
        for hash_index in self._get_hashes(item):
            self.bit_array[hash_index] = 1

    def __contains__(self, item: str) -> bool:
        # Check if item is possibly in Bloom filter
        if not isinstance(item, str) or not item.strip():
            return False
        return all(self.bit_array[hash_index] for hash_index in self._get_hashes(item))

def check_password_uniqueness(bloom_filter: BloomFilter, passwords: List[str]) -> Dict[str, str]:
    # Check uniqueness of passwords using Bloom filter
    results = {}
    for password in passwords:
        if not isinstance(password, str) or not password.strip():
            results[password] = "некоректний пароль"  # invalid password
            continue
        if password in bloom_filter:
            results[password] = "вже використаний"  # already used
        else:
            results[password] = "унікальний"  # unique
            bloom_filter.add(password)
    return results

# Example usage
if __name__ == "__main__":
    # Initialize Bloom filter
    bloom = BloomFilter(size=1000, num_hashes=3)

    # Add existing passwords to the filter
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    # Check new passwords for uniqueness
    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest"]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    # Print the results
    for password, status in results.items():
        print(f"Пароль '{password}' — {status}.")
