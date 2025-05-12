# Task 2: Comparison of Exact Count vs HyperLogLog Approximation
from typing import List, Dict
from first import BloomFilter, check_password_uniqueness
import time
from datasketch import HyperLogLog
import re

def exact_count(ip_list: List[str]) -> int:
    return len(set(ip_list))

def approximate_count(ip_list: List[str], hll_precision: int = 12) -> int:
    hll = HyperLogLog(p=hll_precision)
    for ip in ip_list:
        hll.update(ip.encode('utf8'))
    return int(hll.count())

def read_ip_addresses(filename: str) -> list[str]:
    ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
    ip_list = []

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            match = ip_pattern.search(line)
            if match:
                ip_list.append(match.group())

    return ip_list

if __name__ == "__main__":
    # Task 1 Example usage
    bloom = BloomFilter(size=1000, num_hashes=3)
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest"]
    results = check_password_uniqueness(bloom, new_passwords_to_check)
    for password, status in results.items():
        print(f"Пароль '{password}' — {status}.")

    # Task 2 Example usage
    ip_data = read_ip_addresses("lms-stage-access.log")

    start = time.time()
    exact = exact_count(ip_data)
    exact_time = time.time() - start

    start = time.time()
    approx = approximate_count(ip_data)
    approx_time = time.time() - start

    print("\nComparison Results:")
    print(f"{'Method':<30}{'Unique Count':<20}{'Time (s)':<10}")
    print(f"{'Exact Count':<30}{exact:<20}{exact_time:<10.4f}")
    print(f"{'HyperLogLog Approximation':<30}{approx:<20}{approx_time:<10.4f}")
