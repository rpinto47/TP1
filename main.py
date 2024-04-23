import time
import multiprocessing

def is_prime(n):
    """Check if n is prime."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def find_max_prime(max_time, result_list):
    """Find the largest prime within a timeout."""
    max_prime = 0
    start_time = time.time()
    current_number = 1
    while time.time() - start_time < max_time:
        if is_prime(current_number):
            max_prime = current_number
        current_number += 1
    result_list.append(max_prime)

def find_max_prime_parallel(timeout):
    """Finds the largest prime within a timeout using parallel processing."""
    start_time = time.time()
    num_processes = 4
    processes = []
    result_list = []

    # Criação dos processos
    for _ in range(num_processes):
        process = multiprocessing.Process(target=find_max_prime, args=(timeout, result_list))
        processes.append(process)
        process.start()

    # Espera os processos terminarem ou até o tempo limite
    for process in processes:
        process.join(timeout=timeout - (time.time() - start_time))

    # Encerra processos que ainda estiverem em execução após o tempo limite
    for process in processes:
        if process.is_alive():
            process.terminate()

    # Encontra o maior número primo
    if result_list:
        max_prime = max(result_list)
        print("Largest prime found:", max_prime)
    else:
        print("No prime numbers found within the timeout.")

if __name__ == '__main__':
    find_max_prime_parallel(5)
