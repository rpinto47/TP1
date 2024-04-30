import time
import multiprocessing
from multiprocessing import Pool


def is_prime(n):
    """
    Check if a given number `n` is prime.

    This function uses an optimized method to determine if `n` is a prime number.
    It checks for divisibility by 2 and 3, and then checks odd numbers
    using a step size of 6 for efficiency.

    Args:
        n (int): The number to check for primality.

    Returns:
        bool: True if `n` is a prime number, False otherwise.
    """
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
    """
    Find the largest prime number within a specified range and within a given timeout.

    This function iterates through numbers from `start` to `end`, checking for primes.
    It stops if it finds a prime greater than `local_max`, or if it exceeds the timeout.

    Args:
        start (int): The start of the range.
        end (int): The end of the range.
        timeout (float): The maximum time allowed for this process in seconds.

    Returns:
        int: The largest prime found within the specified range and timeout.
    """
    local_max = 1
    start_time = time.time()

    i = start
    while i < end and (time.time() - start_time) < timeout:
        if is_prime(i) and i > local_max:
            local_max = i
        i += 1

    return local_max


def find_max_prime(max_num, process_number, timeout):
    """
    Find the largest prime number in the range from 1 to `max_num` using multiple processes.

    This function creates `process_number` processes, each responsible for a different range
    of numbers, to find the largest prime. The range is divided into segments, and each process
    has a timeout for safety.

    Args:
        max_num (int): The upper limit of the range to check for primes.
        process_number (int): The number of processes to use for parallel computation.
        timeout (float): The maximum time allowed for each process in seconds.

    Returns:
        None: This function prints the maximum prime found, its number of digits, and the timeout used.
    """
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

        if process_number <= 0:
            process_number = multiprocessing.cpu_count()

        if max_num <= 2 or timeout <= 0:
            raise ValueError("Maximum number must be greater than 2 and timeout must be greater than zero.")

        find_max_prime(max_num, process_number, timeout)

    except ValueError as e:
        print("Invalid input:", e)
