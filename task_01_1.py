import random
import time
from functools import lru_cache


def range_sum_no_cache(array, L, R):
    return sum(array[L : R + 1])


def update_no_cache(array, index, value):
    array[index] = value


@lru_cache(maxsize=1000)
def range_sum_with_cache(array_tuple, L, R):
    array = list(array_tuple)
    return sum(array[L : R + 1])


def update_with_cache(array, index, value):
    array[index] = value
    range_sum_with_cache.cache_clear()


def generate_test_data(N, Q):
    array = [random.randint(1, 1000) for _ in range(N)]
    queries = []
    for _ in range(Q):
        if random.random() < 0.7:
            L = random.randint(0, N - 1)
            R = random.randint(L, N - 1)
            queries.append(("Range", L, R))
        else:
            index = random.randint(0, N - 1)
            value = random.randint(1, 1000)
            queries.append(("Update", index, value))
    return array, queries


def run_tests():
    N, Q = 100000, 50000
    array, queries = generate_test_data(N, Q)

    # Без кешу
    start = time.time()
    for query in queries:
        if query[0] == "Range":
            range_sum_no_cache(array, query[1], query[2])
        else:
            update_no_cache(array, query[1], query[2])
    no_cache_time = time.time() - start

    # З кешем
    array_tuple = tuple(array)
    start = time.time()
    for query in queries:
        if query[0] == "Range":
            range_sum_with_cache(array_tuple, query[1], query[2])
        else:
            update_with_cache(array, query[1], query[2])
    cache_time = time.time() - start

    print(f"Час виконання без кешу: {no_cache_time:.2f} секунд")
    print(f"Час виконання з LRU-кешем: {cache_time:.2f} секунд")


if __name__ == "__main__":
    run_tests()
