import time
import multiprocessing
from multiprocessing import Pool


def is_prime(n):
    """Check if a number is prime with optimized checks."""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    limit = int(n ** 0.5) + 1
    for i in range(5, limit, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True


def worker(start, end, timeout):
    """Worker function to find primes within a range with a timeout."""
    local_max = 1
    start_time = time.time()

    i = start
    while i < end and (time.time() - start_time) < timeout:
        if is_prime(i) and i > local_max:
            local_max = i
        i += 1

    return local_max


def find_max_prime(max_num, process_number, timeout):
    """Find the largest prime within a given range using multiple processes with a timeout."""
    step = max_num // process_number
    intervals = [(i * step, (i + 1) * step, timeout) for i in range(process_number)]

    with Pool(process_number) as pool:
        results = pool.starmap(worker, intervals)

    max_prime = max(results)

    print("Max prime found:", max_prime)
    print("Number of digits:", len(str(max_prime)))
    print("Timeout:", timeout, "seconds")


if __name__ == '__main__':
    try:
        max_num = int(input("Enter the maximum number to check for primes: "))
        process_number = int(input("Enter the number of processes to use: "))
        timeout = float(input("Enter the timeout in seconds: "))

        # Default to the number of CPU cores if process_number is zero or less
        if process_number <= 0:
            process_number = multiprocessing.cpu_count()

        if max_num <= 2:
            raise ValueError("Maximum number must be greater than 2.")

        if timeout <= 0:
            raise ValueError("Timeout must be greater than zero.")

        find_max_prime(max_num, process_number, timeout)

    except ValueError as e:
        print("Invalid input:", e)
