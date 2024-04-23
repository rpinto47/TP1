import multiprocessing
import time

def is_prime(n):
    """Check if n is prime."""
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def find_max_prime(start, end, result_queue):
    max_prime = 2
    for i in range(start, end, 2):
        if is_prime(i):
            max_prime = i
    result_queue.put(max_prime)

def find_max_prime_multiprocess(timeout):
    result_queue = multiprocessing.Queue()
    num_processes = 4
    processes = []

    chunk_size = 10000
    start = 3
    end = start + chunk_size

    start_time = time.time()

    while time.time() - start_time < timeout:
        for _ in range(num_processes):
            p = multiprocessing.Process(target=find_max_prime, args=(start, end, result_queue))
            processes.append(p)
            p.start()
            start = end + 1
            end = start + chunk_size

        for p in processes:
            p.join()

        max_prime = 2
        while not result_queue.empty():
            prime = result_queue.get()
            if prime > max_prime:
                max_prime = prime

    print("Maior valor primo: ", max_prime)

if __name__ == '__main__':
    find_max_prime_multiprocess(5)
